%define prerel beta20
%define major 0
%define libname %mklibname caca %{major}
%define libnamexx %mklibname caca++ %{major}
%define libgl_plugin %mklibname libgl_plugin %{major}
%define libx11_plugin %mklibname libx11_plugin %{major}
%define devname %mklibname -d caca

%bcond_with dox
%bcond_with mono
%bcond_without ruby
%bcond_without slang

Summary:	Text mode graphics library
Name:		libcaca
Version:	0.99
Release:	%{?prerel:0.%{prerel}.}1
License:	GPLv2
Group:		System/Libraries
Url:		http://caca.zoy.org/wiki/libcaca
Source0:	https://github.com/cacalabs/libcaca/releases/download/v%{version}.%{prerel}/libcaca-%{version}.%{prerel}.tar.bz2
#Source0:	http://caca.zoy.org/files/libcaca/%{name}-%{version}%{?prerel:.%{prerel}}.tar.gz
Patch0:		libcaca-0.99-arm.patch

%if %{with slang}
BuildRequires:	pkgconfig(slang)
%endif
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(x11)
%if %{with dox}
BuildRequires:	doxygen
BuildRequires:	texlive
%endif
%if %{with ruby}
BuildRequires:	ruby-devel
%endif
%ifnarch %{mipsx} %{arm} aarch64
%if %{with mono}
BuildRequires:	mono
%endif
%endif

%description
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

%package -n	%{libname}
Summary:	Text mode graphics library
Group:		System/Libraries

%description -n	%{libname}
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the shared library for %{name}.

%package -n	%{libnamexx}
Summary:	Text mode graphics library
Group:		System/Libraries
Conflicts:	%{libname} < 0.99-0.beta17.4

%description -n	%{libnamexx}
This package contains the shared library for %{name}++.

%package -n	%{libgl_plugin}
Summary:	Text mode graphics library
Group:		System/Libraries
Conflicts:	%{libname} < 0.99-0.beta17.4

%description -n	%{libgl_plugin}
This package contains the shared library libgl_plugin.

%package -n	%{libx11_plugin}
Summary:	Text mode graphics library
Group:		System/Libraries
Conflicts:	%{libname} < 0.99-0.beta17.4

%description -n	%{libx11_plugin}
This package contains the shared library libgl_plugin.

%package -n	%{devname}
Summary:	Development files for libcaca
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnamexx} = %{version}-%{release}
Requires:	%{libgl_plugin} = %{version}-%{release}
Requires:	%{libx11_plugin} = %{version}-%{release}
Obsoletes:	%{mklibname -d caca 0} < 0.99-0.beta18

%description -n	%{devname}
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the header files and static libraries needed to
compile applications or shared objects that use libcaca.

%package -n	caca-utils
Summary:	Text mode graphics utilities
Group:		Graphics
Conflicts:	%{libname} < 0.99-0.beta17.4

%description -n	caca-utils
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

%ifnarch %{mipsx} %{arm}
%package -n	caca-sharp
Summary:	Mono binding for libcaca
Group:		Development/Other

%description -n	caca-sharp
Mono binding for libcaca
%endif

%if %{with ruby}
%package -n	ruby-caca
Summary:	Ruby binding for libcaca
Group:		Development/Ruby

%description -n	ruby-caca
Ruby binding for libcaca
%endif

%package -n python-caca
Summary:	Python binding for libcaca
Group:		Development/Python

%description -n	python-caca
Python binding for libcaca

%prep
%setup -qn %{name}-%{version}%{?prerel:.%{prerel}}
%autopatch -p1

#(tpg) fix build with automake-1.13
#sed -i s/AM_CONFIG_HEADER/AC_CONFIG_HEADER/ configure.ac

autoreconf -fi

%build
%configure \
%if %{with slang}
	--enable-slang \
%else
	--disable-slang \
%endif
	--enable-ncurses \
	--enable-x11 \
	--enable-imlib2 \
	--enable-cxx \
%if %{with dox}
	--enable-doc \
%else
	--disable-doc \
%endif
	--enable-plugins \
	--disable-java

%make

%install
%makeinstall_std

%if %{with dox}
rm -rf installed-docs
mv %{buildroot}%{_datadir}/doc/libcaca-dev installed-docs
%endif

%files -n %{libname}
%{_libdir}/libcaca.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libcaca++.so.%{major}*

%files -n %{libgl_plugin}
%{_libdir}/caca/libgl_plugin.so.%{major}*

%files -n %{libx11_plugin}
%{_libdir}/caca/libx11_plugin.so.%{major}*

%files -n %{devname}
%doc NEWS NOTES
%{_bindir}/caca-config
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_libdir}/caca/lib*.so
%{_mandir}/man1/caca-config.1*
%if %{with dox}
%{_mandir}/man3/*
%doc installed-docs/html
%endif

%files -n caca-utils
%doc README THANKS AUTHORS
%{_bindir}/cacaclock
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%{_bindir}/img2txt
%{_datadir}/libcaca/
%{_mandir}/man1/cacademo.1*
%{_mandir}/man1/cacafire.1*
%{_mandir}/man1/cacaplay.1*
%{_mandir}/man1/cacaserver.1*
%{_mandir}/man1/cacaview.1*
%{_mandir}/man1/img2txt.1*

%ifnarch %{mips} %{arm}
%if %{with mono}
%files -n caca-sharp
%{_libdir}/mono/caca-sharp*
%{_libdir}/mono/gac/caca-sharp
%endif
%endif

%if %{with ruby}
%files -n ruby-caca
%{ruby_sitearchdir}/*.so
%{ruby_sitelibdir}/*.rb

%endif

%files -n python-caca
%{py_puresitedir}/caca
