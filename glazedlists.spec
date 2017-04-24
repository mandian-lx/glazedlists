%{?_javapackages_macros:%_javapackages_macros}

# Work around koji build issues on ppc64
# See https://www.redhat.com/archives/fedora-devel-list/2009-March/msg00022.html
%global eclipse_dir $(ls -d /usr/lib*/eclipse)

Name:           glazedlists
Version:        1.9.1
Release:        1.2
Summary:        A toolkit for transformations in Java
Group:		Development/Java
License:        (LGPLv2+ or MPLv1.1+) and ASL 2.0
Url:            http://www.glazedlists.com/
BuildArch:      noarch

Source0:        http://repo1.maven.org/maven2/net/java/dev/glazedlists/%{name}_java15/%{version}/glazedlists_java15-%{version}-dist.zip
# Build against system jars instead of downloaded ones, and don't build things we don't
# have requirements for
Patch0:         %{name}-1.9.1-build.xml.patch
# Use the new Hibernate API
Patch1:         %{name}-1.9.1-hibernate.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  dos2unix
BuildRequires:  aqute-bnd
BuildRequires:  aqute-bndlib
BuildRequires:  eclipse-swt
BuildRequires:  icu4j
BuildRequires:  jcommon
BuildRequires:  jfreechart
BuildRequires:  jgoodies-forms
BuildRequires:  hibernate3
BuildRequires:  hsqldb
BuildRequires:  jvnet-parent

# Adapted from http://www.javaworld.com/javaworld/jw-10-2004/jw-1025-glazed.html
# because the project website doesn't have a good description
%description
Glazed Lists is an open source toolkit for list transformations. If a
developer is already familiar with ArrayList or Vector, he or she will feel
at home with Glazed Lists.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Documentation for the %{name} Java library.

%prep
%setup -q -c %{name}-%{version}
# Build against system jars, and disable unavailable extensions
%patch0 -b .build-xml -p0
rm -rf extensions/ktable extensions/swinglabs extensions/nachocalendar \
        extensions/japex extensions/issuesbrowser 
# Use correct libdir for this build architecture
sed -i.eclipse_dir "s#ECLIPSE_DIR#%{eclipse_dir}#" build.xml

%if 0%{?fedora} >= 23
%global taskdef_classpath /usr/share/java/aqute-bnd/biz.aQute.bnd.jar:/usr/share/java/aqute-bnd/biz.aQute.bndlib.jar
%else
%global taskdef_classpath /usr/share/java/aqute-bnd.jar
%endif

sed -i.taskdef_classpath "s#TASKDEF_CLASSPATH#%{taskdef_classpath}#" build.xml

# Use new hibernate API
#patch1 -b .hibernate -p0

# Clean up line endings
dos2unix license

# Don't download ant tasks
sed -i -e '/"deploy-init"/ s/download-mavenanttasks,//' build.xml

%build
ant -v dist jar sourcejar javadocjar deploy-init -DartifactId=%{name}

# Maven artifact installation
%mvn_artifact target/deploy/pom.xml target/deploy/%{name}-%{version}.jar

# add compatibility alias
%mvn_alias net.java.dev.glazedlists:glazedlists net.java.dev.glazedlists:glazedlists_java15

%install
%mvn_install -J target/docs/api

%files -f .mfiles
%doc license readme.html
%dir %{_javadir}/glazedlists
%dir %{_mavenpomdir}/glazedlists

%files javadoc -f .mfiles-javadoc
%doc license

%changelog
* Tue Jun 07 2016 - Ding-Yi Chen <dchen@redhat.com> 1.9.1-1
- Upstream update to 1.9.1
- Fixes RHBZ #1307537 - glazedlists: FTBFS in rawhide

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 09 2015 Mat Booth <mat.booth@redhat.com> - 1.9.0-6
- Fix FTBFS, rhbz#1096105 and rhbz#1106639
- Move to mfiles
- Fix artifact ID and version in pom

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.9.0-4
- Use Requires: java-headless rebuild (#1067528)

* Mon Oct 14 2013 Mary Ellen Foster <mefoster at gmail.com> - 1.9.0-3
- Enable "treetable" extension which wasn't being built by default 

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Mary Ellen Foster <mefoster at gmail.com> - 1.9.0-1
- Update to 1.9.0
- Revise build process and only enable extensions for which we have dependencies

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Mary Ellen Foster <mefoster at gmail.com> - 1.8.0-3
- Fix license header again
- Add license file to javadoc package
- Remove defattr

* Wed Jan 25 2012 Mary Ellen Foster <mefoster at gmail.com> - 1.8.0-2
- Remove clean section, install unversioned javadocs
- Accurate licenses in header

* Wed Jan 25 2012 Mary Ellen Foster <mefoster at gmail.com> - 1.8.0-1
- Initial package
