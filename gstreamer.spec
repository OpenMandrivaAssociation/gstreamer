%global optflags %{optflags} -O3

# gstreamer is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

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
%define lib32name %mklib32name %{name} %{api} %{major}
%define lib32gstbase %mklib32name gstbase %{api} %{major}
%define lib32gstcheck %mklib32name gstcheck %{api} %{major}
%define lib32gstcontroller %mklib32name gstcontroller %{api} %{major}
%define lib32gstnet %mklib32name gstnet %{api} %{major}
%define dev32name %mklib32name -d %{name}

Name:		gstreamer
Summary:	GStreamer Streaming-media framework runtime
Version:	1.19.1
Release:	1
License:	LGPLv2+
Group:		Sound
Url:		http://gstreamer.freedesktop.org/
Source0: 	https://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz
# RPM Provides: generator
Source10:	gstreamer.attr
Source11:	gstreamer.prov
Patch0:		gstreamer-inspect-rpm-format.patch

BuildRequires:	meson
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	libcap-utils
BuildRequires:	cmake
%ifnarch %{riscv}
BuildRequires:	pkgconfig(valgrind)
%endif
BuildRequires:	pkgconfig(libdw)
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
%endif
%if %{with compat32}
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libpcre)
BuildRequires:	devel(libz)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libxml2)
BuildRequires:	devel(libpopt)
BuildRequires:	devel(libcap)
BuildRequires:	devel(libdw)
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libelf)
BuildRequires:	libunwind-nongnu-devel
%endif

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

%package tools
Summary:	GStreamer Streaming-media framework runtime
Group:		Sound
%rename		gstreamer1.0-tools

%description tools
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

%package -n %{libname}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries
Provides:	libgstreamer%{api} = %{version}-%{release}

%description -n %{libname}
This package contains the library for %{name}.

%package -n %{libgstbase}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n %{libgstbase}
This package contains the library for %{name}base.

%package -n %{libgstcheck}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n %{libgstcheck}
This package contains the library for %{name}check.

%package -n %{libgstcontroller}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n %{libgstcontroller}
This package contains the library for %{name}controller.

%package -n %{libgstnet}
Summary:	Library for GStreamer streaming-media framework
Group:		System/Libraries

%description -n %{libgstnet}
This package contains the library for %{name}net.

%package -n %{girname}
Summary:	GObject Introspection interface libraries for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface libraries for %{name}.

%package -n %{devname}
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
# For gst-inspect, used by rpm dependency generator
Requires:	%{name}-tools = %{EVRD}

%description -n %{devname}
This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Library for GStreamer streaming-media framework (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the library for %{name}.

%package -n %{lib32gstbase}
Summary:	Library for GStreamer streaming-media framework (32-bit)
Group:		System/Libraries

%description -n %{lib32gstbase}
This package contains the library for %{name}base.

%package -n %{lib32gstcheck}
Summary:	Library for GStreamer streaming-media framework (32-bit)
Group:		System/Libraries

%description -n %{lib32gstcheck}
This package contains the library for %{name}check.

%package -n %{lib32gstcontroller}
Summary:	Library for GStreamer streaming-media framework (32-bit)
Group:		System/Libraries

%description -n %{lib32gstcontroller}
This package contains the library for %{name}controller.

%package -n %{lib32gstnet}
Summary:	Library for GStreamer streaming-media framework (32-bit)
Group:		System/Libraries

%description -n %{lib32gstnet}
This package contains the library for %{name}net.

%package -n %{dev32name}
Summary:	Libraries and include files for GStreamer streaming-media framework (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32gstbase} = %{version}-%{release}
Requires:	%{lib32gstcheck} = %{version}-%{release}
Requires:	%{lib32gstcontroller} = %{version}-%{release}
Requires:	%{lib32gstnet} = %{version}-%{release}

%description -n %{dev32name}
This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer.
%endif

%prep
%autosetup -p1
%if %{with compat32}
%meson32 \
	-Dpackage-name='%{distribution} %{name} 32-bit package' \
	-Dpackage-origin='%{disturl}' \
	-Dtests=disabled \
	-Dexamples=disabled \
	-Ddbghelp=disabled \
	-Dintrospection=disabled \
	-Dgtk-doc=disabled \
	-Ddoc=disabled
%endif

%meson \
	-Dpackage-name='%{distribution} %{name} package' \
	-Dpackage-origin='%{disturl}' \
	-Dtests=disabled \
	-Dexamples=disabled \
	-Ddbghelp=disabled \
%if %{with docs}
	-Dgtk-doc=enabled \
%else
	-Dgtk-doc=disabled \
%endif
	-Ddoc=disabled

%build
%if %{with compat32}
%ninja_build -C build32
%endif

%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build
mkdir -p %{buildroot}%{_var}/cache/%{name}-%{api}

%find_lang %{name}-%{api}

#gw really remove rpath for rpmlint
chrpath -d %{buildroot}{%{_bindir}/gst-{inspect,launch,typefind}-%{api},%{_libdir}/{*.so,%{name}-%{api}/*.so}}
#,xmlinspect,xmllaunch

# RPM dependency generator
install -m644 %{S:10} -D %{buildroot}%{_rpmconfigdir}/fileattrs/%{name}.attr
install -m755 %{S:11} -D %{buildroot}%{_rpmconfigdir}/%{name}.prov

%post
%{_sbindir}/setcap cap_net_bind_service,cap_net_admin+ep %{_libexecdir}/%{name}-%{api}/gst-ptp-helper

%files tools -f %{name}-%{api}.lang
%doc AUTHORS COPYING README NEWS
%dir %{_var}/cache/%{name}-%{api}
%{_bindir}/gst-inspect-%{api}
%{_bindir}/gst-launch-%{api}
%{_bindir}/gst-stats-%{api}
%{_bindir}/gst-typefind-%{api}
%dir %{_libdir}/%{name}-%{api}
%{_libexecdir}/%{name}-%{api}/gst-plugin-scanner
%caps(cap_net_bind_service,cap_net_admin+ep) %{_libexecdir}/%{name}-%{api}/gst-ptp-helper
%{_libexecdir}/%{name}-%{api}/gst-completion-helper
%{_libexecdir}/%{name}-%{api}/gst-hotdoc-plugins-scanner
%{_libexecdir}/%{name}-%{api}/gst-plugins-doc-cache-generator
%{_datadir}/bash-completion/completions/*
%{_datadir}/bash-completion/helpers/*
%{_libdir}/%{name}-%{api}/libgstcoreelements.so
%{_libdir}/%{name}-%{api}/libgstcoretracers.so
%{_mandir}/man1/gst-inspect-%{api}.1*
%{_mandir}/man1/gst-launch-%{api}.1*
%{_mandir}/man1/gst-stats-%{api}.1*
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
%dir %{_includedir}/%{name}-%{api}
%dir %{_includedir}/%{name}-%{api}/gst
%{_includedir}/%{name}-%{api}/gst/*.h
%dir %{_includedir}/%{name}-%{api}/gst/base/
%{_includedir}/%{name}-%{api}/gst/base/*.h
%{_includedir}/%{name}-%{api}/gst/check/
%dir %{_includedir}/%{name}-%{api}/gst/controller/
%{_includedir}/%{name}-%{api}/gst/controller/*.h
%{_includedir}/%{name}-%{api}/gst/net/
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
%if %{with docs}
%{_datadir}/gtk-doc/html/%{name}-%{api}/
%{_datadir}/gtk-doc/html/%{name}-libs-%{api}/
%{_datadir}/gtk-doc/html/%{name}-plugins-%{api}
%endif
%{_datadir}/gir-1.0/Gst-%{api}.gir
%{_datadir}/gir-1.0/GstBase-%{api}.gir
%{_datadir}/gir-1.0/GstCheck-%{api}.gir
%{_datadir}/gir-1.0/GstController-%{api}.gir
%{_datadir}/gir-1.0/GstNet-%{api}.gir
%{_rpmconfigdir}/fileattrs/%{name}.attr
%{_rpmconfigdir}/%{name}.prov
%{_datadir}/gdb/auto-load/%{_libdir}/*.py
%{_datadir}/%{name}-%{api}/gdb

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libgstreamer-%{api}.so.%{major}*
%dir %{_prefix}/lib/%{name}-%{api}
%{_prefix}/lib/%{name}-%{api}/libgstcoreelements.so
%{_prefix}/lib/%{name}-%{api}/libgstcoretracers.so

%files -n %{lib32gstbase}
%{_prefix}/lib/libgstbase-%{api}.so.%{major}*

%files -n %{lib32gstcheck}
%{_prefix}/lib/libgstcheck-%{api}.so.%{major}*

%files -n %{lib32gstcontroller}
%{_prefix}/lib/libgstcontroller-%{api}.so.%{major}*

%files -n %{lib32gstnet}
%{_prefix}/lib/libgstnet-%{api}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libgstbase-%{api}.so
%{_prefix}/lib/libgstcheck-%{api}.so
%{_prefix}/lib/libgstreamer-%{api}.so
%{_prefix}/lib/libgstnet-%{api}.so
%{_prefix}/lib/libgstcontroller-%{api}.so
%{_prefix}/lib/pkgconfig/gstreamer-%{api}.pc
%{_prefix}/lib/pkgconfig/gstreamer-base-%{api}.pc
%{_prefix}/lib/pkgconfig/gstreamer-check-%{api}.pc
%{_prefix}/lib/pkgconfig/gstreamer-net-%{api}.pc
%{_prefix}/lib/pkgconfig/gstreamer-controller-%{api}.pc
%{_datadir}/gdb/auto-load/%{_prefix}/lib/*.py
%endif
