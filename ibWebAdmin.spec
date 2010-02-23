Summary:        Adminstration of Firebird over the web
Name:           ibWebAdmin
Version:        1.0.2
Release:        %mkrel 7
License:        GPL
Group:          System/Servers
URL:            http://www.ibwebadmin.net/
Source0:        http://ufpr.dl.sourceforge.net/sourceforge/ibwebadmin/ibWebAdmin_%{version}.tar.gz
Source1:	configuration.inc.php
Requires:       apache-mod_php
Requires:       php-mysql
Requires:       php-mbstring
Requires:       php-mcrypt
Requires(post): ccp >= 0.4.0
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
%if %mdkversion < 200900
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
%endif
Requires:       firebird-server
Requires:       php-firebird
BuildRequires:  imagemagick
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}

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
rm -rf %{buildroot}

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
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/01_%{name}.conf"
</Directory>

<Directory /var/www/%{name}/inc>
    Order deny,allow
    Deny from all
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

%if %mdkversion < 201010
%_post_webapp
%endif
%if %mdkversion < 200900
%update_menus
%update_desktop_database
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif
%if %mdkversion < 200900
%clean_menus
%clean_desktop_database
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc LICENSE NEWS README
%dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/configuration.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/var/www/%{name}
%{_datadir}/applications/*.desktop
