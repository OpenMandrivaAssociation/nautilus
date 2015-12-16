%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api	3.0
%define major	1
%define libname	%mklibname %{name}-extension %{major}
%define devname	%mklibname -d %{name}-extension
%define girname	%mklibname %{name}-gir %{api}

Summary:	File manager for the GNOME desktop environment
Name:		nautilus
Version:	3.18.3
Release:	1
Group:		File tools
License:	GPLv2+
Url:		http://www.gnome.org/projects/nautilus/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/nautilus/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	intltool
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(gail-3.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.33.13
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.0.0
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.5.12
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(libxml-2.0) >= 2.7.8
BuildRequires:	pkgconfig(tracker-sparql-1.0)
BuildRequires:	pkgconfig(x11)
Suggests:	tracker

%description
Nautilus is an excellent file manager for the GNOME desktop environment.

%package -n %{libname}
Summary:	Libraries for Nautilus File manager
Group:		System/Libraries
Obsoletes:	%{_lib}nautilus1 < 3.8.1-2

%description -n %{libname}
Nautilus is an excellent file manager for the GNOME desktop environment.
This package contains libraries used by Nautilus.

%package -n %{devname}
Summary:	Libraries and include files for developing nautilus components
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}nautilus-devel < 3.8.1-2

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop nautilus components.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{libname} < 3.1.3-3

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure \
	--disable-static \
	--disable-update-mimedb \
	--disable-schemas-compile
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome/desktop \
	%{buildroot}%{_datadir}/%{name}/default-desktop \
	%{buildroot}%{_libdir}/%{name}/extensions-2.0

# only start in GNOME
echo "OnlyShowIn=GNOME;" >> %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
%dir %{_localstatedir}/lib/gnome/desktop
%dir %{_localstatedir}/lib/gnome/
%{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop
%{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/extensions-3.0
%{_libdir}/%{name}/extensions-3.0/lib%{name}-sendto.so
%{_libexecdir}/%{name}-convert-metadata
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/gnome-shell/search-providers/%{name}-search-provider.ini
%{_datadir}/GConf/gsettings/%{name}.convert
%{_datadir}/glib-2.0/schemas/org.gnome.%{name}.gschema.xml
%{_mandir}/man1/*
%{_datadir}/appdata/org.gnome.Nautilus.appdata.xml

%files -n %{libname}
%{_libdir}/libnautilus-extension.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Nautilus-%{api}.typelib

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/lib%{name}-extension
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Nautilus-%{api}.gir

