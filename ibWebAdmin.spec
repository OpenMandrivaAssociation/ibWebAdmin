Summary:        ibWebAdmin is intended to handle the adminstration of Firebird over the web
Name:           ibWebAdmin
Version:        1.0.2
Release:        %mkrel 3
License:        GPL
Group:          System/Servers
URL:            http://www.ibwebadmin.net/
Source0:        http://ufpr.dl.sourceforge.net/sourceforge/ibwebadmin/ibWebAdmin_%{version}.tar.gz
Source1:	configuration.inc.php
Requires(pre):  apache-mod_php php-mysql php-mbstring php-mcrypt
Requires:       apache-mod_php php-mysql php-mbstring php-mcrypt
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post): rpm-helper
Requires(postun): rpm-helper
BuildArch:      noarch
BuildRequires:  ImageMagick
BuildRequires:  apache-base >= 2.0.54
Requires(post): ccp >= 0.4.0
Requires:       firebird-server
Requires:       php-firebird
BuildRoot:      %{_tmppath}/%{name}-buildroot

%description
phpMyAdmin is intended to handle the adminstration of MySQL over
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

<IfModule mod_php4.c>
    php_flag session.auto_start 0
</IfModule>

<IfModule mod_php5.c>
    php_flag session.auto_start 0
</IfModule>

<Directory /var/www/%{name}>
    Allow from All
</Directory>

<Directory /var/www/%{name}/inc>
    Order Deny,Allow
    Deny from All
    Allow from None
</Directory>

# Uncomment the following lines to force a redirect to a working 
# SSL aware apache server. This serves as an example.
# 
#<IfModule mod_ssl.c>
#    <LocationMatch /%{name}>
#        Options FollowSymLinks
#        RewriteEngine on
#        RewriteCond %{SERVER_PORT} !^443$
#        RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
#    </LocationMatch>
#</IfModule>
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

%_post_webapp
%update_menus
%update_desktop_database

%postun
%_postun_webapp
%clean_menus
%clean_desktop_database

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc LICENSE NEWS README
%dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/configuration.inc.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/var/www/%{name}
%{_datadir}/applications/*.desktop
