%define name libcaca
%define version 0.99
%define pre beta16
%define release %mkrel 0.%pre.3
%define build_slang 1

%define major 0
%define libname %mklibname caca %major
%define develname %mklibname -d caca

Name: %{name}
Version: %{version}
Release: %{release}
URL: http://libcaca.zoy.org/
Source: http://libcaca.zoy.org/attachment/wiki/libcaca/%{name}-%{version}.%pre.tar.gz
License: WTFPL
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
Buildrequires: ruby-devel mono

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


%package -n %develname
Summary: Development files for libcaca
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Requires: %libname = %version
Obsoletes: %mklibname -d caca 0

%description -n %develname
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

%package -n caca-sharp
Summary: C# binding for libcaca
Group: Development/Other

%description -n caca-sharp
C# binding for libcaca

%package -n ruby-caca
Summary: Ruby binding for libcaca
Group: Development/Ruby

%description -n ruby-caca
Ruby binding for libcaca

%prep
%setup -q -n %name-%version.%pre

%build
%configure2_5x \
%if %build_slang
  --enable-slang \
%else
  --disable-slang \
%endif
--enable-ncurses --enable-x11 --enable-imlib2 --enable-doc --enable-plugins

%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std
%multiarch_binaries %buildroot%_bindir/caca-config
mv %{buildroot}%{_datadir}/doc/libcaca-dev installed-docs
mkdir %{buildroot}%{_datadir}/doc/caca-utils-%{version}
rm %buildroot%{_datadir}/doc/libcucul-dev

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*
# FIXME split them into subpackage, to avoid dependency on X
%_libdir/caca/lib*.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%doc installed-docs/pdf/* installed-docs/html NEWS NOTES
%{_bindir}/caca-config
%_bindir/*/caca-config
%{_includedir}/*
%{_mandir}/man1/caca-config.1*
%{_mandir}/man3/*
%_libdir/pkgconfig/*.pc
%_libdir/lib*.so
%_libdir/lib*a
%_libdir/caca/lib*.so
%_libdir/caca/lib*a

%files -n caca-utils
%defattr(-,root,root)
%doc README THANKS AUTHORS
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%_bindir/img2txt
%{_datadir}/libcaca/
%{_mandir}/man1/cacademo.1*
%{_mandir}/man1/cacafire.1*
%{_mandir}/man1/cacaplay.1*
%{_mandir}/man1/cacaserver.1*
%{_mandir}/man1/cacaview.1*
%_mandir/man1/img2txt.1*

%files -n caca-sharp
%{_libdir}/caca-sharp/caca-sharp.dll
%{_libdir}/caca-sharp/caca-sharp.dll.config

%files -n ruby-caca
%{ruby_sitelibdir}/caca.rb
%{ruby_sitearchdir}/*.so
%exclude %{ruby_sitearchdir}/*a
