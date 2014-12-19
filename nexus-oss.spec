# since we are packaging the compiled java app we disable these
%define debug_package %{nil}
%define __jar_repack %{nil}

%define org sonatype
%define product nexus
%define upstream_version 2.11.0
%define upstream_release 02

Name:           %{product}-oss
Version:        %{upstream_version}.%{upstream_release}
Release:        1%{?dist}
Summary:        Sonatype Nexus OSS Repository Manager

Group:          applications/system
License:        EPL
URL:            https://sonatype.org/nexus
#this is the actual source release
#Source0:        https://github.com/sonatype/%{name}/archive/nexus-%{upstream_version}-%{upstream_release}.tar.gz
# This is the bundled built release
Source0:         http://download.sonatype.com/nexus/oss/nexus-%{upstream_version}-%{upstream_release}-bundle.tar.gz

Requires:       java

%description
Sonatype Nexus OSS Repository Manager

%prep
%setup -q -n nexus-%{upstream_version}-%{upstream_release}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/%{org}
cp -pr * $RPM_BUILD_ROOT/opt/%{org}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
/opt/%{org}/


%changelog
