%define prerel beta17
%define major 0
%define libname %mklibname caca %{major}
%define libnamexx %mklibname caca++ %{major}
%define libcucul %mklibname cucul %{major}
%define libcuculxx %mklibname cucul++ %{major}
%define develname %mklibname -d caca

%define build_slang 1

Name: libcaca
Version: 0.99
Release: 0.%{prerel}.4
License: WTFPL
Group: System/Libraries
URL: http://libcaca.zoy.org/
Source0: http://libcaca.zoy.org/attachment/wiki/libcaca/%{name}-%{version}.%pre.tar.gz

Buildrequires: libx11-devel, libncursesw-devel >= 5
%if %build_slang
Buildrequires: slang-devel
%endif
Buildrequires: imlib2-devel
Buildrequires: libpango-devel
Buildrequires: libmesaglut-devel
Buildrequires: doxygen, tetex-latex, tetex-dvips
Buildrequires: ruby-devel
%ifnarch %mips %arm
BuildRequires: mono
%endif

Summary: Text mode graphics library
%description
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

%package -n %{libname}
Summary: Text mode graphics library
Group: System/Libraries

%description -n %{libname}
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the shared library for %{name}.

%package -n %{libnamexx}
Summary: Text mode graphics library
Group: System/Libraries
Conflicts: %{libname} < 0.99-0.%{prerel}.4

%description -n %{libnamexx}
This package contains the shared library for %{name}++.

%package -n %{libcucul}
Summary: Text mode graphics library
Group: System/Libraries
Conflicts: %{libname} < 0.99-0.%{prerel}.4

%description -n %{libcucul}
This package contains the shared library libcucul.

%package -n %{libcuculxx}
Summary: Text mode graphics library
Group: System/Libraries
Conflicts: %{libname} < 0.99-0.%{prerel}.4

%description -n %{libcuculxx}
This package contains the shared library libcucul++.

%package -n %{develname}
Summary: Development files for libcaca
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}
Requires: %{libnamexx} = %{version}-%{release}
Requires: %{libcucul} = %{version}-%{release}
Requires: %{libcuculxx} = %{version}-%{release}
Obsoletes: %mklibname -d caca 0

%description -n %{develname}
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the header files and static libraries needed to
compile applications or shared objects that use libcaca.

%package -n caca-utils
Summary: Text mode graphics utilities
Group: Graphics
Conflicts: %{libname} < 0.99-0.%{prerel}.4

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

%ifnarch %mips %arm
%package -n caca-sharp
Summary: C# binding for libcaca
Group: Development/Other

%description -n caca-sharp
Mono binding for libcaca
%endif

%package -n ruby-caca
Summary: Ruby binding for libcaca
Group: Development/Ruby

%description -n ruby-caca
Ruby binding for libcaca

%prep
%setup -qn %{name}-%{version}.%prerel

%build
%configure2_5x \
	--disable-static \
%if %build_slang
	--enable-slang \
%else
	--disable-slang \
%endif
	--enable-ncurses \
	--enable-x11 
	--enable-imlib2 \
	--enable-doc \
	--enable-plugins

%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std

rm -f %{buildroot}%{ruby_sitearchdir}/*.la

%multiarch_binaries %{buildroot}%{_bindir}/caca-config

mv %{buildroot}%{_datadir}/doc/libcaca-dev installed-docs
mkdir %{buildroot}%{_datadir}/doc/caca-utils-%{version}
rm %{buildroot}%{_datadir}/doc/libcucul-dev

%files -n %{libname}
%{_libdir}/libcaca.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libcaca++.so.%{major}*

%files -n %{libcucul}
%{_libdir}/libcucul.so.%{major}*

%files -n %{libcuculxx}
%{_libdir}/libcucul++.so.%{major}*

%files -n %{develname}
%doc installed-docs/pdf/* installed-docs/html NEWS NOTES
%{_bindir}/caca-config
%{multiarch_bindir}/caca-config
%{_includedir}/*
%{_mandir}/man1/caca-config.1*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_libdir}/caca/lib*.so

%files -n caca-utils
%doc README THANKS AUTHORS
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%{_bindir}/img2txt
%{_libdir}/caca/lib*.so.%{major}*
%{_datadir}/libcaca/
%{_mandir}/man1/cacademo.1*
%{_mandir}/man1/cacafire.1*
%{_mandir}/man1/cacaplay.1*
%{_mandir}/man1/cacaserver.1*
%{_mandir}/man1/cacaview.1*
%{_mandir}/man1/img2txt.1*

%ifnarch %mips %arm
%files -n caca-sharp
%{_libdir}/mono/caca-sharp*
%{_libdir}/mono/gac/caca-sharp
%endif

%files -n ruby-caca
%{ruby_sitelibdir}/caca.rb
%{ruby_sitearchdir}/*.so

