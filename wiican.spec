%define name	wiican
%define version	0.2.1
%define rel	1

%define udev_rules_dir	/lib/udev/rules.d

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Summary:	Simple wiimote usage assistant and mapping manager
License:	GPLv3
Group:		System/Configuration/Hardware
Url:		http://fontanon.org/wiican/
Source0:	http://launchpad.net/wiican/0.2/%{version}/+download/%{name}-%{version}.tar.gz
BuildArch:	noarch
Requires:	python-dbus
Requires:	gnome-bluetooth
Requires:	pygtk2
Requires:	python-yaml
Requires:	python-pyinotify
Requires:	cwiid
%py_requires -d

%description
WiiCan assists on configuration and management of your wiimote under
GNU/Linux. It tracks bluetooth connectivity and allows to use and
create mappings to adapt your wiimote for use on any application.

Actually WiiCan is a sytem tray icon, programmed in python. It
connects to bluez and hal via dbus for tracking the available
bluetooth devices and wiimote connection status.

%prep
%setup -q

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
install -m0644 udev-rules/45-uinput.rules %{buildroot}%{udev_rules_dir}/51-wiican-uinput.rules

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS TODO
%{python_sitelib}/%{name}-%{version}-py%{py_ver}.egg-info
%{python_sitelib}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/%{name}
%{_bindir}/%{name}
%{udev_rules_dir}/51-wiican-uinput.rules
%config(noreplace) %{_sysconfdir}/modprobe.preload.d/wiican-uinput
