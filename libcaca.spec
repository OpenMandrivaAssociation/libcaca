%define name libcaca
%define version 0.99
%define pre beta11
%define release %mkrel 0.%pre.2
%define build_slang 1
#%ifarch x86_64
#define build_slang 0
#%endif

%define major 0
%define libname %mklibname caca %major

Name: %{name}
Version: %{version}
Release: %{release}
URL: http://sam.zoy.org/projects/libcaca/
Source: http://sam.zoy.org/projects/libcaca/%{name}-%{version}.%pre.tar.bz2
Patch1: libcaca-0.99.beta11-a4wide.patch
License: GPL
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Buildrequires: X11-devel, libncursesw-devel >= 5
%if %build_slang
Buildrequires: slang-devel
%endif
Buildrequires: imlib2-devel
Buildrequires: libpango-devel
Buildrequires: libmesaglut-devel
Buildrequires: doxygen, tetex-latex, tetex-dvips
Buildrequires: automake1.7

Summary: Text mode graphics library
%description
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

%package -n %libname
Summary: Text mode graphics library
Group: System/Libraries

%description -n %libname
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.


%package -n %{libname}-devel
Summary: Development files for libcaca
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{name}-devel
Provides: lib%{name}-devel = %{version}-%{release}
Requires: %libname = %version

%description -n %{libname}-devel
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the header files and static libraries needed to
compile applications or shared objects that use libcaca.

%package -n caca-utils
Summary: Text mode graphics utilities
Group: Graphics
%description -n caca-utils
This package contains utilities and demonstration programs for libcaca, the
Colour AsCii Art library.

cacaview is a simple image viewer for the terminal. It opens most image
formats such as JPEG, PNG, GIF etc. and renders them on the terminal using
ASCII art. The user can zoom and scroll the image, set the dithering method
or enable anti-aliasing.

cacaball is a tiny graphic program that renders animated ASCII metaballs on
the screen, cacafire is a port of AALib's aafire and displays burning ASCII
art flames, cacamoir animates colourful moire circles and cacaplas displays
an old school plasma effect.

cacademo is a simple application that shows the libcaca rendering features
such as line and ellipses drawing, triangle filling and sprite blitting.

%prep
%setup -q -n %name-%version.%pre
%patch1 -p1 -b .a4wide
aclocal-1.7
automake-1.7 -a -c
autoconf

%build
%configure2_5x \
%if %build_slang
  --enable-slang \
%else
  --disable-slang \
%endif
--enable-ncurses --enable-x11 --enable-imlib2 --enable-doc
%make 

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std
%multiarch_binaries %buildroot%_bindir/caca-config
mv %{buildroot}%{_datadir}/doc/libcucul-dev installed-docs
mkdir %{buildroot}%{_datadir}/doc/caca-utils-%{version}

%clean
rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc installed-docs/pdf/* installed-docs/html NEWS NOTES TODO
%{_bindir}/caca-config
%_bindir/*/caca-config
%{_includedir}/*
%{_datadir}/man/man1/caca-config.1*
%{_datadir}/man/man3/*
%_libdir/pkgconfig/*.pc
%_libdir/lib*.so
%_libdir/lib*a


%files -n caca-utils
%defattr(-,root,root)
%doc README THANKS AUTHORS
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%_bindir/img2irc
%{_datadir}/libcaca/
%{_mandir}/man1/cacademo.1*
%{_mandir}/man1/cacafire.1*
%{_mandir}/man1/cacaplay.1*
%{_mandir}/man1/cacaserver.1*
%{_mandir}/man1/cacaview.1*
%_mandir/man1/img2irc.1*


