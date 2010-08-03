%define upstream_name		wiican
%define upstream_version	0.2.1

Name:		%{upstream_name}
Version:	%{upstream_version}
Release:	%mkrel 1
Summary:	Simple wiimote usage assistant and mapping manager
License:	GPL
Group:		Development/Perl
Url:		http://kolab.org/cgi-bin/viewcvs-kolab.cgi/server/perl-kolab/
Source0:	%{name}-%{version}.tar.gz

Provides:	wiican = %{upstream_version}
Obsoletes:	wiican < %{upstream_version}
Requires:	Python >= 2.5
Requires:	dbus-python
Requires:	PyGTK
Requires:	PyYAML
Requires:	PyINotify
Requires:	gnome-bluetooth
BuildArch:	noarch




%description
Wiican it's a user-friendly systray application for use
and configure wiimote (or Wii remote controller).
On backend it's wminput, the cwiid event driver for wiimote.

It tracks if the needed bluetooth adapter it's available and drives
the user into the process of connect/disconnect wiimote

A mapping manager it's supplied for edit and create  multiple wiimote
configurations.

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


#install -d $RPM_BUILD_ROOT{%{_bindir}/,%{_datadir}/%{name}/,%{_datadir}/pyshared/wiican/,%{_datadir}/wiican}/,%{_initrddir}/,%{_datadir}/locale/}
#install -d $RPM_BUILD_ROOT{%{_datadir}/locale/es/,%{_datadir}/locale/es/LC_MESSAGES/,%{_datadir}/doc/wiican/,%{_datadir}/python-support/}
#install -d $RPM_BUILD_ROOT{%{_datadir}/wiican/config_skel/,%{_datadir}/pixmaps/,%{_datadir}/pyshared/,%{_datadir}/wiican/,%{_datadir}/wiican/img/,%{_datadir}/pyshared/wiican/}
#install bin/%{name} $RPM_BUILD_ROOT%{_bindir}/wiican
#install usr/share/wiican/img/*.* $RPM_BUILD_ROOT%{_datadir}/*.*
#install sounds/*.wav $RPM_BUILD_ROOT%{_datadir}/%{name}/sounds


#install %{name}.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%files
%defattr(644,root,root,755)
%doc LICENSE
#%doc README
%attr(755,root,root) %{_bindir}
%dir %{_datadir}/%{name}
%dir %_prefix/lib/
%attr(0744,root,root)%{_bindir}/wiican
%attr(0755,root,root)%python_sitelib/wiican-0.2.1-py2.6.egg-info
%attr(0755,root,root)%python_sitelib/wiican/__init__.py
%attr(0755,root,root)%python_sitelib/wiican/defs.py
%attr(0755,root,root)%python_sitelib/wiican/dotconfig.py
%attr(0755,root,root)%python_sitelib/wiican/mapping.py
%attr(0755,root,root)%python_sitelib/wiican/notificator.py
%attr(0755,root,root)%python_sitelib/wiican/pnganimation.py
%attr(0755,root,root)%python_sitelib/wiican/wiimotemanager.py
%attr(0755,root,root)%{_datadir}/applications/wiican.desktop
%attr(0755,root,root)%{_datadir}/pixmaps/wiican.svg
%attr(0755,root,root)%{_datadir}/wiican/about.ui
%attr(0755,root,root)%{_datadir}/wiican/config_skel/mouse.wminput
%attr(0755,root,root)%{_datadir}/wiican/config_skel/neverball.wminput
%attr(0755,root,root)%{_datadir}/wiican/entry.ui
%attr(0755,root,root)%{_datadir}/wiican/img/wiitrayoff.svg
%attr(0755,root,root)%{_datadir}/wiican/img/wiitrayon.svg
%attr(0755,root,root)%{_datadir}/wiican/img/wiitrayon1.svg
%attr(0755,root,root)%{_datadir}/wiican/img/wiitrayon2.svg
%attr(0755,root,root)%{_datadir}/wiican/img/wiitrayon3.svg
%attr(0755,root,root)%{_datadir}/wiican/mapping.ui
%attr(0755,root,root)%{_datadir}/wiican/wiican.svg
