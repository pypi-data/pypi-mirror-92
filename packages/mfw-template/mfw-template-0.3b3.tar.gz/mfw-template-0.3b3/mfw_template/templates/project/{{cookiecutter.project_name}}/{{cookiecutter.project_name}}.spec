%define debug_package %{nil}
%define _build_id_links none
%define service_user {{ cookiecutter.project_name }}

Name:       {{ cookiecutter.project_name }}
Version:    {{ cookiecutter.version }}
Release:    1%{?dist}
Summary:    {{ cookiecutter.project_name }}

License:    {{ cookiecutter.license }}
URL:        {{ cookiecutter.project_url }}
AutoReqProv: no
Source0:    %{name}.tar.bz2
Source6:    web.service
Source9:    worker.service
Source10:   scheduler.service
Source12:   settings.yml
Source13:   logrotate.conf
BuildRequires:  python(abi) >= 3.7
BuildRequires: pkgconfig(python) >= 3.7
Requires: python(abi) >= 3.7
Requires: pkgconfig(python) >= 3.7

BuildRequires:    postgresql-devel
Requires:   postgresql-libs postgresql 
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel

%description
{{ cookiecutter.project_name }}

%prep
rm -rf %{_builddir}/%{name}/
%setup -q -b 0 -n %{name}

%build
rm -rf $RPM_BUILD_ROOT

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/%{name}/
cp -r * ${RPM_BUILD_ROOT}/opt/%{name}/
cp .mr.developer.cfg .mfwtemplaterc ${RPM_BUILD_ROOT}/opt/%{name}/
cd ${RPM_BUILD_ROOT}/opt/%{name}/
./build.sh -c buildout-rpm.cfg

# create resource dirs
mkdir -p ${RPM_BUILD_ROOT}/var/log/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}/blobstorage
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d/
mkdir -p ${RPM_BUILD_ROOT}/etc/%{name}/
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/

# settings file
cp %{SOURCE12} ${RPM_BUILD_ROOT}/etc/%{name}/settings.yml
sed -i "s|fsblob://\%%(here)s/blobstorage|fsblob:///var/lib/%{name}/blobstorage|g" ${RPM_BUILD_ROOT}/etc/%{name}/settings.yml

# logrotate config
cp %{SOURCE13} ${RPM_BUILD_ROOT}/etc/logrotate.d/%{name}

# systemd config
cp %{SOURCE6} ${RPM_BUILD_ROOT}/usr/lib/systemd/system/%{name}-web.service
cp %{SOURCE9} ${RPM_BUILD_ROOT}/usr/lib/systemd/system/%{name}-worker.service
cp %{SOURCE10} ${RPM_BUILD_ROOT}/usr/lib/systemd/system/%{name}-scheduler.service

# strip rpmbuildroot paths
grep -lrZF "#!$RPM_BUILD_ROOT" $RPM_BUILD_ROOT | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
find $RPM_BUILD_ROOT -type f -regex '.*egg-link$' |xargs -I% grep -lrZF "$RPM_BUILD_ROOT" % | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/opt/%{name}/bin/ | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"
grep -lrZF "$RPM_BUILD_ROOT" $RPM_BUILD_ROOT/opt/%{name}/venv/bin/ | xargs -r -0 perl -p -i -e "s|$RPM_BUILD_ROOT||g"

# cleanup
rm ${RPM_BUILD_ROOT}/opt/%{name}/.installed.cfg
find ${RPM_BUILD_ROOT} -regex '.*\.pyc$' -exec rm '{}' ';'
find ${RPM_BUILD_ROOT} -regex '.*\.pyo$' -exec rm '{}' ';'


%post
/opt/%{name}/venv/bin/python -m compileall -q /opt/%{name}/ > /dev/null 2>&1 
/usr/bin/systemctl daemon-reload

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{service_user} >/dev/null || /usr/sbin/groupadd -r %{service_user}
/usr/bin/getent passwd %{service_user} >/dev/null || /usr/sbin/useradd -r \
     -g %{service_user} -d /opt/%{name}/ -s /sbin/nologin %{service_user}

%files
%defattr(644, %{service_user},%{service_user},755)
/opt/%{name}/
%attr(755, %{service_user},%{service_user}) /opt/%{name}/bin/*
%attr(755, %{service_user},%{service_user}) /opt/%{name}/venv/bin/*
%config /etc/%{name}/settings.yml
%attr(-,root,root) /usr/lib/systemd/system/%{name}-web.service
%attr(-,root,root) /usr/lib/systemd/system/%{name}-scheduler.service
%attr(-,root,root) /usr/lib/systemd/system/%{name}-worker.service
%attr(755,%{service_user},%{service_user}) /var/log/%{name}
%attr(755,%{service_user},%{service_user}) /var/lib/%{name}
%attr(755,%{service_user},%{service_user}) /var/lib/%{name}/blobstorage

%attr(-,root,root) /etc/logrotate.d/%{name}

%changelog

* {{ cookiecutter.rpm_date }} {{ cookiecutter.author_name }} {{ cookiecutter.version }}
- initial package
