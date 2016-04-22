%bcond_with docs

%define major 0
%define api 1.0
%define libname %mklibname %{name} %{api} %{major}
%define libgstbase %mklibname gstbase %{api} %{major}
%define libgstcheck %mklibname gstcheck %{api} %{major}
%define libgstcontroller %mklibname gstcontroller %{api} %{major}
%define libgstnet %mklibname gstnet %{api} %{major}
%define girname %mklibname gst-gir %{api}
%define devname %mklibname -d %{name}

Name:		gstreamer
Summary: 	GStreamer Streaming-media framework runtime
Version: 	1.8.1
Release: 	1
License: 	LGPLv2+
Group:		Sound
Url:		http://gstreamer.freedesktop.org/
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/gstreamer/%(echo %{version}|cut -d. -f1-2)/%{name}-%{version}.tar.xz
Patch0:		gstreamer-inspect-rpm-format.patch

BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(popt)
%ifarch %{ix86}
BuildRequires:	nasm => 0.90
BuildRequires:	pkgconfig(valgrind)
%endif
%if %{with docs}
BuildRequires:	gtk-doc >= 0.7
BuildRequires:	transfig
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd412-xml
BuildRequires:	ghostscript
BuildRequires:	python-pyxml
%endif

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package	tools
Summary:	GStreamer Streaming-media framework runtime
Group:		Sound
%rename		gstreamer1.0-tools

%description	tools
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package -n	%{libname}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries
Provides:	libgstreamer%{api} = %{version}-%{release}

%description -n	%{libname}
This package contains the library for %{name}.

%package -n	%{libgstbase}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n	%{libgstbase}
This package contains the library for %{name}base.

%package -n	%{libgstcheck}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n	%{libgstcheck}
This package contains the library for %{name}check.

%package -n	%{libgstcontroller}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n	%{libgstcontroller}
This package contains the library for %{name}controller.

%package -n	%{libgstnet}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n	%{libgstnet}
This package contains the library for %{name}net.

%package -n	%{girname}
Summary:	GObject Introspection interface libraries for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface libraries for %{name}.

%package -n	%{devname}
Summary:	Libraries and include files for GStreamer streaming-media framework
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libgstbase} = %{version}-%{release}
Requires:	%{libgstcheck} = %{version}-%{release}
Requires:	%{libgstcontroller} = %{version}-%{release}
Requires:	%{libgstnet} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{name}%{api}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer.

%prep
%setup -q
%apply_patches

%build
%configure \
	--enable-debug \
	--with-package-name='%{distribution} %{name} package' \
	--with-package-origin='%{disturl}' \
	--disable-tests \
	--disable-examples \
%if %{with docs}
	--enable-docbook \
	--enable-gtk-doc \
%else
	--disable-docbook \
	--disable-gtk-doc \
%endif
%ifarch %{mips}
	--disable-valgrind \
%endif
	--with-html-dir=%{_datadir}/gtk-doc/html

%make

%check
#cd tests/check
#make check

%install
%makeinstall_std
mkdir -p %{buildroot}%{_var}/cache/%{name}-%{api}

%find_lang %{name}-%{api}

#gw really remove rpath for rpmlint
chrpath -d %{buildroot}{%{_bindir}/gst-{inspect,launch,typefind}-%{api},%{_libdir}/{*.so,%{name}-%{api}/*.so}}
#,xmlinspect,xmllaunch

%files tools -f %{name}-%{api}.lang
%doc AUTHORS COPYING README NEWS
%dir %{_var}/cache/%{name}-%{api}
%{_bindir}/gst-inspect-%{api}
%{_bindir}/gst-launch-%{api}
%{_bindir}/gst-stats-%{api}
%{_bindir}/gst-typefind-%{api}
%dir %{_libdir}/%{name}-%{api}
%{_libexecdir}/%{name}-%{api}/gst-plugin-scanner
%{_libexecdir}/%{name}-%{api}/gst-ptp-helper
%{_datadir}/bash-completion/completions/*
%{_datadir}/bash-completion/helpers/*
%{_libdir}/%{name}-%{api}/libgstcoreelements.so
%{_libdir}/%{name}-%{api}/libgstcoretracers.so
%{_mandir}/man1/gst-inspect-%{api}.1*
%{_mandir}/man1/gst-launch-%{api}.1*
%{_mandir}/man1/gst-typefind-%{api}.1*

%files -n %{libname}
%{_libdir}/libgstreamer-%{api}.so.%{major}*

%files -n %{libgstbase}
%{_libdir}/libgstbase-%{api}.so.%{major}*

%files -n %{libgstcheck}
%{_libdir}/libgstcheck-%{api}.so.%{major}*

%files -n %{libgstcontroller}
%{_libdir}/libgstcontroller-%{api}.so.%{major}*

%files -n %{libgstnet}
%{_libdir}/libgstnet-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Gst-%{api}.typelib
%{_libdir}/girepository-1.0/GstBase-%{api}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{api}.typelib
%{_libdir}/girepository-1.0/GstController-%{api}.typelib
%{_libdir}/girepository-1.0/GstNet-%{api}.typelib

%files -n %{devname}
%doc ChangeLog
%if %{with docs}
%doc %{_datadir}/doc/%{name}-%{api}
%endif
%dir %{_includedir}/%{name}-%{api}
%dir %{_includedir}/%{name}-%{api}/gst
%{_includedir}/%{name}-%{api}/gst/*.h
%dir %{_includedir}/%{name}-%{api}/gst/base/
%{_includedir}/%{name}-%{api}/gst/base/*.h
%{_includedir}/%{name}-%{api}/gst/check/
%dir %{_includedir}/%{name}-%{api}/gst/controller/
%{_includedir}/%{name}-%{api}/gst/controller/*.h
%{_includedir}/%{name}-%{api}/gst/net/
%{_libdir}/%{name}-%{api}/include/gst
%{_libdir}/libgstbase-%{api}.so
%{_libdir}/libgstcheck-%{api}.so
%{_libdir}/libgstreamer-%{api}.so
%{_libdir}/libgstnet-%{api}.so
%{_libdir}/libgstcontroller-%{api}.so
%{_libdir}/pkgconfig/gstreamer-%{api}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{api}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{api}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{api}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{api}.pc
%{_datadir}/aclocal/gst-element-check-%{api}.m4
%{_datadir}/gtk-doc/html/%{name}-%{api}/
%{_datadir}/gtk-doc/html/%{name}-libs-%{api}/
%{_datadir}/gtk-doc/html/%{name}-plugins-%{api}
%{_datadir}/gir-1.0/Gst-%{api}.gir
%{_datadir}/gir-1.0/GstBase-%{api}.gir
%{_datadir}/gir-1.0/GstCheck-%{api}.gir
%{_datadir}/gir-1.0/GstController-%{api}.gir
%{_datadir}/gir-1.0/GstNet-%{api}.gir

