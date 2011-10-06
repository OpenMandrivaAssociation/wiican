%define name	wiican
%define version	0.3.3
%define rel	1

%define udev_rules_dir	/lib/udev/rules.d

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	Simple Wiimote usage assistant and mapping manager
License:	GPLv3
Group:		System/Configuration/Hardware
Url:		http://fontanon.org/wiican/
Source0:	http://launchpad.net/wiican/0.3/%{version}/+download/%{name}-%{version}.tar.gz
BuildArch:	noarch
Requires:	python-dbus
Requires:	gnome-bluetooth
Requires:	pygtk2
Requires:	python-yaml
Requires:	python-pyinotify
Requires:	python-ply
Requires:	gnome-python-gconf
Requires:	python-gobject
Requires:	cwiid
Requires:	pyxdg
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils

%description
WiiCan assists on configuration and management of your Wiimote under
GNU/Linux. It tracks Bluetooth connectivity and allows to use and
create mappings to adapt your Wiimote for use on any application.

Actually WiiCan is a system tray icon, programmed in Python. It
connects to bluez and HAL via D-Bus for tracking the available
Bluetooth devices and Wiimote connection status.

%prep
%setup -q -n %{name}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install \
        --prefix=%{_prefix} \
	--root %{buildroot}

#autoload uinput module
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.preload.d
echo uinput > %{buildroot}%{_sysconfdir}/modprobe.preload.d/wiican-uinput

#fix udev-rule name
mv %{buildroot}%{udev_rules_dir}/99-uinput.rules \
   %{buildroot}%{udev_rules_dir}/99-wiican-uinput.rules

#fix desktop file
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications/ \
	--remove-category=HardwareSettings \
	--remove-key=GenericName \
	%{buildroot}%{_datadir}/applications/%{name}.desktop
	
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%post_install_gconf_schemas %{name}
set -x
/sbin/modprobe uinput &>/dev/null
:

%preun
%preun_uninstall_gconf_schemas %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS TODO
%config(noreplace) %{_sysconfdir}/modprobe.preload.d/wiican-uinput
%config(noreplace) %{_sysconfdir}/gconf/schemas/%{name}.schemas
%{python_sitelib}/%{name}-%{version}-py%{py_ver}.egg-info
%{python_sitelib}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}-service
%{udev_rules_dir}/99-wiican-uinput.rules
%{_iconsdir}/hicolor/*/*/%{name}*
%{_iconsdir}/hicolor/scalable/mimetypes/gnome-mime-application-x-wii.svg
%{_datadir}/dbus-1/services/org.gnome.wiican.service
%{_datadir}/mime/packages/wiican.xml
