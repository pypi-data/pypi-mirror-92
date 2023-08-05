# -- metadata ---------------

Name:      igwn-accounting
Version:   1.0.0
Release:   1%{?dist}

BuildArch: noarch
Group:     Development/Libraries
License:   ASL 2.0
Packager:  Duncan Macleod <duncan.macleod@ligo.org>
Prefix:    %{_prefix}
Source0:   %pypi_source
Summary:   IGWN Computing accounting tools
Url:       https://accounting.ligo.org
Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

# -- build requirements -----

# macros
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build
BuildRequires: python3
BuildRequires: python%{python3_pkgversion}-setuptools

# man pages (only on rhel8 or later)
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-argparse-manpage
BuildRequires: python3-condor
BuildRequires: python%{python3_pkgversion}-dateutil
%endif

# -- packages ---------------

#%% package -n igwn-accounting
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Requires: python%{python3_pkgversion}-setuptools
%description
IGWN Computing Accounting tools

%package -n python%{python3_pkgversion}-%{name}
Summary: %{summary}
Requires: python%{python3_pkgversion}-dateutil
Requires: python3-condor
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
The Python %{python3_version} IGWN Accounting library.

# -- build ------------------

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

# -- files ------------------

%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%files
%license LICENSE
%doc README.md
%{_bindir}/*
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
%{_mandir}/man1/*.1*
%endif

# -- changelog --------------

%changelog
* Tue Jan 19 2021 Duncan Macleod <duncan.macleod@ligo.org> - 1.0.0-1
- initial release
