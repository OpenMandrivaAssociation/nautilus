%define major	1
%define gir_major	3.0
%define libname	%mklibname %{name}-extension %{major}
%define girname	%mklibname %{name}-gir %{gir_major}
%define develname	%mklibname -d %{name}

Summary: File manager for the GNOME desktop environment
Name: nautilus
Version: 3.4.1
Release: 1
Group: File tools
License: GPLv2+
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.1.6
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.13
BuildRequires:	pkgconfig(gail-3.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.0.0
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(libexif)

Requires(post,postun): shared-mime-info desktop-file-utils

%description
Nautilus is an excellent file manager for the GNOME desktop environment.

%package -n %{libname}
Summary:        Libraries for Nautilus File manager
Group:          System/Libraries
Obsoletes:	%{_lib}nautilus1 < 3.4.1-1

%description -n %{libname}
Nautilus is an excellent file manager for the GNOME desktop environment.
This package contains libraries used by Nautilus.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Conflicts:	%{libname} < 3.2.1

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary:	Libraries and include files for developing nautilus components
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}
Requires:	%{girname} = %{version}
%rename		%{name}-devel
Obsoletes:	%{libname}-devel

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop nautilus components.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--disable-update-mimedb \
	--disable-schemas-compile

%make

%install
%makeinstall_std
find %{buildroot} -name "*.la" -exec rm -rf {} \;

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome/desktop \
	%{buildroot}%{_datadir}/nautilus/default-desktop \
	%{buildroot}%{_libdir}/nautilus/extensions-2.0

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
%dir %{_localstatedir}/lib/gnome/desktop
%dir %{_localstatedir}/lib/gnome/
%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop
%{_bindir}/*
%{_libexecdir}/nautilus-convert-metadata
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-2.0
%dir %{_libdir}/nautilus/extensions-3.0
%{_libdir}/nautilus/extensions-3.0/libnautilus-sendto.so
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/GConf/gsettings/nautilus.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%{_datadir}/mime/packages/nautilus.xml
%{_datadir}/nautilus
%{_iconsdir}/hicolor/*/apps/nautilus.*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libnautilus*.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Nautilus-%{gir_major}.typelib

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/libnautilus-extension
%{_datadir}/gir-1.0/Nautilus-%{gir_major}.gir

