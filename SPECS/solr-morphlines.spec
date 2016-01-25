%define debug_package %{nil}
%define solr_install_dir %{_javadir}/solr
%define plugin_install_dir %{solr_install_dir}/plugins
%define plugin_name morphlines
%define plugin_source_dir contrib/%{plugin_name}

Name:           solr-%{plugin_name}
Version:        5.4.1
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
%{__install} -p -m 755 contrib/morphlines-cell/lib/* %{buildroot}%{plugin_install_dir}
%{__install} -p -m 755 contrib/morphlines-core/lib/* %{buildroot}%{plugin_install_dir}
%{__install} -p -m 755 dist/solr-%{plugin_name}-cell-* %{buildroot}%{plugin_install_dir}
%{__install} -p -m 755 dist/solr-%{plugin_name}-core-* %{buildroot}%{plugin_install_dir}

%{__mkdir} -p %{buildroot}%{solr_install_dir}/docs/solr-%{plugin_name}-cell
%{__mkdir} -p %{buildroot}%{solr_install_dir}/docs/solr-%{plugin_name}-core
%{__cp} -R -p docs/solr-%{plugin_name}-cell/* %{buildroot}%{solr_install_dir}/docs/solr-%{plugin_name}-cell
%{__cp} -R -p docs/solr-%{plugin_name}-core/* %{buildroot}%{solr_install_dir}/docs/solr-%{plugin_name}-core

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{plugin_install_dir}/*
%{solr_install_dir}/docs/solr-%{plugin_name}-cell
%{solr_install_dir}/docs/solr-%{plugin_name}-core
%docdir %{solr_install_dir}/docs/solr-%{plugin_name}-cell
%docdir %{solr_install_dir}/docs/solr-%{plugin_name}-core
%doc contrib/morphlines-cell/README.txt

%changelog
* Mon Jan 25 2016 Chris Beer <chris@cbeer.info> - 5.4.1-0
- Update to Solr 5.4.1

* Sat Dec 15 2015 Chris Beer <chris@cbeer.info> - 5.4.0-0
- Update to Solr 5.4.0

* Sat Sep 26 2015 Chris Beer <chris@cbeer.info> - 5.3.1-0
- Update to Solr 5.3.1

* Thu Sep 10 2015 Chris Beer <chris@cbeer.info> - 5.3.0-1
- Update to Solr 5.3.0

* Tue Jun 2 2015 Chris Beer <chris@cbeer.info> - 5.2.1-1
- Initial package