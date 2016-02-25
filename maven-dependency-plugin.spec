%global pkg_name maven-dependency-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.7
Release:        3.14%{?dist}
Summary:        Plugin to manipulate, copy and unpack local and remote artifacts

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/%{pkg_name}
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip
Patch0:         0001-Add-setThreshold-stub.patch
# Added apache-commons-io dep
Patch1:         %{pkg_name}-commons-io.patch
# Added maven-core dep
Patch2:         %{pkg_name}-core.patch
# Removed exception catching as it has already been done
# (not upstreamable)
Patch4:         %{pkg_name}-removed-exception-catching.patch

BuildArch:      noarch

BuildRequires: %{?scl_prefix}plexus-utils
BuildRequires: %{?scl_prefix_java_common}ant
BuildRequires: %{?scl_prefix_java_common}apache-commons-io
BuildRequires: %{?scl_prefix}maven-local
BuildRequires: %{?scl_prefix}maven-install-plugin
BuildRequires: %{?scl_prefix}maven-compiler-plugin
BuildRequires: %{?scl_prefix}maven-dependency-tree
BuildRequires: %{?scl_prefix}maven-plugin-plugin
BuildRequires: %{?scl_prefix}maven-plugin-annotations
BuildRequires: %{?scl_prefix}maven-resources-plugin
BuildRequires: %{?scl_prefix}maven-surefire-plugin
BuildRequires: %{?scl_prefix}maven-surefire-provider-junit
BuildRequires: %{?scl_prefix}maven-jar-plugin
BuildRequires: %{?scl_prefix}maven-javadoc-plugin
BuildRequires: %{?scl_prefix}maven-dependency-analyzer
BuildRequires: %{?scl_prefix}maven-common-artifact-filters
BuildRequires: %{?scl_prefix}maven-file-management
BuildRequires: %{?scl_prefix}maven-project
BuildRequires: %{?scl_prefix}maven-artifact-manager
BuildRequires: %{?scl_prefix}maven-plugin-testing-tools


%description

The dependency plugin provides the capability to manipulate
artifacts. It can copy and/or unpack artifacts from local or remote
repositories to a specified location.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
%{summary}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1

sed -i \
    's:org.codehaus.classworlds.ClassRealm:org.codehaus.plexus.classworlds.realm.ClassRealm:' \
    src/test/java/org/apache/maven/plugin/dependency/its/AbstractDependencyPluginITCase.java
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Tests fail to compile because they use unsupported legacy API.
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 2.7-3.14
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 2.7-3.13
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.7-3.12
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.11
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.7-3.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 2.7-3.9
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.7-3.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-3.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.7-3
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.7-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Mar 15 2013 Michal Srb <msrb@redhat.com> - 2.7-1
- Update to upstream version 2.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-1
- Update to upstream version 2.6
- Build with xmvn
- Install license files

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.1-2
- Remove unneeded BR: asm2

* Tue Aug 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.1-1
- Update to upstream version 2.5.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Tomas Radej <tradej@redhat.com> - 2.4-1
- Updated to the upstream version
- Partially removed a test because of a legacy class use
- Removed exception checking as it has already been done

* Fri Jan 13 2012 Alexander Kurtakov <akurtako@redhat.com> 2.3-3
- Add missing BR.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-1
- Update to latest upstream

* Tue Jun 28 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-2
- BR/R maven-shared-file-management.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to 2.2 final release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.4.svn949573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-0.3.svn949573
- Fix test case to expect new classworlds

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2-0.2.svn949573
- Add missing Requires.

* Thu Jun  3 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-0.1.svn949573
- Initial package
