#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		subver	20011111cvs
%define		rel		1
%define		srcname		xmldb
Summary:	XML:DB API for Java
Name:		java-%{srcname}
Version:	0.1
Release:	0.%{subver}.%{rel}
License:	BSD
Group:		Development/Languages/Java
Obsoletes:	xmldb-api
# wget http://trumpetti.atm.tut.fi/gentoo/distfiles/xmldb-api-11112001.tar.gz
Source0:	xmldb-xapi-%{subver}-src.tar.gz
# Source0-md5:  559bdc3a09ea2dd6cd914103631e7141
# http://sources.gentoo.org/viewcvs.py/gentoo-x86/dev-java/xmldb/files/build-20011111.xml?rev=1.1.1.1&view=markup
Source1:	build.xml
Source2:	license.txt
Patch0:		syntaxfix.patch
URL:		http://xmldb-org.sourceforge.net/
BuildRequires:	ant >= 1.6
BuildRequires:	java-junit
BuildRequires:	java-xalan
BuildRequires:	jpackage-utils >= 1.6
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-junit
Requires:	java-xalan
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The API interfaces are what driver developers must implement when
creating a new driver and are the interfaces that applications are
developed against. Along with the interfaces a concrete DriverManager
implementation is also provides.

%package sdk
Summary:	SDK for XML:DB
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	xmldb-api-sdk

%description sdk
The reference implementation provides a very simple file system based
implementation of the XML:DB API. This provides what is basically a
very simple native XML database that uses directories to represent
collections and just stores the XML in files.

The driver development kit provides a set of base classes that can be
extended to simplify and speed the development of XML:DB API drivers.
These classes are used to provide the basis for the reference
implementation and therefore a simple example of how a driver can be
implemented. Using the SDK classes significantly reduces the amount of
code that must be written to create a new driver.

Along with the SDK base classes the SDK also contains a set of jUnit
test cases that can be used to help validate the driver while it is
being developed. The test cases are still in development but there are
enough tests currently to be useful.

%package javadoc
Summary:	Javadoc for XML:DB
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for XML:DB.

%prep
%setup -q -n xmldb
%patch0
find -name "*.jar" | xargs rm -v
cp -p %{SOURCE1} build.xml
cp -p %{SOURCE2} license.txt

%build
CLASSPATH=$(build-classpath junit xalan)
%ant jar %{?with_javadoc:javadoc} \
	-Dsrc=. \
	-Djar=%{srcname}.jar \
	-Dsdk-jar=%{srcname}-sdk.jar

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
cp -a dist/%{srcname}-sdk.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-sdk-%{version}.jar
ln -s %{srcname}-sdk-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-sdk.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a dist/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc license.txt
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%files sdk
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-sdk-%{version}.jar
%{_javadir}/%{srcname}-sdk.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
