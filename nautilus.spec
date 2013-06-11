%define lib_major	1
%define gir_major	3.0
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname -d %{name}
%define gir_name	%mklibname %{name}-gir %{gir_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		nautilus
Version:	3.8.1
Release:	1
Summary:	File manager for the GNOME desktop environment
Group:		File tools
License:	GPLv2+
URL:		http://www.gnome.org/projects/nautilus/
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		nautilus-3.5.92-linkage.patch
BuildRequires:	intltool
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.5.12
BuildRequires:	pkgconfig(glib-2.0) >= 2.33.13
BuildRequires:	pkgconfig(gail-3.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.0.0
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(tracker-sparql-0.16)
Suggests:	tracker

%description
Nautilus is an excellent file manager for the GNOME desktop environment.

%package -n %{lib_name}
Summary:	Libraries for Nautilus File manager
Group:		System/Libraries

%description -n %{lib_name}
Nautilus is an excellent file manager for the GNOME desktop environment.
This package contains libraries used by Nautilus.

%package -n %{develname}
Summary:	Libraries and include files for developing nautilus components
Group:		Development/GNOME and GTK+
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop nautilus components.

%package -n %{gir_name}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}
Conflicts:	%{lib_name} < 3.1.3-3

%description -n %{gir_name}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-update-mimedb \
	--disable-schemas-compile
%make

%install
%makeinstall_std

# we don't want these
find %{buildroot} -name "*.la" -exec rm -rf {} \;

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome/desktop \
	%{buildroot}%{_datadir}/%{name}/default-desktop \
	%{buildroot}%{_libdir}/%{name}/extensions-2.0

# only start in GNOME
echo "OnlyShowIn=GNOME;" >> %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop

%{find_lang} %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
%dir %{_localstatedir}/lib/gnome/desktop
%dir %{_localstatedir}/lib/gnome/
%{_bindir}/*
%{_libexecdir}/%{name}-convert-metadata
%{_mandir}/man1/*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop
%{_datadir}/GConf/gsettings/%{name}.convert
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.SearchProvider.service
%{_datadir}/gnome-shell/search-providers/%{name}-search-provider.ini
%{_datadir}/glib-2.0/schemas/org.gnome.%{name}.gschema.xml
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/extensions-3.0
%{_libdir}/%{name}/extensions-3.0/lib%{name}-sendto.so

%files -n %{lib_name}
%{_libdir}/lib%{name}*.so.%{lib_major}*

%files -n %{gir_name}
%{_libdir}/girepository-1.0/Nautilus-%{gir_major}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/lib%{name}-extension
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/Nautilus-%{gir_major}.gir
