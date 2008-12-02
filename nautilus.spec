%define lib_major	1
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname -d %{name}

%define req_eel_version 2.25.1
%define req_gnomedesktop_version 2.1.0
%define req_librsvg_version 2.3.0
%define req_vfs_version 2.14.2

Name: nautilus
Version: 2.25.1
Release: %mkrel 1
Summary: File manager for the GNOME desktop environment
Group: File tools
License: GPLv2+
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/nautilus-%{version}.tar.bz2
Source1: nautilus_16.png
Source2: nautilus_32.png
Source3: nautilus_48.png
Patch: nautilus-2.23.4-missing-headers.patch
# (fc) 1.0.6-1mdk put default launchers on desktop according to product.id (Mandriva specific)
Patch2: nautilus-defaultdesktop.patch
# (fc) 1.0.4-4mdk merge desktop with system launcher (used for dynamic, Mandriva specific)
Patch12: nautilus-dynamic.patch
# gw from Fedora, add support for the "drag to save" protocol
# http://bugzilla.gnome.org/show_bug.cgi?id=171655
Patch15:	nautilus-2.22.0-treeview-xds-dnd.patch
# gw from Fedora, fix crash on weird file infos
# http://bugzilla.gnome.org/show_bug.cgi?id=519743
Patch17:	nautilus-filetype-symlink-fix.patch
# (fc) 2.0.5-2mdk enable tree by default, directory are listed before files, don't show files in tree
Patch22: nautilus-2.3.7-mdksettings.patch
# (fc) 2.3.9-2mdk don't show KDE specific links (CVS + me) (Mdk bug #4844)
Patch28: nautilus-kdedesktop.patch
# (fc) 2.4.0-1mdk don't colourise selected icon
Patch32: nautilus-2.17.1-colour.patch
# (fc) 2.21.92-2mdv move beagle and tracker dependency to runtime, not compile time (Fedora)
Patch33: nautilus-2.23.5-dynamic-search.patch
# (fc) 2.21.92-2mdv fix RTL build when disabling self-check (Fedora)
Patch34: nautilus-2.23.1-rtlfix.patch
# (fc) 2.22.2-2mdv auto-unmount ejected medias when mount points are in fstab (Mdv bug #39540)
Patch35: nautilus-2.22.1-umountfstab.patch

Obsoletes: gmc
Provides: gmc

Requires: drakxtools-newt >= 1.1.7-46mdk
Requires: %mklibname gvfs 0
Requires: %{lib_name} >= %{version}-%{release}
Requires: eel >= %{req_eel_version}

Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
BuildRequires: unique-devel
BuildRequires: glib2-devel >= 2.19.0
BuildRequires: eel-devel >= %{req_eel_version}
BuildRequires: gnome-desktop-devel >= %{req_gnomedesktop_version}
BuildRequires: librsvg-devel >= %{req_librsvg_version}
BuildRequires: libjpeg-devel
BuildRequires: libgnomeui2-devel > 2.5.0
BuildRequires: libORBit2-devel >= 2.9.0
BuildRequires: libcdda-devel
BuildRequires: libexif-devel >= 0.6.9
BuildRequires: exempi-devel
BuildRequires: automake1.9
BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: libgcrypt-devel
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
Requires:       eel-devel >= %{req_eel_version}
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
%patch -p1
%patch2 -p1 -b .defaultdesktop
%patch12 -p1 -b .dynamic
%patch15 -p1 -b .xds
%patch17 -p0 -b .symlink
%patch22 -p1 -b .mdksettings
%patch28 -p1 -b .kdedesktop
%patch32 -p1 -b .colour
%patch33 -p1 -b .dynamic-search
#%patch34 -p1 -b .rtl
%patch35 -p1 -b .umountfstab

%build

CFLAGS="$RPM_OPT_FLAGS -DUGLY_HACK_TO_DETECT_KDE" 
# "-DNAUTILUS_OMIT_SELF_CHECK"
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


%files -n %{develname}
%defattr(-, root, root)
%doc ChangeLog
%{_includedir}/*
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%_datadir/gtk-doc/html/libnautilus-extension
