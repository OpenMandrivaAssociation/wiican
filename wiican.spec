%define name	wiican
%define version	0.3.0
%define rel	2

%define udev_rules_dir	/lib/udev/rules.d

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	Simple Wiimote usage assistant and mapping manager
License:	GPLv3
Group:		System/Configuration/Hardware
Url:		http://fontanon.org/wiican/
Source0:	http://launchpad.net/wiican/0.2/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:		wiican-0.3.0-fix_prefixdir.patch
Patch1:		wiican-0.3.0-utils_keynone.patch
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
BuildRequires:	desktop-file-utils
%py_requires -d

%description
WiiCan assists on configuration and management of your Wiimote under
GNU/Linux. It tracks Bluetooth connectivity and allows to use and
create mappings to adapt your Wiimote for use on any application.

Actually WiiCan is a system tray icon, programmed in Python. It
connects to bluez and HAL via D-Bus for tracking the available
Bluetooth devices and Wiimote connection status.

%prep
%setup -q
%patch0
%patch1

#fix prefix
sed -i -e 's,@MDV_PREFIX@,%{_prefix},' setup.py

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --root %{buildroot}

#autoload uinput module
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.preload.d
echo uinput > %{buildroot}%{_sysconfdir}/modprobe.preload.d/wiican-uinput

#udev-rule, change priority to override system default setting
mkdir -p %{buildroot}%{udev_rules_dir}
install -m0644 udev-rules/99-uinput-rules %{buildroot}%{udev_rules_dir}/99-wiican-uinput.rules

#fix desktop file
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications/ \
	--remove-category=HardwareSettings \
	--remove-key=GenericName \
	%{buildroot}%{_datadir}/applications/%{name}.desktop
	
#gconf schema
install -D -m0644 wiican.schemas %{buildroot}%{_sysconfdir}/gconf/schemas/%{name}.schemas

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
%{_datadir}/dbus-1/services/org.gnome.wiican.service
