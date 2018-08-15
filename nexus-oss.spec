# since we are packaging the compiled java app we disable these
%define debug_package %{nil}
%define __jar_repack %{nil}

%define org sonatype
%define product nexus
%define upstream_version 2.14.9
%define upstream_release 01

Name:           %{product}-oss
Version:        %{upstream_version}.%{upstream_release}
Release:        1%{?dist}
Summary:        Sonatype Nexus OSS Repository Manager

Group:          applications/system
License:        EPL
URL:            https://sonatype.org/nexus
#this is the actual source release
#Source0:        https://github.com/sonatype/%{name}/archive/%{product}-%{upstream_version}-%{upstream_release}.tar.gz
# This is the bundled built release
Source0:        http://download.sonatype.com/nexus/oss/%{product}-%{upstream_version}-%{upstream_release}-bundle.tar.gz
Source1:        sysconfig.default
Patch0:         sysvinit.patch

AutoReqProv:    no
Requires:       jre = 1.7.0
Requires(pre):  shadow-utils

%description
Sonatype Nexus OSS Repository Manager

%prep
%setup -q -n %{product}-%{upstream_version}-%{upstream_release}
%patch0

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{product}
mkdir -p $RPM_BUILD_ROOT/opt/%{org}
cd ..
cp -pr %{product}-%{upstream_version}-%{upstream_release} $RPM_BUILD_ROOT/opt/%{org}/%{product}
cp -pr sonatype-work $RPM_BUILD_ROOT/opt/%{org}/
mkdir -p $RPM_BUILD_ROOT/%{_initddir}
mv $RPM_BUILD_ROOT/opt/%{org}/%{product}/bin/%{product} $RPM_BUILD_ROOT/%{_initddir}/
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/run/%{product}

#Some cross platform cleanup
rm -rf $RPM_BUILD_ROOT/opt/%{org}/bin/jsw/macosx-*
rm -rf $RPM_BUILD_ROOT/opt/%{org}/bin/jsw/solaris-*
rm -rf $RPM_BUILD_ROOT/opt/%{org}/bin/jsw/windows-*
rm -rf $RPM_BUILD_ROOT/opt/%{org}/bin/nexus.bat

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{product} >/dev/null || groupadd -r %{product}
getent passwd %{product} >/dev/null || \
    useradd -r -g %{product} -d /opt/%{org}/%{product} -s /sbin/nologin \
    -c "System Account for Sonatype %{product} OSS" %{product}
exit 0

%files
%defattr(-,nexus,nexus,-)
%doc
/opt/%{org}/
%{_initddir}/%{product}
%{_sysconfdir}/sysconfig/%{product}
%dir %{_localstatedir}/run/%{product}

%changelog
* Wed Aug 15 2018 Greg Swift <gregswift@gmail.com> - 2.14.9.01-1
- Update to last 2 upstream

* Mon Apr 25 2016 Greg Swift <gregswift@gmail.com> - 2.13.0.01-1
- Update to upstream
- https://support.sonatype.com/hc/en-us/articles/218229168-Nexus-Repository-Manager-2-13-Release-Notes

* Mon Nov 02 2015 Greg Swift <gregswift@gmail.com> - 2.11.4.01-1
- Update to upstream
- https://support.sonatype.com/entries/95320157-Sonatype-Nexus-2-11-4-Release-Notes

* Mon Apr 27 2015 Greg Swift <gregswift@gmail.com> - 2.11.2.06-1
- Update to upstream. Bypassing a bad release
- https://support.sonatype.com/entries/87851808-Sonatype-Nexus-2-11-2-Release-Notes

* Tue Jan 06 2015 Greg Swift <gregswift@gmail.com> - 2.11.1.01-1
- Update for CVE-2014-9389
