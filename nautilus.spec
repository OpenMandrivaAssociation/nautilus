%define lib_major	1
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname -d %{name}

Name: nautilus
Version: 2.32.2.1
Release: 5
Summary: File manager for the GNOME desktop environment
Group: File tools
License: GPLv2+
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/nautilus-%{version}.tar.bz2
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

BuildRequires: glib2-devel >= 2.25.9
BuildRequires: gnome-desktop-devel >= 2.29.9
BuildRequires: librsvg-devel >= 2.3.0
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
Obsoletes: gmc
Provides: gmc
Obsoletes: gnome-volume-manager
Provides: gnome-volume-manager
Requires: %mklibname gvfs 0
Requires: %{lib_name} >= %{version}-%{release}
Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils

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
Obsoletes:		%{lib_name}-devel
Provides:		%{name}-devel = %{version}
Conflicts:		%{_lib}nautilus0-devel
Conflicts:		%{_lib}nautilus2-devel

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop nautilus components.

%prep
rm -rf %{buildroot}

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
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
find %{buildroot}%{_libdir} -name '*.la' -type f -delete -print

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome/desktop \
 %{buildroot}%{_datadir}/nautilus/default-desktop

mkdir -p %{buildroot}%{_libdir}/nautilus/extensions-2.0

%{find_lang} %{name} --with-gnome --all-name

%preun
%preun_uninstall_gconf_schemas apps_nautilus_preferences

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
%{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas
%dir %{_localstatedir}/lib/gnome/desktop
%dir %{_localstatedir}/lib/gnome/
%{_bindir}/*
%_libexecdir/nautilus-convert-metadata
%_mandir/man1/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/nautilus
%{_iconsdir}/hicolor/*/apps/nautilus.*
%_datadir/mime/packages/nautilus.xml
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-2.0

%files -n %{lib_name}
%{_libdir}/libnautilus*.so.%{lib_major}*
%_libdir/girepository-1.0/Nautilus-2.0.typelib

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%_datadir/gtk-doc/html/libnautilus-extension
%_datadir/gir-1.0/Nautilus-2.0.gir

