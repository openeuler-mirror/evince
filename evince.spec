Name:           evince
Version:        3.30.1
Release:        3
Summary:        Document viewer for multiple document formats
License:        GPLv2+ and GPLv3+ and LGPLv2+ and MIT and Afmparse
URL:            https://wiki.gnome.org/Apps/Evince
Source0:        https://download.gnome.org/sources/%{name}/3.30/%{name}-%{version}.tar.xz
Patch0:         evince-3.21.4-NPNVToolKit.patch
Patch1:         0001-Resolves-deb-762530-rhbz-1061177-add-man-pages.patch

BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.36.0 pkgconfig(gtk+-x11-3.0) >= 3.16.0 pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(poppler-glib) >= 0.24.0 pkgconfig(libgxps) >= 0.2.1       pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libnautilus-extension) pkgconfig(libxml-2.0)  pkgconfig(gspell-1)   pkgconfig(libspectre)
BuildRequires:  pkgconfig(adwaita-icon-theme)    pkgconfig(libsecret-1) pkgconfig(libarchive) libappstream-glib
BuildRequires:  desktop-file-utils itstool libtool gtk-doc texlive-lib-devel
BuildRequires:  gnome-common intltool gettext gcc-c++ libtiff-devel yelp-tools
Provides:       evince-libs evince-dvi evince-nautilus
Obsoletes:      evince-libs evince-dvi evince-nautilus
Requires:       glib2%{?_isa} >= 2.36.0 gtk3%{?_isa} >= 3.16.0 texlive-collection-fontsrecommended nautilus

%description
Evince is a document viewer for multiple document formats. The goal of evince is to replace the
multiple document viewers that exist on the GNOME Desktop with a single simple application.
Evince is specifically designed to support the file following formats:
PDF, Postscript, djvu, tiff, dvi, XPS, SyncTex support with gedit, comics books (cbr,cbz,cb7 and cbt).

%package        devel
Summary:        Support for developing backends for the evince document viewer
Requires:       %{name}-libs = %{version}-%{release}

%description devel
This package contains libraries and header files needed for evince
backend development.

%package        help
Summary:        Help documents for evince
%description    
This package contain the help documents for evince.

%prep
%autosetup -n %{name}-%{version} -p1

%build
export SYNCTEX_CFLAGS=-I/usr/include/synctex
autoreconf -f -i
%configure --disable-static --enable-introspection --enable-comics=yes --enable-dvi=yes \
           --enable-libgnome-desktop --enable-xps=yes --enable-t1lib=no --enable-ps=yes
%make_build V=1 LIBTOOL=/usr/bin/libtool

%install
%make_install
%find_lang evince --with-gnome

install -d $RPM_BUILD_ROOT%{_datadir}/applications
find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.la' -print -delete
find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.a' -print -delete

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/org.gnome.Evince.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/org.gnome.Evince-previewer.desktop

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f evince.lang
%license COPYING
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/org.gnome.Evince*
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service
%{_datadir}/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%{_datadir}/GConf/gsettings/evince.convert
%{_datadir}/metainfo/org.gnome.Evince.appdata.xml
%{_datadir}/thumbnailers/evince.thumbnailer
%{_libexecdir}/evinced
%{_userunitdir}/org.gnome.Evince.service
%{_libdir}/*.so.*
%dir %{_libdir}/evince
%dir %{_libdir}/evince/4
%dir %{_libdir}/evince/4/backends
%{_libdir}/evince/4/backends/*.so
%{_libdir}/evince/4/backends/*.evince-backend
%{_libdir}/nautilus/extensions-3.0/libevince-properties-page.so
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/metainfo/*.metainfo.xml

%files devel
%{_datadir}/gtk-doc/html/evince/
%{_datadir}/gtk-doc/html/libevview-3.0
%{_datadir}/gtk-doc/html/libevdocument-3.0
%dir %{_includedir}/evince
%{_includedir}/evince/3.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir

%files help
%doc NEWS AUTHORS
%{_mandir}/man1/*.1*


%changelog
* Mon Dec 2 2019 chenzhenyu <chenzhenyu13@huawei.com> - 3.30.1-3
- Package init
