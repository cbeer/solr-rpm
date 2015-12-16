%define debug_package %{nil}
%define solr_install_dir %{_javadir}/solr
%define plugin_install_dir %{solr_install_dir}/plugins
%define plugin_name dataimporthandler-extras
%define plugin_source_dir contrib/%{plugin_name}

Name:           solr-%{plugin_name}
Version:        5.4.0
Release:        0%{?dist}
Summary:        A distributed, highly available, RESTful search engine

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://lucene.apache.org/solr/
Source0:        http://archive.apache.org/dist/lucene/solr/%{version}/solr-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       solr >= %{version}

Provides: %{name}

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n solr-%{version}

%build
true

%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir} -p %{buildroot}%{plugin_install_dir}
%{__install} -p -m 755 %{plugin_source_dir}/lib/* %{buildroot}%{plugin_install_dir}
%{__install} -p -m 755 dist/solr-%{plugin_name}-* %{buildroot}%{plugin_install_dir}

%{__mkdir} -p %{buildroot}%{solr_install_dir}/docs/solr-%{plugin_name}
%{__cp} -R -p docs/solr-%{plugin_name}/* %{buildroot}%{solr_install_dir}/docs/solr-%{plugin_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{plugin_install_dir}/*
%{solr_install_dir}/docs/solr-%{plugin_name}
%docdir %{solr_install_dir}/docs/solr-%{plugin_name}

%changelog

* Sat Dec 15 2015 Chris Beer <chris@cbeer.info> - 5.4.0-0
- Update to Solr 5.4.0

* Sat Sep 26 2015 Chris Beer <chris@cbeer.info> - 5.3.1-0
- Update to Solr 5.3.1

* Thu Sep 10 2015 Chris Beer <chris@cbeer.info> - 5.3.0-1
- Update to Solr 5.3.0

* Tue Jun 2 2015 Chris Beer <chris@cbeer.info> - 5.2.1-1
- Initial package