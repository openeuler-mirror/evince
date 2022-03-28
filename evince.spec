Name:           evince
Version:        3.38.2
Release:        2
Summary:        Document viewer for multiple document formats
License:        GPLv2+ and GPLv3+ and LGPLv2+ and MIT and Afmparse
URL:            https://wiki.gnome.org/Apps/Evince
Source0:        https://download.gnome.org/sources/%{name}/3.38/%{name}-%{version}.tar.xz
Patch0:         evince-3.21.4-NPNVToolKit.patch
%ifarch riscv64
Patch1:         prevent-search-synctex.patch
%endif

BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.36.0 pkgconfig(gtk+-x11-3.0) >= 3.16.0 pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(poppler-glib) >= 0.33.0 pkgconfig(libgxps) >= 0.2.1       pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libnautilus-extension) pkgconfig(libxml-2.0)  pkgconfig(gspell-1)   pkgconfig(libspectre)
BuildRequires:  pkgconfig(adwaita-icon-theme)    pkgconfig(libsecret-1) pkgconfig(libarchive) libappstream-glib-devel
BuildRequires:  pkgconfig(gstreamer-1.0) pkgconfig(gstreamer-base-1.0) pkgconfig(gstreamer-video-1.0) pkgconfig(synctex) >= 1.19
BuildRequires:  desktop-file-utils itstool libtool gtk-doc texlive-lib-devel meson djvulibre-devel
BuildRequires:  gnome-common intltool gettext-devel gcc-c++ libtiff-devel yelp-tools gcc
Provides:       evince-libs evince-dvi evince-nautilus
Obsoletes:      evince-libs evince-dvi evince-nautilus
Requires:       glib2%{?_isa} >= 2.36.0 gtk3%{?_isa} >= 3.22.0 texlive-collection-fontsrecommended nautilus

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
%description    help 
This package contain the help documents for evince.

%prep
%autosetup -n %{name}-%{version} -p1

%build
export CFLAGS='-I%{_builddir}/%{name}-%{version}/cut-n-paste/synctex %optflags'
#export CFLAGS='-I/usr/include/synctex %optflags'
%meson -Dcomics=enabled -Ddvi=enabled -Ddjvu=enabled -Dxps=enabled \
        -Dt1lib=disabled -Dsystemduserunitdir=no -Dnautilus=false \
	-Dps=enabled

%meson_build

%install
%meson_install
%find_lang evince --with-gnome

install -d $RPM_BUILD_ROOT%{_datadir}/applications
find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.la' -print -delete
find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.a' -print -delete

%check
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/metainfo/org.gnome.Evince.appdata.xml
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
%{_libdir}/*.so.*
%dir %{_libdir}/evince
%dir %{_libdir}/evince/4
%dir %{_libdir}/evince/4/backends
%{_libdir}/evince/4/backends/*.so
%{_libdir}/evince/4/backends/*.evince-backend
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
* Sun Mar 27 2022 YukariChiba <i@0x7f.cc> - 3.38.2-2
- Use internal synctex instead

* Tue Jun 15 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 3.38.2-1
- Upgrade to 3.38.2
- Delete 0001-Resolves-deb-762530-rhbz-1061177-add-man-pages.patch that
  existed in 3.38.2 version
- Use meson rebuild, change 'SYNCTEX_CFLAGS' to 'CFLAGS'

* Mon Jun 8 2020 yanan li <liyanan032@huawei.com> - 3.30.1-4
- Disable designated LIBTOOL directory in %make_build
 
* Mon Dec 2 2019 chenzhenyu <chenzhenyu13@huawei.com> - 3.30.1-3
- Package init
