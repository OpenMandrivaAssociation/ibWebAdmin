Summary:        Adminstration of Firebird over the web
Name:           ibWebAdmin
Version:        1.0.2
Release:        12
License:        GPL
Group:          System/Servers
URL:            http://www.ibwebadmin.net/
Source0:        http://ufpr.dl.sourceforge.net/sourceforge/ibwebadmin/ibWebAdmin_%{version}.tar.gz
Source1:	configuration.inc.php
Requires:       apache-mod_php
Requires:       php-mysql
Requires:       php-mbstring
Requires:	apache-mod_socache_shmcb
Requires:       php-mcrypt
Requires(post): ccp >= 0.4.0
Requires:       firebird-server
Requires:       php-firebird
BuildRequires:  imagemagick
BuildArch:      noarch

%description
phpMyAdmin is intended to handle the adminstration of Firebird over
the web. Currently it can : create and drop databases, create,
copy, drop and alter tables, delete, edit and add fields, execute
any SQL-statement, even batch-queries, manage keys on fields, load
text files into tables, create and read dumps of tables, export
data to CSV value, administer multiple servers and single
databases.

%prep
%setup -q -n %{name}_%{version}
cp -f %{SOURCE1} %{_builddir}/%{name}_%{version}/inc/configuration.inc.php

%build

%install
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}

cp -aRf * %{buildroot}/var/www/%{name}/

# cleanup
pushd %{buildroot}/var/www/%{name}
    rm -f change_cvs.sh LICENSE Makefile NEWS README
popd

# fix config file location
mv %{buildroot}/var/www/%{name}/inc/configuration.inc.php %{buildroot}%{_sysconfdir}/%{name}/
ln -s %{_sysconfdir}/%{name}/configuration.inc.php %{buildroot}/var/www/%{name}/inc/configuration.inc.php

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF
Alias /%{name} /var/www/%{name}

php_flag session.auto_start 0

<Directory /var/www/%{name}>
    Require host 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/01_%{name}.conf"
</Directory>

<Directory /var/www/%{name}/inc>
    Require all denied
</Directory>
EOF

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=ibWebAdmin
Comment=%{summary}
Exec="%{_bindir}/www-browser http://localhost/%{name}/"
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Databases;
EOF

%post
ccp --delete --ifexists --set "NoOrphans" --ignoreopt VERSION \
	--oldfile %{_sysconfdir}/%{name}/configuration.inc.php \
	--newfile %{_sysconfdir}/%{name}/configuration.inc.php.rpmnew

%clean

%files
%defattr(-,root,root,0755)
%doc LICENSE NEWS README
%dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/configuration.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/var/www/%{name}
%{_datadir}/applications/*.desktop


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-8mdv2011.0
+ Revision: 611168
- rebuild

* Tue Feb 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.2-7mdv2010.1
+ Revision: 510423
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- switch to "localhost access only" default access policy

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.0.2-7mdv2010.0
+ Revision: 429489
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.0.2-6mdv2009.0
+ Revision: 247147
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 1.0.2-4mdv2008.1
+ Revision: 168498
- rebuild
- fix description
- fix summary
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Sep 11 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.0.2-3mdv2008.0
+ Revision: 84402
- Do not force superserver, as noticed by Philippe Makowski.

* Tue May 15 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.0.2-2mdv2008.0
+ Revision: 26993
- Fix URL tag.


* Mon Nov 27 2006 Marcelo Ricardo Leitner <mrl@mandriva.com> 1.0.2-1mdv2007.0
+ Revision: 87363
- Import ibWebAdmin

