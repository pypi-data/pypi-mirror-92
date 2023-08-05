# -*- coding: utf-8 -*-
# Copyright 2020 Cardiff University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the `igwn_accounting.report` module
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import io
import json
import subprocess
import sys
from getpass import getuser
from pathlib import Path
from socket import getfqdn
from unittest import mock

import pytest

from .. import report as igwn_report


def test_comment():
    stream = io.StringIO()
    igwn_report.comment("test", file=stream)
    assert stream.getvalue() == "# test\n"


@pytest.mark.parametrize("userad, tagad", [
    (igwn_report.IGWN_USER_CLASSAD, igwn_report.IGWN_TAG_CLASSAD),
    ("Owner", "AccountingGroup"),
])
def test_parse_job(userad, tagad):
    job = {
        userad: "test",
        tagad: "test.dev.pytest",
        "MATCH_EXP_JOBGLIDEIN_ResourceName": "Local Job",
        "RemoteWallClockTime": 100.,
        "CumulativeSuspensionTime": 10.,
    }
    assert igwn_report.parse_job(job, "deepthought") == (
         "test",
         "test.dev.pytest",
         90/3600.,
         "deepthought",
    )


@pytest.mark.parametrize("glidein_resourcename, glidein_site, jobcluster", [
    # job that didn't report 'Site'
    ("Local Job", "undefined", "deepthought"),
    # distributed job that reported as a local job
    ("Local Job", "Unknown", "OSG.deepthought"),
    # distributed job that ran remotely
    ("TEST", "REMOTE", "OSG.REMOTE"),
])
def test_parse_job_osg(glidein_resourcename, glidein_site, jobcluster):
    job = {
        igwn_report.IGWN_USER_CLASSAD: "test",
        igwn_report.IGWN_TAG_CLASSAD: "test.dev.pytest",
        "CumulativeSuspensionTime": 0.,
        "MATCH_EXP_JOBGLIDEIN_ResourceName": glidein_resourcename,
        "MATCH_GLIDEIN_Site": glidein_site,
        "RemoteWallClockTime": 3600.,
    }
    assert igwn_report.parse_job(job, "deepthought") == (
         "test",
         "test.dev.pytest",
         1.,
         jobcluster,
    )


@mock.patch("shutil.which", return_value="/test/condor_history")
@mock.patch("subprocess.run")
def test_get_history_subprocess(sprun, _):
    igwn_report._get_history_subprocess(
        "sched.test",
        "Owner == test",
        ["A", "B"],
        "ClassAd > 12345",
        "pool.test",
    )
    assert sprun.called_once_with(
        [
            "/test/condor_history",
            "-name", "sched.test",
            "-since", "ClassAD > 12345",
            "-constraint", "Owner == test",
            "-pool", "pool.test",
            "-af", "A", "B",
        ],
        stdout=subprocess.PIPE,
        check=True,
    )


@mock.patch("subprocess.check_output", return_value="condor version 1.2.3")
@mock.patch.object(sys, "argv", ["a", "b", "c"])
@mock.patch.object(Path, "exists")
@mock.patch("datetime.datetime")
@pytest.mark.parametrize("has_condor_version, condor_version", [
    (False, None),
    (True, "condor version 1.2.3"),
])
def test_get_run_metadata(
        mock_datetime,
        mock_path_exists,
        mock_sys_argv,
        has_condor_version,
        condor_version,
):
    # finalise mocks
    mock_datetime.utcnow.return_value = "some date"
    mock_path_exists.return_value = has_condor_version
    # check function formats data correctly
    assert igwn_report.get_run_metadata() == {
        "collector_name": "igwn-accounting-report",
        "collector_version": igwn_report.__version__,
        "user": getuser(),
        "host": getfqdn(),
        "system_condor_version": condor_version,
        "python_version": sys.version,
        "cmd": "a b c",
        "utcdate": "some date",
    }


# end-to-end test with fake data

DATA_FILE = Path(__file__).parent / "condor_history.txt"
RESULT_JSON = json.dumps({
    "data": [
        {"user": "user1", "tag": "tag1", "usage": 7,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user1", "tag": "tag1", "usage": 7,
         "utcdate": "2021-01-01", "resource": "TEST"},
        {"user": "user1", "tag": "tag2", "usage": 2,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user2", "tag": "tag1", "usage": 2,
         "utcdate": "2021-01-01", "resource": "OSG.Remote"},
        {"user": "user2", "tag": "tag1", "usage": 2,
         "utcdate": "2021-01-01", "resource": "TEST"},
    ],
    "meta": {
        "key": "value",
    },
}, indent=None, sort_keys=True, separators=(",", ":"))
RESULT_ASCII = """
user1 tag1 7 2021-01-01 OSG.Remote
user1 tag1 7 2021-01-01 TEST
user1 tag2 2 2021-01-01 OSG.Remote
user2 tag1 2 2021-01-01 OSG.Remote
user2 tag1 2 2021-01-01 TEST
""".strip()


def mock_get_history(*args, **kwargs):
    with DATA_FILE.open("r") as file:
        for line in file:
            yield json.loads(line)


@pytest.mark.parametrize("fmt, expected", (
    ("ascii", RESULT_ASCII),
    ("json", RESULT_JSON),
))
@mock.patch("igwn_accounting.report._get_history_python", mock_get_history)
@mock.patch(
    "igwn_accounting.report.get_run_metadata",
    return_value={"key": "value"},
)
def test_main(_, fmt, expected, tmpdir):
    output = tmpdir.join("output.txt")
    igwn_report.main([
        "--cluster", "TEST",
        "--scheduler", "test.sched",
        "--utc", "2021-01-01",
        "--output-file", str(output),
        "--format", fmt,
    ])
    # check output matches
    assert output.read().strip() == expected
