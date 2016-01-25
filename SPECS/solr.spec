%define debug_package %{nil}
%define base_install_dir %{_javadir}/%{name}
%define solr_group solr
%define solr_user solr

Name:           solr
Version:        5.4.1
Release:        0%{?dist}
Summary:        A distributed, highly available, RESTful search engine

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://lucene.apache.org/solr/
Source0:        http://archive.apache.org/dist/lucene/solr/%{version}/solr-%{version}.tgz
Source1:        init.d-solr
Source2:        logrotate.d-solr
Source3:        sysconfig-solr
Patch0:         solr.xml.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       jpackage-utils
Requires:       jre >= 1.7.0
Requires:       lsof

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

Provides: solr

%description
A distributed, highly available, RESTful search engine

%prep
%setup -q -n %{name}-%{version}

%patch0 -p0

%build
true

%install
rm -rf $RPM_BUILD_ROOT

#bin
%{__mkdir} -p %{buildroot}%{base_install_dir}/bin
%{__install} -p -m 755 bin/oom_solr.sh %{buildroot}%{base_install_dir}/bin
%{__install} -p -m 755 bin/post %{buildroot}%{base_install_dir}/bin
%{__install} -p -m 755 bin/solr %{buildroot}%{base_install_dir}/bin
%{__install} -p -m 644 bin/solr.in.sh %{buildroot}%{base_install_dir}/bin

# contrib
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/contrib

# licenses
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/licenses
%{__install} -p -m 644 licenses/* %{buildroot}%{base_install_dir}/licenses

#libs
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/dist
%{__install} -p -m 644 dist/solr-analytics-*.jar %{buildroot}%{base_install_dir}/dist
%{__install} -p -m 644 dist/solr-cell-*.jar %{buildroot}%{base_install_dir}/dist
%{__install} -p -m 644 dist/solr-dataimporthandler-%{version}.jar %{buildroot}%{base_install_dir}/dist
%{__install} -p -m 644 dist/solr-core-*.jar %{buildroot}%{base_install_dir}/dist

# server libs
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

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/scripts/cloud-scripts
%{__install} -p -m 755 server/scripts/cloud-scripts/* %{buildroot}%{base_install_dir}/server/scripts/cloud-scripts

# webapp

%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/server/solr-webapp/webapp
%{__cp} -R -p server/solr-webapp/webapp/* %{buildroot}%{base_install_dir}/server/solr-webapp/webapp

# config
%{__mkdir} -p %{buildroot}%{_sysconfdir}/solr
%{__install} -p -m 644 server/solr/README.txt %{buildroot}%{_sysconfdir}/solr
%{__install} -p -m 644 server/solr/solr.xml %{buildroot}%{_sysconfdir}/solr
%{__install} -p -m 644 server/solr/zoo.cfg %{buildroot}%{_sysconfdir}/solr
%{__install} -p -m 644 server/resources/log4j.properties %{buildroot}%{_sysconfdir}/solr
ln -sf %{_sysconfdir}/solr/log4j.properties %{buildroot}%{base_install_dir}/server/resources/log4j.properties

%{__install} -p -m 644 server/resources/jetty-logging.properties %{buildroot}%{_sysconfdir}/solr
ln -sf %{_sysconfdir}/solr/jetty-logging.properties %{buildroot}%{base_install_dir}/server/resources/jetty-logging.properties

# docs
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/docs/solr-core
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/docs/images
%{__mkdir} -p %{buildroot}%{_javadir}/%{name}/docs/changes
%{__install} -p -m 644 docs/*.html %{buildroot}%{base_install_dir}/docs
%{__install} -p -m 644 docs/images/* %{buildroot}%{base_install_dir}/docs/images
%{__install} -p -m 644 docs/changes/* %{buildroot}%{base_install_dir}/docs/changes
%{__cp} -R -p docs/solr-core/* %{buildroot}%{base_install_dir}/docs/solr-core

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
%{_javadir}/solr/docs/*
%docdir %{solr_install_dir}/docs/solr-core
%{_javadir}/solr/licenses/*
%docdir %{solr_install_dir}/licenses
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
