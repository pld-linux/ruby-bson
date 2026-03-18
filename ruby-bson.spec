#
# Conditional build:
%bcond_without	tests		# build without tests

%define	gem_name bson
Summary:	Ruby implementation of BSON
Name:		ruby-%{gem_name}
Version:	5.2.0
Release:	1
License:	Apache-2.0
Group:		Development/Languages
Obsoletes:	ruby-bson-doc < %{version}-%{release}
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	48cce5da08593134fef87ef9c857893d
URL:		https://github.com/mongodb/bson-ruby
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-json
BuildRequires:	ruby-rspec-core
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Ruby BSON implementation for MongoDB. For more information about
Mongo, see <http://www.mongodb.org>. For more information on BSON, see
<http://www.bsonspec.org>.

%prep
%setup -q -n %{gem_name}-%{version}

%build
cd ext/bson
%{__ruby} extconf.rb
%{__make}
cd ../..
cp ext/bson/bson_native.so lib/
%if %{with tests}
%{__ruby} -rrubygems -S rspec spec/**/*_spec.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.md CONTRIBUTING.md CHANGELOG.md
%attr(755,root,root) %{ruby_vendorlibdir}/bson_native.so
%{ruby_vendorlibdir}/bson.rb
%{ruby_vendorlibdir}/bson
