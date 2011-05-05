%define lib_major	1
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname -d %{name}

%define req_gnomedesktop_version 2.29.91
%define req_librsvg_version 2.3.0
%define req_vfs_version 2.14.2

Name: nautilus
Version: 2.32.2.1
Release: %mkrel 2
Summary: File manager for the GNOME desktop environment
Group: File tools
License: GPLv2+
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/nautilus-%{version}.tar.bz2
Source1: nautilus_16.png
Source2: nautilus_32.png
Source3: nautilus_48.png
# (fc) 1.0.6-1mdk put default launchers on desktop according to product.id (Mandriva specific)
Patch2: nautilus-defaultdesktop.patch
# (fc) 1.0.4-4mdk merge desktop with system launcher (used for dynamic, Mandriva specific)
Patch12: nautilus-dynamic.patch
# gw from Fedora, fix crash on weird file infos
# http://bugzilla.gnome.org/show_bug.cgi?id=519743
Patch17:	nautilus-filetype-symlink-fix.patch
# (fc) 2.3.9-2mdk don't show KDE specific links (CVS + me) (Mdk bug #4844)
Patch28: nautilus-kdedesktop.patch
# (fc) 2.4.0-1mdk don't colourise selected icon
Patch32: nautilus-2.29.92-colour.patch
# (fc) 2.21.92-2mdv fix RTL build when disabling self-check (Fedora)
Patch34: nautilus-2.26.0-rtlfix.patch
# (fc) 2.22.2-2mdv auto-unmount ejected medias when mount points are in fstab (Mdv bug #39540)
Patch35: nautilus-2.25.91-umountfstab.patch
# (fc) 2.26.0-2mdv allow to lockdown context menu (Novell bug #363122) (SUSE)
Patch36: nautilus-bnc363122-lockdown-context-menus.diff
# (fc) 2.26.0-2mdv add a search .desktop file (GNOME bug #350950) (SUSE)
Patch37: nautilus-bgo350950-search-desktop.diff
# (fc) 2.27.91-2mdv fix infinite startup when show_desktop is disabled (Fedora)
Patch39: nautilus-condrestart.patch

Obsoletes: gmc
Provides: gmc

Obsoletes: gnome-volume-manager
Provides: gnome-volume-manager

Requires: %mklibname gvfs 0
Requires: %{lib_name} >= %{version}-%{release}

Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
BuildRequires: glib2-devel >= 2.25.9
BuildRequires: gnome-desktop-devel >= %{req_gnomedesktop_version}
BuildRequires: librsvg-devel >= %{req_librsvg_version}
BuildRequires: libjpeg-devel
BuildRequires: libice-devel
BuildRequires: libsm-devel
BuildRequires: libx11-devel
BuildRequires: GConf2
BuildRequires: libORBit2-devel >= 2.9.0
BuildRequires: libcdda-devel
BuildRequires: libxrender-devel
BuildRequires: libexif-devel >= 0.6.9
BuildRequires: exempi-devel
BuildRequires: unique-devel
BuildRequires: automake1.9
BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: libgcrypt-devel
BuildRequires: libgail-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc
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

%package -n %{develname}
Summary:        Libraries and include files for developing nautilus components
Group:          Development/GNOME and GTK+
Requires:       %name = %{version}
Requires:		%{lib_name} = %{version}
Requires:       librsvg-devel >= %{req_librsvg_version}
Obsoletes:		%{name}-devel
Obsoletes:		%{lib_name}-devel
Provides:		%{name}-devel = %{version}
Provides:		lib%{name}-devel = %{version}
Conflicts:		%{_lib}nautilus0-devel
Conflicts:		%{_lib}nautilus2-devel

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop nautilus components.

BuildRoot:%{_tmppath}/%{name}-%{version}-root

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch2 -p1 -b .defaultdesktop
%patch12 -p1 -b .dynamic
%patch17 -p0 -b .symlink
%patch28 -p1 -b .kdedesktop
%patch32 -p1 -b .colour
%patch34 -p1 -b .rtlfix
%patch35 -p1 -b .umountfstab
%patch36 -p1 -b .lockdown-contextmenus
%patch37 -p1 -b .search-desktop
%patch39 -p1 -b .condrestart

#needed by patch37
libtoolize --force
aclocal -I m4
gtkdocize
autoconf
automake
#autoreconf

%build

CFLAGS="$RPM_OPT_FLAGS -DUGLY_HACK_TO_DETECT_KDE" 
%configure2_5x --disable-update-mimedb

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

mkdir -p  $RPM_BUILD_ROOT%{_miconsdir} $RPM_BUILD_ROOT%{_liconsdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_miconsdir}/nautilus.png
cp %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/nautilus.png
cp %{SOURCE3} $RPM_BUILD_ROOT%{_liconsdir}/nautilus.png

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/gnome/desktop \
 $RPM_BUILD_ROOT%{_datadir}/nautilus/default-desktop

mkdir -p $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0

%{find_lang} %{name} --with-gnome --all-name

%if %mdkversion < 200900
%post
%{update_menus}
%post_install_gconf_schemas apps_nautilus_preferences
%update_mime_database
%update_desktop_database
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas apps_nautilus_preferences

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_mime_database
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS HACKING AUTHORS MAINTAINERS
%{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas
%dir %{_localstatedir}/lib/gnome/desktop
%dir %{_localstatedir}/lib/gnome/
%{_bindir}/*
%_libexecdir/nautilus-convert-metadata
%_mandir/man1/*
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/nautilus
%{_iconsdir}/hicolor/*/apps/nautilus.*
%_datadir/mime/packages/nautilus.xml
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-2.0

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/libnautilus*.so.%{lib_major}*
%_libdir/girepository-1.0/Nautilus-2.0.typelib

%files -n %{develname}
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%_datadir/gtk-doc/html/libnautilus-extension
%_datadir/gir-1.0/Nautilus-2.0.gir
