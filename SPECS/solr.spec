%define debug_package %{nil}
%define base_install_dir %{_javadir}/%{name}
%define solr_group solr
%define solr_user solr

Name:           solr
Version:        5.2.1
Release:        1%{?dist}
Summary:        A distributed, highly available, RESTful search engine

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://lucene.apache.org/solr/
Source0:        http://archive.apache.org/dist/lucene/solr/%{version}/solr-%{version}.tgz
Source1:        init.d-solr
Source2:        logrotate.d-solr
Source3:        sysconfig-solr
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       jre >= 1.7.0

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

Provides: solr

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n %{name}-%{version}

%build
true

%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir} -p %{buildroot}%{base_install_dir}/bin
%{__install} -p -m 755 bin/solr %{buildroot}%{base_install_dir}/bin
%{__install} -p -m 644 bin/solr.in.sh %{buildroot}%{base_install_dir}/bin

#libs
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/dist
%{__install} -p -m 644 dist/*.jar %{buildroot}%{base_install_dir}/dist

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server
%{__install} -p -m 644 server/*.jar %{buildroot}%{base_install_dir}/server

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/contexts
%{__install} -p -m 644 server/contexts/*.xml %{buildroot}%{base_install_dir}/server/contexts

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/etc
%{__install} -p -m 644 server/etc/*.xml %{buildroot}%{base_install_dir}/server/etc

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/lib
%{__install} -p -m 644 server/lib/*.jar %{buildroot}%{base_install_dir}/server/lib

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/lib/ext
%{__install} -p -m 644 server/lib/ext/*.jar %{buildroot}%{base_install_dir}/server/lib/ext

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/modules
%{__install} -p -m 644 server/modules/*.mod %{buildroot}%{base_install_dir}/server/modules

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/resources

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/solr-webapp

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/webapps
%{__install} -p -m 644 server/webapps/*.war %{buildroot}%{base_install_dir}/server/webapps


# config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/solr
%{__install} -p -m 644 server/solr/solr.xml %{buildroot}%{_sysconfdir}/solr
%{__install} -p -m 644 server/resources/log4j.properties %{buildroot}%{_sysconfdir}/solr
ln -sf %{_sysconfdir}/solr/log4j.properties %{buildroot}%{base_install_dir}/server/resources/log4j.properties

%{__install} -p -m 644 server/resources/jetty-logging.properties %{buildroot}%{_sysconfdir}/solr
ln -sf %{_sysconfdir}/solr/jetty-logging.properties %{buildroot}%{base_install_dir}/server/resources/jetty-logging.properties

# data
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}/lib
ln -sf %{_sysconfdir}/solr/solr.xml %{buildroot}%{_localstatedir}/lib/%{name}/solr.xml

# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/solr
ln -sf %{_localstatedir}/log/%{name} %{buildroot}%{base_install_dir}/server/logs

# plugins
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/plugins

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/solr
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/solr

%{__mkdir} -p %{buildroot}%{_localstatedir}/run/solr
%{__mkdir} -p %{buildroot}%{_localstatedir}/lock/subsys/solr

%pre
getent group %{solr_group} >/dev/null || groupadd -r %{solr_group}
getent passwd %{solr_user} >/dev/null || /usr/sbin/useradd --comment "Solr Daemon User" --shell /sbin/nologin -M -r -g %{solr_group} --home %{base_install_dir} %{solr_user}

%post
/sbin/chkconfig --add solr

%preun
if [ $1 -eq 0 ]; then
  /sbin/service solr stop >/dev/null 2>&1
  /sbin/chkconfig --del solr
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/solr
%config(noreplace) %{_sysconfdir}/sysconfig/solr
%{_sysconfdir}/logrotate.d/solr
%dir %{_javadir}/solr
%{_javadir}/solr/bin/*
%{_javadir}/solr/dist/*
%{_javadir}/solr/server/*
%dir %{_javadir}/solr/plugins
%config(noreplace) %{_sysconfdir}/solr
%doc README.txt LICENSE.txt  NOTICE.txt  CHANGES.txt docs/*
%defattr(-,solr,solr,-)
%dir %{_localstatedir}/lib/solr
%{_localstatedir}/lib/solr/solr.xml
%dir %{_localstatedir}/lib/solr/lib
%{_localstatedir}/run/solr
%dir %{_localstatedir}/log/solr
%dir %{_javadir}/solr/server/solr-webapp


%changelog

* Tue Jun 2 2015 Chris Beer <chris@cbeer.info> - 5.2.1-1
- Initial package