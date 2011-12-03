%define lib_major	1
%define gir_major	3.0
%define lib_name	%mklibname %{name} %{lib_major}
%define girname	%mklibname %{name}-gir %{gir_major}
%define develname	%mklibname -d %{name}

Name: nautilus
Version: 3.2.1
Release: 1
Summary: File manager for the GNOME desktop environment
Group: File tools
License: GPLv2+
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/nautilus-%{version}.tar.xz
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

BuildRequires:	intltool
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.1.6
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.13
BuildRequires:	pkgconfig(gail-3.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.0.0
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(libexif)

Requires: %{lib_name} >= %{version}-%{release}
Requires(post): shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils

%description
Nautilus is an excellent file manager for the GNOME desktop environment.

%package -n %{lib_name}
Summary:        Libraries for Nautilus File manager
Group:          System/Libraries

%description -n %{lib_name}
Nautilus is an excellent file manager for the GNOME desktop environment.
This package contains libraries used by Nautilus.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{lib_name} = %{version}-%{release}
Conflicts:	%{lib_name} < 3.2.1

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary:        Libraries and include files for developing nautilus components
Group:          Development/GNOME and GTK+
Requires:		%{lib_name} = %{version}
%rename			%{name}-devel
Obsoletes:		%{lib_name}-devel

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop nautilus components.

%prep
rm -rf %{buildroot}

%setup -q
#patch2 -p1 -b .defaultdesktop
#patch12 -p1 -b .dynamic
#patch17 -p0 -b .symlink
#patch28 -p1 -b .kdedesktop
#patch32 -p1 -b .colour
#patch34 -p1 -b .rtlfix
#patch35 -p1 -b .umountfstab
#patch36 -p1 -b .lockdown-contextmenus
#patch37 -p1 -b .search-desktop
#patch39 -p1 -b .condrestart

%build
%configure2_5x \
	--disable-static \
	--disable-update-mimedb \
	--disable-schemas-compile

%make

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name "*.la" -exec rm -rf {} \;

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome/desktop \
	%{buildroot}%{_datadir}/nautilus/default-desktop \
	%{buildroot}%{_libdir}/nautilus/extensions-2.0

%{find_lang} %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
%dir %{_localstatedir}/lib/gnome/desktop
%dir %{_localstatedir}/lib/gnome/
%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop
%{_bindir}/*
%_libexecdir/nautilus-convert-metadata
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/nautilus.*
%{_datadir}/GConf/gsettings/nautilus.convert
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%{_datadir}/mime/packages/nautilus.xml
%{_datadir}/nautilus
%{_datadir}/pixmaps/*
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-2.0
%dir %{_libdir}/nautilus/extensions-3.0
%{_libdir}/nautilus/extensions-3.0/libnautilus-sendto.so
%{_mandir}/man1/*

%files -n %{lib_name}
%{_libdir}/libnautilus*.so.%{lib_major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Nautilus-%{gir_major}.typelib

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/libnautilus-extension
%{_datadir}/gir-1.0/Nautilus-%{gir_major}.gir

