#
# Conditional build:
%bcond_without	tests		# build without tests

%define	gem_name bson
Summary:	Ruby implementation of BSON
Name:		ruby-%{gem_name}
Version:	1.6.4
Release:	2
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	b57dc6b0d7f52424e5854b4442e09ea3
URL:		http://www.mongodb.org
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-json
BuildRequires:	ruby-minitest
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Ruby BSON implementation for MongoDB. For more information about
Mongo, see <http://www.mongodb.org>. For more information on BSON, see
<http://www.bsonspec.org>.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
%if %{with tests}
# Run the test suite with minitest.
# https://jira.mongodb.org/browse/RUBY-465
sed -i "/gem 'test-unit'/ d" test/bson/test_helper.rb

testrb -Ilib test/**/*_test.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%attr(755,root,root) %{_bindir}/b2json
%attr(755,root,root) %{_bindir}/j2bson
%{ruby_vendorlibdir}/bson.rb
%{ruby_vendorlibdir}/bson
