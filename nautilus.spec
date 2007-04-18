%define lib_major	1
%define lib_name	%mklibname %{name} %{lib_major}

%define req_eel_version 2.15.91
%define req_gnomedesktop_version 2.1.0
%define req_librsvg_version 2.3.0
%define req_vfs_version 2.14.2

Name: nautilus
Version: 2.18.1
Release: %mkrel 3
Summary: Nautilus is a file manager for the GNOME desktop environment
Group: File tools
License: GPL
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/nautilus-%{version}.tar.bz2
Source1: nautilus_16.png
Source2: nautilus_32.png
Source3: nautilus_48.png
Source4: emblem-shared.svg.bz2
# (fc) 1.0.6-1mdk new default desktop initialization
Patch2: nautilus-2.18.0-defaultdesktop.patch
# (fc) 1.0.4-4mdk merged desktop with system desktop
Patch12: nautilus-2.5.1-dynamic.patch
# (fc) 2.0.5-2mdk enable tree by default, directory are listed before files, don't show files in tree
Patch22: nautilus-2.3.7-mdksettings.patch
# (fc) 2.3.9-2mdk don't show KDE specific links (CVS + me) (Mdk bug #4844)
Patch28: nautilus-2.10.1-kdedesktop.patch
# (fc) 2.3.9-3mdk allow editing .desktop files everywhere
Patch31: nautilus-2.9.1-editdesktop.patch
# (fc) 2.4.0-1mdk don't colourise selected icon
Patch32: nautilus-2.17.1-colour.patch
# (fc) 2.8.2-7mdk don't monitor supermount devices (Mdk bug #14880)
Patch36: nautilus-2.8.2-supermount.patch
# (fc) 2.10.1-8mdk don't check sound server status to allow audio preview
Patch39: nautilus-2.10.1-audiopreview.patch
# (fc) 2.12.2-5mdk add support for .desktop in gtk bookmarks
Patch40: nautilus-2.15.2-desktopitem.patch

BuildRoot:%{_tmppath}/%{name}-%{version}-root

Obsoletes: gmc
Provides: gmc

Requires: mpg123
Requires: vorbis-tools
Requires: sox
Requires: drakxtools-newt >= 1.1.7-46mdk
# needed for dynamic desktop
Requires: gnome-vfs2 >= %{req_vfs_version}
Requires: %{lib_name} >= %{version}-%{release}
Requires: eel >= %{req_eel_version}

Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
BuildRequires: eel-devel >= %{req_eel_version}
BuildRequires: gnome-desktop-devel >= %{req_gnomedesktop_version}
BuildRequires: gnome-vfs2-devel >= %{req_vfs_version}
BuildRequires: librsvg-devel >= %{req_librsvg_version}
BuildRequires: libjpeg-devel
BuildRequires: libgnomeui2-devel > 2.5.0
BuildRequires: libORBit2-devel >= 2.9.0
BuildRequires: libcdda-devel
BuildRequires: libexif-devel >= 0.6.9
BuildRequires: libbeagle-devel
BuildRequires: perl-XML-Parser
BuildRequires: automake1.9
BuildRequires: intltool
BuildRequires: desktop-file-utils
Obsoletes: nautilus-trilobite
Provides: nautilus-trilobite = %{version}

%description
Nautilus is an excellent file manager for the GNOME desktop environment.

%package -n %{lib_name}
Summary:        Libraries for Nautilus File manager
Group:          System/Libraries
Conflicts:	%{_lib}nautilus2

%description -n %{lib_name}
Nautilus is an excellent file manager for the GNOME desktop environment.
This package contains libraries used by Nautilus.

%package -n %{lib_name}-devel
Summary:        Libraries and include files for developing nautilus components
Group:          Development/GNOME and GTK+
Requires:       %name = %{version}
Requires:		%{lib_name} = %{version}
Requires:       eel-devel >= %{req_eel_version}
Requires:       librsvg-devel >= %{req_librsvg_version}
Obsoletes:		%{name}-devel
Provides:		%{name}-devel = %{version}
Provides:		lib%{name}-devel = %{version}
Conflicts:		%{_lib}nautilus0-devel
Conflicts:		%{_lib}nautilus2-devel

%description -n %{lib_name}-devel
This package provides the necessary development libraries and include 
files to allow you to develop nautilus components.


%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch12 -p1 -b .dynamic
%patch2  -p1 -b .defaultdesktop
%patch22 -p1 -b .mdksettings
%patch28 -p1 -b .kdedesktop
%patch31 -p1 -b .editdesktop
%patch32 -p1 -b .colour
%patch36 -p1 -b .supermount
%patch39 -p1 -b .audiopreview
%patch40 -p1 -b .desktopitem

#fix build
aclocal-1.9
automake-1.9
autoconf

%build

CFLAGS="$RPM_OPT_FLAGS -DUGLY_HACK_TO_DETECT_KDE" %configure2_5x --disable-update-mimedb

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

pushd $RPM_BUILD_ROOT%{_datadir}/pixmaps/nautilus
bzcat %{SOURCE5} | tar xf -
popd

mkdir -p $RPM_BUILD_ROOT%{_menudir}

cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_bindir}/%{name} --no-desktop" \
needs="x11" section="System/File Tools" title="Nautilus" \
longtitle="Nautilus - GNOME file manager" icon="%{name}.png" xdg="true"
?package(%{name}):command="%{_bindir}/nautilus-file-management-properties" \
needs="gnome" section="System/Configuration/GNOME" longtitle="Change how files are managed" \
title="File Management" icon="gnome-fs-directory.png" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-FileTools" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/nautilus.desktop
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration-GNOME" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/nautilus-file-management-properties.desktop


mkdir -p  $RPM_BUILD_ROOT%{_miconsdir} $RPM_BUILD_ROOT%{_liconsdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_miconsdir}/nautilus.png
cp %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/nautilus.png
cp %{SOURCE3} $RPM_BUILD_ROOT%{_liconsdir}/nautilus.png

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/gnome/desktop \
 $RPM_BUILD_ROOT%{_datadir}/nautilus/default-desktop

mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/gnome/scalable/emblems
bzcat %{SOURCE4} > $RPM_BUILD_ROOT%{_iconsdir}/gnome/scalable/emblems/emblem-shared.svg

mkdir -p $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0

%{find_lang} %{name} --with-gnome --all-name

%post
%{update_menus}
%post_install_gconf_schemas apps_nautilus_preferences
%update_mime_database
%update_desktop_database
%update_icon_cache hicolor
%update_icon_cache gnome

%preun
%preun_uninstall_gconf_schemas apps_nautilus_preferences

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%postun
%{clean_menus}
%clean_mime_database
%clean_desktop_database
%clean_icon_cache hicolor
%clean_icon_cache gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS HACKING AUTHORS MAINTAINERS
%{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas
%dir %{_localstatedir}/gnome/desktop
%dir %{_localstatedir}/gnome/
%{_bindir}/*
%{_menudir}/*
%{_libdir}/bonobo/servers/*
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/nautilus
%{_iconsdir}/hicolor/*/apps/nautilus.*
%{_iconsdir}/gnome/scalable/emblems/emblem-shared.svg
%_datadir/mime/packages/nautilus.xml
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-1.0

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/libnautilus*.so.%{lib_major}*


%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
