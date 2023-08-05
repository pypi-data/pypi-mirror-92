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

"""Generate a report of IGWN Computing Grid usage for a 24-hour period.
"""

import argparse
import datetime
import json
import logging
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from getpass import getuser
from math import ceil
from pathlib import Path
from shutil import which
from socket import getfqdn

from dateutil.parser import parse as _parse_date
from dateutil import tz

import htcondor

from . import __version__

try:
    from htcondor import HTCondorException
except ImportError:  # htcondor < 8.9.0
    HTCONDOR_8_8 = True
    HTCondorException = RuntimeError
else:
    HTCONDOR_8_8 = False

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

PROG = "igwn-accounting-report"

# configure logger
LOGGER = logging.getLogger(PROG)
_HANDLER = logging.StreamHandler(sys.stderr)
_HANDLER.setFormatter(
    logging.Formatter('[%(name)s %(asctime)s] %(levelname)+8s: %(message)s'),
)
LOGGER.addHandler(_HANDLER)
LOGGER.setLevel(logging.INFO)

# date handling
UTC = tz.tzutc()
LOCAL = tz.tzlocal()
NOW = datetime.datetime.utcnow().replace(
    microsecond=0,
    tzinfo=UTC,
)
TODAY = NOW.replace(hour=0, minute=0, second=0)
YESTERDAY = TODAY + datetime.timedelta(days=-1)

# condor history data
IGWN_USER_CLASSAD = "LigoSearchUser"
IGWN_TAG_CLASSAD = "LigoSearchTag"
HISTORY_CLASSADS = [
    IGWN_USER_CLASSAD,
    IGWN_TAG_CLASSAD,
    "CpusProvisioned",
    "CumulativeSuspensionTime",
    "MATCH_GLIDEIN_Site",
    "MATCH_EXP_JOBGLIDEIN_ResourceName",
    "Owner",
    "RemoteWallClockTime",
    "RequestCpus",
]


# -- utilities --------------

def comment(*args, **kwargs):
    """Print a comment (text preceded by a hash)
    """
    print("#", end=" ", file=kwargs.get("file"))
    print(*args, **kwargs)


def parse_date(input_):
    date = _parse_date(input_)
    return date.replace(tzinfo=UTC)


def find_epoch(utcstart, days=1, **delta):
    """Returns the Unix epoch [start, end) interval for the given UTC day

    Parameters
    ----------
    utcstart : `datetime.datetime`
        the UTC start datetime of the interval

    days, **delta
        duration of interval expressed as keyword arguments to
        :class:`datetime.timedelta`

    Returns
    -------
    utcstart, utcend : `float`
        a pair of Unix epoch floats that define the interval
    """
    utcend = utcstart + datetime.timedelta(days=days, **delta)
    return utcstart.timestamp(), utcend.timestamp()


def parse_job(job, cluster):
    """Parse the information about a job into what we want

    Returns
    -------
    owner : `str`
        the name of the job owner
    tag : `str`
        the search tag used
    cpu_hours : `float`
        the total cost of this job in CPU hours
    cluster : `str`
        the name of the cluster to use in the accounting

    Notes
    -----
    The ``cpu_hours`` is calculated as

        RequestCpus * (RemoteWallclockTime - CumulativeSuspensionTime) / hour
    """
    owner = job.get(IGWN_USER_CLASSAD, job.get("Owner", "UNKNOWN"))
    tag = job.get(IGWN_TAG_CLASSAD, job.get("AccountingGroup", "UNDEFINED"))
    # get cpus
    try:
        cpus = float(job["CpusProvisioned"])
    except (KeyError, ValueError):
        cpus = float(job.get("RequestCpus", 1))
    # get total job time (seconds)
    runtime = (
        float(job["RemoteWallClockTime"]) -
        float(job["CumulativeSuspensionTime"])
    )
    # if job was assigned a MATCH_GLIDEIN_Site, then it was submitted
    # to the OSG scheduler, otherwise it's a local job.
    if job.get("MATCH_GLIDEIN_Site", "undefined") != "undefined":
        if job["MATCH_EXP_JOBGLIDEIN_ResourceName"] == "Local Job":
            cluster = "OSG.{}".format(cluster)
        else:
            cluster = "OSG.{}".format(job["MATCH_GLIDEIN_Site"])
    else:
        cluster = cluster

    return owner, tag, cpus * runtime / 3600., cluster


# -- command-line parsing ---

class HelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    """Help formatter with customisations to support argparse-manpage
    """
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = "Usage: "
        return super()._format_usage(
            usage,
            actions,
            groups,
            prefix,
        )


class ArgumentParser(argparse.ArgumentParser):
    """`ArgumentParser` with customisations to support argparse-manpage
    """
    def __init__(self, *args, **kwargs):
        manpage = kwargs.pop("manpage", None)

        kwargs.setdefault("description", __doc__)
        kwargs.setdefault("formatter_class", HelpFormatter)
        super(ArgumentParser, self).__init__(*args, **kwargs)

        self._positionals.title = "Required arguments"
        self._optionals.title = "Options"

        # add manpage options for argparse-manpage
        self._manpage = manpage


def create_parser():
    """Create a command-line parser for this tool
    """
    parser = ArgumentParser(prog=PROG)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="show verbose output",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=__version__,
        help="show version number and exit",
    )
    parser.add_argument(
        "-c",
        "--cluster",
        required=True,
        help="computing centre from which the accounting data comes "
             "(required)",
    )
    parser.add_argument(
        "-s",
        "--schedulers",
        nargs="*",
        help="schedulers to query, multiple arguments can be given",
    )
    parser.add_argument(
        "-p",
        "--pool",
        help="name of collector to query",
    )
    parser.add_argument(
        "-u",
        "--utc",
        default=YESTERDAY,
        type=parse_date,
        help="UTC date to query",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default="stdout",
        help="path of file to write output into",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("json", "ascii"),
        default="ascii",
        help="output format",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="number of processes to use",
    )
    parser.add_argument(
        "-w",
        "--warn-on-error",
        action="store_true",
        default=False,
        help="only print a warning when history queries fail "
             "rather than erroring",
    )

    # augment parser for argparse-manpage
    parser.man_short_description = "generate a condor usage report"

    return parser


# -- condor interactions ----

def find_schedulers(pool=None):
    """Returns the names of all schedulers known by the condor collector
    """
    coll = htcondor.Collector(pool)
    scheds = [
        schedd["name"] for
        schedd in coll.locateAll(htcondor.DaemonTypes.Schedd)
    ]
    if not scheds:
        raise RuntimeError(
            "condor_status did not return any schedd names",
        )
    return scheds


def get_history(
        schedname,
        cluster,
        start,
        end,
        classads=HISTORY_CLASSADS,
        pool=None,
):
    """Query for all jobs that completed in the given interval

    Parameters
    ----------
    schedname : `str`
        the (host)name of the scheduler to query

    start : `float`
        the Unix epoch start of the relevant interval

    end : `float`
        the Unix epoch end of the relevant interval

    classads : `list` of `str`
        the list of classads to return for each job

    Returns
    -------
    history : `iterable` of `dict`
        the raw output from :meth:`htcondor.Schedd.history`
    """
    since = "JobFinishedHookDone < {}".format(start)
    constraint = " && ".join((
        "JobStatus != 3",
        "JobUniverse != 7",
        "Owner != \"igwn-pilot\"",
        "EnteredCurrentStatus <= {}".format(end),
    ))
    args = (schedname, constraint, classads, since, pool)
    try:
        history = _get_history_python(*args)
        for job in history:
            yield parse_job(job, cluster)
    except HTCondorException as exc:
        LOGGER.warning(
            "history query using python API failed: {}, "
            "retrying using condor_history executable [{}]".format(
                str(exc),
                schedname,
            ),
        )
        for job in _get_history_subprocess(*args):
            yield parse_job(job, cluster)


def _get_history_python(schedname, constraint, classads, since, pool):
    try:
        schedd_ad = htcondor.Collector(pool).locate(
            htcondor.DaemonTypes.Schedd,
            schedname,
        )
        schedd = htcondor.Schedd(schedd_ad)
    except HTCondorException:
        # raise proper exceptions normally,
        # this just serves to allow us to separate out ValueErrors
        # that are raised by htcondor < 8.9.0, see below
        # NOTE: this except block can be entirely removed if we get
        #       as far as requiring htcondor >= 8.9.0
        raise
    except ValueError as exc:
        # if htcondor < 8.9.0, translate a ValueError into a
        # RuntimeError so that we can separate it from any other
        # ValueErrors we might get from job parsing or similar
        # NOTE: this block can be entirely removed if we get
        #       as far as requiring htcondor >= 8.9.0
        raise HTCondorException(str(exc)) from exc
    return schedd.history(
        constraint,
        projection=classads,
        since=since,
    )


def _get_history_subprocess(schedname, constraint, classads, since, pool):
    cmd = [
        which("condor_history"),
        "-name", schedname,
        "-since", since,
        "-constraint", constraint,
    ]
    if not HTCONDOR_8_8:  # htcondor >=8.9.0
        cmd.extend(["-jsonl", "-af"] + classads)
    else:  # htcondor < 8.9.0
        cmd.extend(_format_condor_history_classads(classads))
    if pool:
        cmd.extend(("-pool", pool))
    load_json = json.loads
    for line in subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
    ).stdout.splitlines():
        if not HTCONDOR_8_8:  # htcondor >= 8.9.0
            yield load_json(line)
        else:  # htcondor < 8.9.0
            data = load_json(line)
            for key in list(data.keys()):
                if data[key] == "undefined":  # just ignore undefined classads
                    del data[key]
            yield data


def _format_condor_history_classads(classads):
    """Returns a list of `-format <str> <classad>` arguments for condor_history

    Notes
    -----
    This is only required to support htcondor < 8.9.0 and can be removed when
    we can require htcondor >=8.9.0
    """
    args = [
        "-format",
        "{{\"{}\": \"%v\", ".format(classads[0]),
        classads[0],
    ]
    for classad in classads[1:-1]:
        args.extend((
            "-format",
            "\"{}\": \"%v\", ".format(classad),
            classad
        ))
    args.extend((
        "-format",
        "\"{}\": \"%v\"}}\\n".format(classads[-1]),
        classads[-1],
    ))
    return args


def get_all_history(schedulers, cluster, start, end, error=True, pool=None):
    """Yield all jobs from all schedulers
    """
    for sched in schedulers:
        yield from _handle_history(
            get_history(sched, cluster, start, end, pool=pool),
            sched,
            error=error,
        )


def _handle_history(iterator, sched, error=True, iterate=True):
    try:
        yield from iterator
    except (RuntimeError, ValueError) as exc:
        exc.args = (str(exc) + " [{}]".format(sched),)
        if error:
            LOGGER.critical(str(exc))
            raise
        LOGGER.warning(str(exc))
    else:
        LOGGER.debug("Data received from {}".format(sched))


def _get_history_mp(sched, *args, error=True, **kwargs):
    return list(_handle_history(
        get_history(sched, *args, **kwargs),
        sched,
        error=error,
        iterate=False,
    ))


def get_all_history_mp(
        nproc,
        schedulers,
        cluster,
        start,
        end,
        error=True,
        pool=None,
):
    _get_history = partial(
        _get_history_mp,
        cluster=cluster,
        start=start,
        end=end,
        error=error,
        pool=pool,
    )
    with ProcessPoolExecutor(nproc) as pool:
        for result in pool.map(_get_history, schedulers):
            yield from result


def get_run_metadata():
    """Returns a `dict` of useful metadata regarding this process

    Mainly for debugging issues with the data.
    """
    if Path("/usr/bin/condor_version").exists():
        system_condor_version = subprocess.check_output(
            ["/usr/bin/condor_version"],
            encoding="utf-8",
        )
    else:
        system_condor_version = None
    return {
        "collector_name": "igwn-accounting-report",
        "collector_version": __version__,
        "python_version": sys.version,
        "system_condor_version": system_condor_version,
        "host": getfqdn(),
        "user": getuser(),
        "utcdate": str(datetime.datetime.utcnow()),
        "cmd": " ".join(sys.argv),
    }


def print_ascii(data, utc, file):
    for key in sorted(data):
        owner, tag, jobcluster = key
        print(
            "{} {} {} {} {}".format(
                owner,
                tag,
                ceil(data[key]),
                utc,
                jobcluster,
            ),
            file=file,
        )


def print_json(data, utc, file):
    reformatted = []
    for key in sorted(data):
        owner, tag, jobcluster = key
        reformatted.append({
            "user": owner,
            "tag": tag,
            "resource": jobcluster,
            "utcdate": utc,
            "usage": ceil(data[key]),
        })

    jdata = {
        "data": reformatted,
        "meta": get_run_metadata(),
    }

    json.dump(
        jdata,
        file,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )


def main(args=None):
    """Run the thing

    Parameters
    ----------
    args : `list`
        the input command line arguments, defaults to `sys.argv`
    """
    global LOGGER

    parser = create_parser()
    args = parser.parse_args(args=args)

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    # finalise epoch to query
    start, end = find_epoch(args.utc)
    startutc = datetime.datetime.utcfromtimestamp(start).replace(tzinfo=UTC)
    endutc = datetime.datetime.utcfromtimestamp(end).replace(tzinfo=UTC)
    LOGGER.info("Now: {} | {}".format(NOW, NOW.astimezone(LOCAL)))
    LOGGER.info(
        "Epoch start: {} | {} | {}".format(
            start,
            startutc,
            startutc.astimezone(LOCAL)
        ),
    )
    LOGGER.info(
        "Epoch end:   {} | {} | {}".format(
            end,
            endutc,
            endutc.astimezone(LOCAL)
        ),
    )

    # find schedulers
    schedulers = args.schedulers or find_schedulers(args.pool)
    LOGGER.info("Querying {} schedulers".format(len(schedulers)))
    for sched in sorted(schedulers):
        LOGGER.debug("  {}".format(sched))

    accounting = defaultdict(int)
    cluster = args.cluster

    # get history
    args.jobs = min(args.jobs, len(schedulers))
    if args.jobs != 1:
        history = get_all_history_mp(
            args.jobs,
            schedulers,
            cluster,
            start,
            end,
            error=not args.warn_on_error,
            pool=args.pool,
        )
    else:
        history = get_all_history(
            schedulers,
            cluster,
            start,
            end,
            error=not args.warn_on_error,
            pool=args.pool,
        )
    for i, (owner, tag, cost, jobcluster) in enumerate(history):
        accounting[(owner, tag, jobcluster)] += cost
    try:
        LOGGER.info("Parsed {} jobs".format(i+1))
    except UnboundLocalError:
        LOGGER.warning("Parsed 0 jobs")
    LOGGER.info("Writing output")

    date = startutc.strftime("%Y-%m-%d")

    if args.output_file == "stdout":
        file = sys.stdout
    else:
        file = open(args.output_file, "w")

    # write
    try:
        if args.format == "ascii":
            print_ascii(accounting, date, file)
        elif args.format == "json":
            print_json(accounting, date, file)
            if file is sys.stdout:  # json doesn't print trailing newline
                print()
    finally:
        if file is not sys.stdout:
            file.close()
            LOGGER.debug("Output written to {}".format(args.output_file))


# execute the module (enables running as `python -m igwn_accounting.report`)
if __name__ == "__main__":
    main()
