%define major	1
%define gir_major	3.0
%define libname	%mklibname %{name}-extension %{major}
%define girname	%mklibname %{name}-gir %{gir_major}
%define develname	%mklibname -d %{name}

Summary: File manager for the GNOME desktop environment
Name: nautilus
Version: 3.6.3
Release: 1
Group: File tools
License: GPLv2+
URL: http://www.gnome.org/projects/nautilus/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/nautilus/3.6/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.13
BuildRequires:	pkgconfig(gail-3.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 3.0.0
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(exempi-2.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:  pkgconfig(tracker-sparql-0.14)

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
%{_libexecdir}/nautilus-shell-search-provider
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-2.0
%dir %{_libdir}/nautilus/extensions-3.0
%{_libdir}/nautilus/extensions-3.0/libnautilus-sendto.so
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.SearchProvider.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/gnome-shell/search-providers/nautilus-search-provider.ini
%{_datadir}/GConf/gsettings/nautilus.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%{_datadir}/mime/packages/nautilus.xml
%{_datadir}/nautilus
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



%changelog
* Fri Dec  7 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.3-1
- update to 3.6.3

* Mon Oct 29 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.1-1
- update to 3.6.1

* Tue Oct  2 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Tue May 15 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.2-1
+ Revision: 799033
- new version 3.4.2

* Thu May 03 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.4.1-1
+ Revision: 795389
- new version 3.4.1
- removed old sources and patches
- cleaned up spec more

* Sat Dec 03 2011 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-1
+ Revision: 737393
- new version 3.2.1
- split out gir pkg
- rebuild before major upgrade
- removed .la files
- cleaned up spec
- removed defattr, BuildRoot, clean section, mkrel
- removed old scriptlets
- removed dups app icons
- removed devel reqs from devel pkg

* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.32.2.1-4
+ Revision: 702919
- attempt to relink against libpng15.so.15

* Wed Sep 28 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.2.1-3
+ Revision: 701690
- rebuild
- rebuild for new libpng

* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 2.32.2.1-2
+ Revision: 669315
- br gconf2

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Wed Dec 29 2010 Funda Wang <fwang@mandriva.org> 2.32.2.1-1mdv2011.0
+ Revision: 625792
- add more BR
- update to new version 2.32.2.1

* Wed Dec 08 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.2-1mdv2011.0
+ Revision: 616309
- update to new version 2.32.2

* Sun Nov 14 2010 Funda Wang <fwang@mandriva.org> 2.32.1-1mdv2011.0
+ Revision: 597444
- update to new version 2.32.1

* Mon Sep 27 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581369
- update to new version 2.32.0

* Mon Sep 13 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.92-1mdv2011.0
+ Revision: 577910
- update build deps
- new version
- rediff patch 28
- update build deps

* Wed Aug 18 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.90-1mdv2011.0
+ Revision: 571174
- update to new version 2.31.90

* Thu Aug 12 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.31.6-1mdv2011.0
+ Revision: 569223
- update build deps
- enable introspection support
- new version
- rediff patch 28
- update file list

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.30.1-2mdv2010.1
+ Revision: 540358
- rebuild so that shared libraries are properly stripped again

* Mon Apr 26 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.1-1mdv2010.1
+ Revision: 538962
- update to new version 2.30.1

* Mon Mar 29 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 528769
- new version
- drop merged patch 0

* Sun Mar 14 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.92.1-2mdv2010.1
+ Revision: 518883
- fix border around desktop (bug #56686)'

* Wed Mar 10 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.92.1-1mdv2010.1
+ Revision: 517406
- update to new version 2.29.92.1

* Mon Mar 08 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 515984
- new version
- drop patch 33
- rediff patch 32

* Mon Feb 22 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.91-1mdv2010.1
+ Revision: 509762
- new version
- bump gnome-desktop dep

* Tue Feb 09 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.90-1mdv2010.1
+ Revision: 503158
- update to new version 2.29.90

* Mon Jan 25 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.2-1mdv2010.1
+ Revision: 496143
- update to new version 2.29.2

* Wed Jan 13 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.1-2mdv2010.1
+ Revision: 490618
- rebuild for new libgnome-desktop

* Tue Dec 22 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.29.1-1mdv2010.1
+ Revision: 481613
- new version
- drop patch 38
- bump gnome-desktop dep

* Tue Dec 15 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.4-1mdv2010.1
+ Revision: 478834
- update to new version 2.28.4

* Mon Dec 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.3-1mdv2010.1
+ Revision: 478456
- update to new version 2.28.3

* Mon Nov 30 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.2-1mdv2010.1
+ Revision: 471746
- new version
- drop patch 40

* Wed Oct 21 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.1-1mdv2010.0
+ Revision: 458622
- Fix BR
- Release 2.28.1
- Regenerate patch33
- Patch40 (Fedora): fix tracker 0.7 support
- Fix BR

* Mon Oct 05 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.0-2mdv2010.0
+ Revision: 454124
- Nautilus provides gnome-volume-manager features now

* Mon Sep 21 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446705
- new version
- drop patch 40

* Mon Sep 14 2009 Frederic Crozat <fcrozat@mandriva.com> 2.27.92-3mdv2010.0
+ Revision: 440662
- Patch40 (GIT): fix flashing at startup

* Thu Sep 10 2009 Frederic Crozat <fcrozat@mandriva.com> 2.27.92-2mdv2010.0
+ Revision: 436509
- Remove requires on drakxtools-newt, moved to nautilus-filesharing

* Mon Sep 07 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 432561
- new version
- drop patches 0,40

* Tue Sep 01 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.91-3mdv2010.0
+ Revision: 424045
- fix logout problem (bug #53329)

* Mon Aug 31 2009 Frederic Crozat <fcrozat@mandriva.com> 2.27.91-2mdv2010.0
+ Revision: 422857
- Patch39 (Fedora): fix infinite startup when show_desktop is disabled
- Patch40 (GIT): fix crash in configuration dialog

* Mon Aug 24 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.91-1mdv2010.0
+ Revision: 420573
- new version
- update file list

* Tue Jul 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 395762
- update to new version 2.27.4

* Mon Jun 15 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.2-1mdv2010.0
+ Revision: 385997
- new version
- rediff patch 36

* Mon May 11 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.27.1-1mdv2010.0
+ Revision: 374192
- new version
- update patch 37
- fix build

* Thu Apr 16 2009 Frederic Crozat <fcrozat@mandriva.com> 2.26.2-2mdv2009.1
+ Revision: 367709
- Update patch28 to really hide old KDE .desktop files

* Tue Apr 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.2-1mdv2009.1
+ Revision: 366962
- update to new version 2.26.2

* Fri Apr 03 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 363682
- new version
- drop patch 15

* Thu Apr 02 2009 Frederic Crozat <fcrozat@mandriva.com> 2.26.0-2mdv2009.1
+ Revision: 363523
- Update and apply patch34
- Patch36 (SUSE): allow to lockdown context menu (Novell bug #363122)
- Patch37 (SUSE): add a search .desktop file (GNOME bug #350950)
- Patch38: browser mode

* Mon Mar 16 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 355752
- update to new version 2.26.0

* Wed Mar 11 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.93-1mdv2009.1
+ Revision: 353718
- update to new version 2.25.93

* Mon Mar 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 347294
- update to new version 2.25.92

* Mon Feb 16 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 340887
- new version
- rediff patch 35

* Mon Feb 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.4-1mdv2009.1
+ Revision: 336428
- update to new version 2.25.4

* Mon Jan 19 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.3-1mdv2009.1
+ Revision: 331393
- update to new version 2.25.3

* Fri Dec 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.2-1mdv2009.1
+ Revision: 316103
- don't depend on eel anymore
- new version
- drop patches 0,22
- fix build deps
- update patches 12,28

* Tue Dec 02 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.25.1-1mdv2009.1
+ Revision: 309059
- update build deps
- new version
- bump deps
- update file list

* Mon Nov 24 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.2-1mdv2009.1
+ Revision: 306205
- update to new version 2.24.2

* Sun Nov 09 2008 Adam Williamson <awilliamson@mandriva.org> 2.24.1-3mdv2009.1
+ Revision: 301276
- rebuild for new xcb stuff

* Thu Nov 06 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.1-2mdv2009.1
+ Revision: 300216
- rebuild for new  gnome-desktop

* Mon Oct 20 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 295648
- update to new version 2.24.1

* Mon Sep 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 286436
- new version
- bump eel dep

* Tue Sep 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.92-1mdv2009.0
+ Revision: 282911
- new version

* Mon Sep 01 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 278665
- new version
- bump eel dep

* Wed Aug 20 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.90-1mdv2009.0
+ Revision: 274357
- new version

* Mon Aug 04 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.6.1-1mdv2009.0
+ Revision: 263529
- new version
- bump glib dep

* Thu Jul 24 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.5.1-2mdv2009.0
+ Revision: 245134
- patch to support XDS (drag to save) protocol
- patch to fix a crash

* Tue Jul 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.5.1-1mdv2009.0
+ Revision: 240355
- new version

* Tue Jul 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 240002
- new version
- rediff patch 12
- replace patch 33 with latest version from Fedora

* Thu Jul 03 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.23.4-1mdv2009.0
+ Revision: 231407
- new version
- disable patch 34
- update patch 34
- patch 0: fix build
- update file list

* Mon Jun 30 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.4-1mdv2009.0
+ Revision: 230283
- new version
- update license
- drop patch 36

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Jun 02 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.3-2mdv2009.0
+ Revision: 214325
- Patch36 (SVN): various bug fixes from SVN

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed May 28 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.3-1mdv2009.0
+ Revision: 212732
- new version
- drop patch 36

  + Frederic Crozat <fcrozat@mandriva.com>
    - really add patch
    - Patch36: various bug fixes from SVN

* Wed May 21 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.2-2mdv2009.0
+ Revision: 209752
- Patch35 : auto-unmount ejected medias when mount points are in fstab (Mdv bug #39540)

* Wed Apr 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.2-1mdv2009.0
+ Revision: 192474
- new version
- drop patch 35

* Tue Apr 01 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.1-2mdv2008.1
+ Revision: 191420
- Patch35: various fixes from SVN

* Fri Mar 28 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.1-1mdv2008.1
+ Revision: 190891
- Release 2.22.1
- Remove patch35, merged upstream

* Wed Mar 26 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-4mdv2008.1
+ Revision: 190445
- Update patch35 with new fixes from SVN (including Mdv bug #38654)

* Mon Mar 17 2008 Frederic Crozat <fcrozat@mandriva.com> 2.22.0-3mdv2008.1
+ Revision: 188379
- Patch33 (Fedora): replace buildtime with runtime dependencyu for beagle and tracker
- Patch34 (Fedora): fix build of RTL when self check are disabled
- Patch35 (SVN): many fixes from SVN

* Tue Mar 11 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.0-2mdv2008.1
+ Revision: 185244
- build with exempi support

* Tue Mar 11 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 184861
- new version

* Mon Feb 25 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.92-1mdv2008.1
+ Revision: 175143
- new version
- drop patch 33

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.21.91-2mdv2008.1
+ Revision: 170994
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Tue Feb 12 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.91-1mdv2008.1
+ Revision: 165834
- new version
- bump deps

* Tue Jan 29 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159639
- new version
- bump deps
- fix nautilus extensions dir

* Tue Jan 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.6-1mdv2008.1
+ Revision: 156156
- new version
- bump deps

* Mon Jan 14 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.5-1mdv2008.1
+ Revision: 151911
- new version
- drop patch 34
- update patch 12
- bump deps

* Thu Jan 10 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.2-4mdv2008.1
+ Revision: 147648
- Force rebuild with latest GConf package

* Thu Jan 10 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.2-3mdv2008.1
+ Revision: 147576
- Update patch34 with additional crasher fix when cancelling job

* Thu Jan 10 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.2-2mdv2008.1
+ Revision: 147519
- Patch34 (SVN): fix crash when overwriting file

* Tue Jan 08 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.2-1mdv2008.1
+ Revision: 146709
- new version
- drop patch 34

* Tue Jan 08 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.1-4mdv2008.1
+ Revision: 146517
- Ressurect and update patch28 for gio
- Patch34 (SVN): fix build with glib 2.15.1
- Remove patch31, feature no longer exist upstream
- Replace dependency on gnome-vfs with gvfs
- Restore removed patch

* Fri Jan 04 2008 Frederic Crozat <fcrozat@mandriva.com> 2.21.1-3mdv2008.1
+ Revision: 144972
- Restore and port patch 12 to gio/gvfs
- Restore removed patch

* Fri Dec 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2.21.1-2mdv2008.1
+ Revision: 138924
- Restore patch 2 (default launchers on desktop) and port it to gio
- Rename patch 0 as patch33
- Restore removed patch

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 21 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.21.1-1mdv2008.1
+ Revision: 136221
- new version
- bump deps
- rediff patch 0
- drop patches 2,12,28,36,39,40,41,42,43

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.0-8mdv2008.1
+ Revision: 120728
- new version
- patch for new libbeagle

* Thu Dec 06 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.0-7mdv2008.1
+ Revision: 116033
- rebuild for new libbeagle

* Tue Dec 04 2007 Thierry Vignaud <tv@mandriva.org> 2.20.0-6mdv2008.1
+ Revision: 115413
- rebuild for new libbeagle

* Tue Nov 06 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-5mdv2008.1
+ Revision: 106446
-Patch43 (Fedora): use totem audio preview or gstreamer for audio preview
-clean specfile

* Wed Oct 03 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-4mdv2008.0
+ Revision: 94930
- Patch42 (SVN): fix small fonts crash (GNOME bug #454884)

* Tue Oct 02 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-3mdv2008.0
+ Revision: 94664
- Patch41 (SVN): fix missing frame for async thumbnails (GNOME bug #478363)

* Tue Oct 02 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-2mdv2008.0
+ Revision: 94625
- Patch40 (SVN): fix thumbnail incorrect invalidation (GNOME bug #480608)

* Tue Sep 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.0
+ Revision: 89481
- new version
- drop patch 40

* Fri Sep 14 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.91-4mdv2008.0
+ Revision: 85545
- Update patch2 to work with xdg user directory
- don't update/clean gnome icon cache anymore

* Tue Aug 28 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.91-3mdv2008.0
+ Revision: 72654
- remove emblem-shared, it is in gnome-icon-theme

* Tue Aug 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.91-2mdv2008.0
+ Revision: 72473
- Patch40: fix .desktop to be valid
- Don't add old obsoletes categories to existing .desktop

* Mon Aug 27 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.91-1mdv2008.0
+ Revision: 71817
- new version

* Tue Aug 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.90-1mdv2008.0
+ Revision: 63276
- new version

* Tue Aug 07 2007 Frederic Crozat <fcrozat@mandriva.com> 2.19.6-2mdv2008.0
+ Revision: 59956
- Remove patch40, not needed anymore with XDG user dirs

* Tue Jul 31 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.6-1mdv2008.0
+ Revision: 56995
- fix buildrequires
- new version
- drop patch 41

* Tue Jul 24 2007 Pascal Terjan <pterjan@mandriva.org> 2.19.5-2mdv2008.0
+ Revision: 54987
- Added P41 from svn to fix crash in browser mode

* Tue Jul 10 2007 Funda Wang <fwang@mandriva.org> 2.19.5-1mdv2008.0
+ Revision: 50855
- New version

* Tue Jun 19 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 41287
- new version
- call unversioned automake

* Wed Jun 06 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.3-1mdv2008.0
+ Revision: 36019
- new version

* Wed Apr 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.1-3mdv2008.0
+ Revision: 14382
- new version


* Tue Apr 03 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0.1-3mdv2007.1
+ Revision: 150400
- Update patch2 to handle productid with trailing space

* Thu Mar 15 2007 Frederic Crozat <fcrozat@mandriva.com> 2.18.0.1-2mdv2007.1
+ Revision: 144376
- Update patch2: add support for default desktop files based on productid

* Mon Mar 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.0.1-1mdv2007.1
+ Revision: 141722
- new version

* Mon Mar 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.0-1mdv2007.1
+ Revision: 141697
- new version
- readd ChangeLog

  + Thierry Vignaud <tvignaud@mandriva.com>
    - no need to package big ChangeLog when NEWS is already there

* Mon Feb 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.92-2mdv2007.1
+ Revision: 125912
- new version

* Wed Feb 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.91-2mdv2007.1
+ Revision: 120778
- bump
- new version

* Mon Jan 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.90-1mdv2007.1
+ Revision: 111888
- new version

* Mon Dec 18 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.1-1mdv2007.1
+ Revision: 98481
- new version
- rediff patch 32
- add new icons

* Wed Nov 22 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.3-1mdv2007.1
+ Revision: 86209
- new version

* Wed Nov 08 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.2-2mdv2007.1
+ Revision: 78048
- bot rebuild
- new version

* Fri Oct 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.1-3mdv2007.1
+ Revision: 63832
- rebuild
- unpack patches
- Import nautilus

* Fri Oct 06 2006 Götz Waschk <waschk@mandriva.org> 2.16.1-1mdv2007.0
- drop patch 41
- New version 2.16.1

* Thu Sep 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.16.0-2mdv2007.0
- Patch41 (CVS): fix various crashes

* Tue Sep 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.0-1mdv2007.0
- New release 2.16.0

* Tue Aug 22 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.92.1-1mdv2007.0
- Release 2.15.92.1

* Wed Aug 09 2006 Götz Waschk <waschk@mandriva.org> 2.15.91-1mdv2007.0
- bump deps
- drop patch 1
- New release 2.15.91

* Tue Aug 08 2006 Götz Waschk <waschk@mandriva.org> 2.15.90-3mdv2007.0
- patch 1: fix bug 23804

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.90-2mdv2007.0
- Rebuild with latest dbus

* Wed Jul 26 2006 Götz Waschk <waschk@mandriva.org> 2.15.90-1mdv2007.0
- bump deps
- New release 2.15.90

* Fri Jul 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.4-2mdv2007.0
- Rebuild with latest libgail

* Wed Jul 12 2006 Götz Waschk <waschk@mandriva.org> 2.15.4-1mdv2007.0
- new macros
- xdg menu
- bump deps
- New release 2.15.4

* Wed Jun 14 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.2-2mdv2007.0
- Fix patch40 to no longer used removed eel functions

* Tue Jun 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.2-1
- New release 2.15.2

* Sat Jun 03 2006 Frederic Crozat <fcrozat@mandriva.com> 2.15.1-1mdv2007.0
- Release 2.15.1
- Remove patch37 (merged upstream)

* Sat Apr 22 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-6mdk
- Remove patch18 (no longer needed)

* Thu Apr 20 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.14.1-5mdk
- add BuildRequires: intltool

* Wed Apr 19 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-4mdk
- Fix invalid conflicts on library package

* Mon Apr 17 2006 Götz Waschk <waschk@mandriva.org> 2.14.1-3mdk
- enable beagle support

* Sat Apr 15 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-1mdk
- Add conflicts to ease upgrade

* Sat Apr 15 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.1-1mdk
- Release 2.14.1

* Sun Mar 05 2006 Michael Scherer <misc@mandriva.org> 2.12.2-4mdk
- own %%{_localstatedir}/gnome/, fix #16329

* Mon Feb 27 2006 Frederic Crozat <fcrozat@mandriva.com> 2.12.2-3mdk
- Fortify uninstall script

* Fri Feb 24 2006 Frederic Crozat <fcrozat@mandriva.com> 2.12.2-2mdk
- Use mkrel

* Mon Nov 28 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.12.2-1mdk
- New release 2.12.2

* Fri Oct 28 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-6mdk
- Update patch40, fix crash when .desktop (Mdk bug #19464)

* Tue Oct 25 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-5mdk
- Patch40: add support for .desktop item in gtk bookmarks

* Fri Oct 21 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-4mdk
- Update buildrequires

* Wed Oct 19 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-3mdk
- Fix buildrequires

* Wed Oct 12 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.12.1-2mdk
- rebuild for new libgsf

* Fri Oct 07 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-1mdk
- Release 2.12.1
- Remove patches 0, 34, 38, 40, 41 (merged upstream)

* Wed Sep 14 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-9mdk 
- Patch40 (CVS): various upstream fixes including Mdk bug #17968
- Patch41 (neumair): fix lazy icon positioning (for new volume)

* Sat Sep 10 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-8mdk 
- Patch39: don't check sound server status to allow audio preview

* Fri Sep 09 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-6mdk 
- Update patch28 to not show device box from KDE

* Sat Sep 03 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.10.1-6mdk
- rebuild to remove glitz dep

* Thu Sep 01 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-5mdk 
- Patch38: workaround bug in radeon acceleration (Mdk bug #17723)

* Thu Aug 18 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-4mdk 
- Update patch28 to also hide KDE trask .desktop file

* Sun Jun 12 2005 Götz Waschk <waschk@mandriva.org> 2.10.1-3mdk
- don't thumbnail files that are still changing

* Sat Apr 23 2005 Götz Waschk <waschk@mandriva.org> 2.10.1-2mdk
- fix buildrequires

* Fri Apr 22 2005 Frederic Crozat <fcrozat@mandriva.com> 2.10.1-1mdk 
- Release 2.10.1 (based on Götz Waschk package)
- Regenerate patch31
- Remove patches 33 (no longer applicable), 35 (merged upstream)
- Remove dependency on gnome-control-center

* Sat Apr 02 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-8mdk 
- Patch37: fix i18n init for windows name

* Tue Mar 22 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-7mdk 
- Patch36: don't monitor supermount devices (Mdk bug #14880)

* Thu Mar 17 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-6mdk 
- Patch35 (CVS): various fixes

* Wed Jan 05 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-5mdk 
- Rebuild with latest howl

* Tue Dec 28 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.8.2-4mdk
- rebuild with libexif 0.6.x

* Tue Nov 23 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.8.2-3mdk 
- Remove eog dependency, bonobo component is no more used (Fedora)

* Wed Nov 10 2004 Götz Waschk <waschk@linux-mandrake.com> 2.8.2-2mdk
- add sox dependancy (Thierry Vignaud)

* Wed Nov 10 2004 Götz Waschk <waschk@linux-mandrake.com> 2.8.2-1mdk
- fix buildrequires
- New release 2.8.2
- Remove patches 16 (handled by nautilus-filesharing extension), 35, 36, 37, 38 (merged upstream)
- Regenerate patches 2, 31

* Fri Sep 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.3-10mdk
- Update patch36 to remove one warning
- Update patch16 to remove one warning
- Update patch31 for new mimetype for desktop file

* Thu Sep 09 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.3-9mdk
- Patch37: fix emblem sort (Mdk bug #10767)
- Patch38 (CVS): fix rare crash

* Tue Sep 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.3-8mdk
- Patch35 (CVS): quiet nautilus for small image file
- Patch36 : fix bonobo warning (Mdk bug #11125)

* Fri Sep 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.3-7mdk
- Patch34: fix background with local encoded name loading (Mdk bug #10353)

* Fri Aug 27 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.3-6mdk
- Fix menu

* Wed Aug 04 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.3-5mdk
- disable patch 33 to build with libexif9 again

* Tue Aug 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.3-4mdk
- Patch33: Fix build with libexif 0.6.9

* Sat Jul 24 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.6.3-3mdk
- add BuildRequires: automake1.8

* Thu Jul 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com>  2.6.3-2mdk
- Requires gnome-control-center for the file-properties config dialog.

* Wed Jun 16 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.6.3-1mdk
- New release 2.6.3

* Mon Jun 07 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.2-1mdk
- new version

* Tue Apr 20 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.1-1mdk
- rediff patch 16
- New release 2.6.1

* Thu Apr 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-2mdk
- Rebuild against latest libcroco

* Wed Apr 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-1mdk
- Release 2.6.0 (with Götz help)
- Regenerates patches 12, 16, 31
- Bump requirements
- Disable patch27 (need to be moved to gnome-vfs)
- Remove patches 33, 34, 35 (merged upstream)

