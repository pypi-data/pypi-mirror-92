Summary: Utilities for obtaining short-lived proxy certificates for LIGO
Name: ligo-proxy-utils
Version: 2.0.0
Release: 1%{?dist}
Source0: http://software.igwn.org/sources/source/%{name}-%{version}.tar.gz
License: GPLv3+
BuildArch: noarch
Url: https://wiki.ligo.org/AuthProject

# -- build requirements

# macros
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros

# build
BuildRequires: python3
BuildRequires: python%{python3_pkgversion}-setuptools

# tests
BuildRequires: python%{python3_pkgversion}-pytest
BuildRequires: python%{python3_pkgversion}-ciecplib >= 0.4.1-2

# man pages
%if 0%{?rhel} == 0 || 0%{?rhel} >= 8
BuildRequires: python%{python3_pkgversion}-argparse-manpage
%else
BuildRequires: help2man
%endif

# -- packages

# ligo-proxy-utils
Requires: python%{python3_pkgversion}-ligo-proxy-utils = %{version}-%{release}
Requires: python%{python3_pkgversion}-setuptools
%description
Command line utilities for generating short-lived LIGO Credentials

# python3-ligo-proxy-utils
%package -n python%{python3_pkgversion}-%{name}
Summary: Python %{python3_version} modules for %{name}
Requires: python%{python3_pkgversion}-ciecplib
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
The Python %{python3_version} modules for %{name}

# -- build

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

# for RHEL<8 generate the man page using help2man
%if 0%{?rhel} > 0 && 0%{?rhel} < 8
mkdir -p %{buildroot}%{_mandir}/man1/
env PYTHONPATH=%{buildroot}%{python3_sitelib} help2man \
	--source %{name} \
	--no-info \
	--no-discard-stderr \
	--name "generate a LIGO.ORG X.509 credential using CIECPLib" \
	--output %{buildroot}%{_mandir}/man1/ligo-proxy-init.1 \
	%{buildroot}%{_bindir}/ligo-proxy-init
%endif

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
export PATH="%{buildroot}%{_bindir}:${PATH}"
# run the unit tests
%{__python3} -m pytest --pyargs ligo_proxy_utils.tests
# test basic executable functionality
ligo-proxy-init -h
ligo-proxy-init -v

%clean
rm -rf $RPM_BUILD_ROOT

# -- files

%files -n python%{python3_pkgversion}-%{name}
%license COPYING
%doc README.md
%{python3_sitelib}

%files
%license COPYING
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*.1*

# -- changelog

%changelog
* Wed Jan 27 2021 Duncan Macleod <duncan.macleod@ligo.org> - 2.0.0-1
- rewrite in python

* Thu Dec 03 2020 Satya Mohapatra <patra@mit.edu> - 1.3.6-1
- kagra access
* Mon Dec 17 2018 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.5-1
- Use 2048 bits for RFC 3820 compliant impersonation proxy
* Wed Nov 28 2018 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.4-1
- Use addressbook.ligo.org to verify uid instead of ldap.ligo.org
* Wed Apr 12 2017 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.3-1
- Remove shred and store intermediate files in /dev/shm if available
* Fri Dec 02 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.2-1
- Add option to specify certificate lifetime which now defaults to 11.5 days
* Tue Nov 22 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.1-1
- Add option to create RFC 3820 compliant impersonation proxy
* Mon Aug 01 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.3.0-1
- Remove LDAP user check
- Use "rm -P" to safely delete files on Mac OS X
* Mon Jun 13 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.5-1
- Allow Virgo members to use ligo-proxy-init
- Print LDAP lookup warning only in debug mode
* Wed Feb 17 2016 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.4-1
- Perform LDAP lookup check on port 80
- Continue script if LDAP lookup check fails to run
* Thu Nov 05 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.3-1
- Fixed bugs in Kerberos support
- Modified user validity check to use unencrypted connection
* Thu Oct 15 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.2-1
- Modified group check to only whitelist LSC and LIGOLab
- Fixed invalid password warning
- Added explicit Kerberos support
- Added destroy option
* Mon Jul 20 2015 Paul Hopkins <paul.hopkins@ligo.org> - 1.2.1-1
- Added automatic failover for LIGO IdP servers
* Fri Jun 06 2014 Adam Mercer <adam.mercer@ligo.org) - 1.0.1-1
- Curl now asks for password directly
- Clears (DY)LD_LIBRARY_PATH environment variables
- Explicitly sets umask
- Checks user is not Virgo member
- Minor bugfixes
* Fri Feb 22 2013 Scott Koranda <scott.koranda@ligo.org> - 1.0.0-1
- Initial version.
