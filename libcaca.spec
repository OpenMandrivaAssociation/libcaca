%define	prerel	beta18
%define	major	0
%define	libname	%mklibname caca %{major}
%define	libnamexx %mklibname caca++ %{major}
%define	libgl_plugin %mklibname libgl_plugin %{major}
%define	libx11_plugin %mklibname libx11_plugin %{major}
%define	devname %mklibname -d caca

%bcond_without	dox
%bcond_without	slang

Name:		libcaca
Version:	0.99
Release:	%{?prerel:0.%{prerel}.}1
Summary:	Text mode graphics library
License:	GPLv2
Group:		System/Libraries
URL:		http://libcaca.zoy.org/
Source0:	http://libcaca.zoy.org/attachment/wiki/libcaca/%{name}-%{version}%{?prerel:.%{prerel}}.tar.gz
Patch0:		libcaca-0.99.beta18-ruby1.9.patch

%if %{with slang}
Buildrequires:	pkgconfig(slang)
%endif
Buildrequires:	pkgconfig(glut)
Buildrequires:	pkgconfig(imlib2)
Buildrequires:	pkgconfig(ncursesw)
Buildrequires:	pkgconfig(pangoft2)
Buildrequires:	pkgconfig(x11)
%if %{with dox}
Buildrequires:	doxygen texlive
%endif
Buildrequires:	ruby-devel
%ifnarch %{mipsx} %{arm}
BuildRequires:	mono
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

%package -n	ruby-caca
Summary:	Ruby binding for libcaca
Group:		Development/Ruby

%description -n	ruby-caca
Ruby binding for libcaca

%package -n python-caca
Summary:	Python binding for libcaca
Group:		Development/Python

%description -n	python-caca
Python binding for libcaca

%prep
%setup -qn %{name}-%{version}%{?prerel:.%{prerel}}
%patch0 -p1 -b .ruby19~
autoreconf -fi

%build
%configure2_5x \
	--disable-static \
%if %{with slang}
	--enable-slang \
%else
	--disable-slang \
%endif
	--enable-ncurses \
	--enable-x11 \
	--enable-imlib2 \
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
# maybe b/c they are symlinks
rm -f %{buildroot}%{_libdir}/libcucul*.la

%multiarch_binaries %{buildroot}%{_bindir}/caca-config

%if %{with dox}
rm -rf installed-docs
mv %{buildroot}%{_datadir}/doc/libcaca-dev installed-docs
rm %{buildroot}%{_datadir}/doc/libcucul-dev
%endif

%files -n %{libname}
%{_libdir}/libcaca.so.%{major}*
%{_libdir}/libcucul.so.%{major}*

%files -n %{libnamexx}
%{_libdir}/libcaca++.so.%{major}*
%{_libdir}/libcucul++.so.%{major}*

%files -n %{libgl_plugin}
%{_libdir}/caca/libgl_plugin.so.%{major}*

%files -n %{libx11_plugin}
%{_libdir}/caca/libx11_plugin.so.%{major}*

%files -n %{devname}
%doc NEWS NOTES
%{_bindir}/caca-config
%{multiarch_bindir}/caca-config
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_libdir}/caca/lib*.so
%{_mandir}/man1/caca-config.1*
%if %{with dox}
%{_mandir}/man3/*
%doc installed-docs/pdf/* installed-docs/html 
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
%files -n caca-sharp
%{_libdir}/mono/caca-sharp*
%{_libdir}/mono/gac/caca-sharp
%endif

%files -n ruby-caca
%{ruby_sitelibdir}/caca.rb
%{ruby_sitearchdir}/*.so

%files -n python-caca
%{py_puresitedir}/caca


%changelog
* Tue Apr 10 2012 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta18.1
+ Revision: 790232
- add python binding
- update patch
- new version

* Thu Feb 23 2012 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 0.99-0.beta17.6
+ Revision: 779615
- buildrequires: s/tetex-latex tetex-dvips/texlive/
- hardcode release for conflicts, don't use macro...
- build docs by default
- make sure that we don't build docs if conditional is disabled
- cleanup spec
- explicitly disable java bindings (seems broken and is automatically enabled if
  javac is available on system, thus breaking build locally)

* Wed Feb 15 2012 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 0.99-0.beta17.5
+ Revision: 774604
- fix build with ruby 1.9 (P0)
- mass rebuild of ruby packages against ruby 1.9.1

* Thu Dec 22 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.99-0.beta17.4
+ Revision: 744259
- libcucul wasnt more than symlinks
- but the plugin are DSOs
- converted BRs to pkgconfig provides
- more fixes
- rebuild
- split up lib pkgs
- moved plugins to utils pkg
- cleaned up spec

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 0.99-0.beta17.3
+ Revision: 661607
- fix multiarch usage

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Mon Nov 29 2010 Funda Wang <fwang@mandriva.org> 0.99-0.beta17.2mdv2011.0
+ Revision: 602958
- reduce BR
- update file list

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Mon Feb 08 2010 Pascal Terjan <pterjan@mandriva.org> 0.99-0.beta17.1mdv2010.1
+ Revision: 502259
- Update to beta17

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - fix devel provides

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 0.99-0.beta16.5mdv2010.0
+ Revision: 449857
- fix libtool troubles (from Arnaud Patard)
- disable mono on arm too
- disable mono on mips (from Arnaud Patard)

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.99-0.beta16.4mdv2010.0
+ Revision: 425523
- rebuild

  + Pascal Terjan <pterjan@mandriva.org>
    - Use plugins to not link the lib against X

* Fri Nov 07 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta16.2mdv2009.1
+ Revision: 300541
- rebuild for new libxcb

* Sat Oct 18 2008 Pascal Terjan <pterjan@mandriva.org> 0.99-0.beta16.1mdv2009.1
+ Revision: 294925
- Update to beta16

* Tue Oct 14 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta15.3mdv2009.1
+ Revision: 293564
- fix pkgconfig file

* Sat Oct 11 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta15.2mdv2009.1
+ Revision: 292189
- rebuild
- new version
- update file list

* Fri Jul 18 2008 Pascal Terjan <pterjan@mandriva.org> 0.99-0.beta14.1mdv2009.0
+ Revision: 238226
- Update to beta 14
- Disable --no-undefined for ruby binding

* Fri Jun 13 2008 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta13.2mdv2009.0
+ Revision: 218743
- 0.99beta13b
- new version
- drop ruby patch
- patch for gcc 4.3

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Pascal Terjan <pterjan@mandriva.org>
    - Update URL
    - Fix license

* Thu Nov 29 2007 Pascal Terjan <pterjan@mandriva.org> 0.99-0.beta13.1mdv2008.1
+ Revision: 113868
- update to 0.99 beta13
- build C# and Ruby bindings

* Mon Oct 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta12.1mdv2008.1
+ Revision: 101111
- new version
- drop patch
- new devel name

  + Thierry Vignaud <tv@mandriva.org>
    - replace %%{_datadir}/man by %%{_mandir}!

* Fri Jun 01 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.99-0.beta11.2mdv2008.0
+ Revision: 34314
- Rebuild with libslang2.


* Mon Dec 04 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.99-0.beta11.1mdv2007.0
+ Revision: 90333
- Import libcaca

* Mon Dec 04 2006 Götz Waschk <waschk@mandriva.org> 0.99-0.beta11.1mdv2007.1
- fix buildrequires
- rediff patch 1
- add library package
- drop patch 0
- new version

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9-15mdv2007.0
- Rebuild

* Thu Jun 15 2006 Götz Waschk <waschk@mandriva.org> 0.9-14mdv2007.0
- disable slang on x86_64 to make it build

* Wed Jun 14 2006 Götz Waschk <waschk@mandriva.org> 0.9-13mdv2007.0
- remove debug files
- fix devel deps

* Tue May 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.9-12mdk
- fix requires

* Sat May 20 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.9-11mdk
- fix buildrequires

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.9-10mdk
- Rebuild

* Thu Aug 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.9-9mdk
- Rebuild

* Sun Feb 20 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9-8mdk
- Patch1: fix a4wide check for new file location

* Mon Jan 31 2005 Götz Waschk <waschk@linux-mandrake.com> 0.9-7mdk
- multiarch support

* Sat Aug 07 2004 Götz Waschk <waschk@linux-mandrake.com> 0.9-6mdk
- really fix buildrequires

* Thu Aug 05 2004 Götz Waschk <waschk@linux-mandrake.com> 0.9-4mdk
- patch to fix man pages build

* Sat May 01 2004 Götz Waschk <waschk@linux-mandrake.com> 0.9-3mdk
- fix 9.0 build

* Sat Feb 07 2004 Götz Waschk <waschk@linux-mandrake.com> 0.9-2mdk
- fix directory ownership

* Mon Feb 02 2004 Götz Waschk <waschk@linux-mandrake.com> 0.9-1mdk
- new version

* Mon Feb 02 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.9-1
- new release

* Sun Jan 18 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.8-1
- new release

* Wed Jan 07 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.7-1
- new release

* Sun Jan 04 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-2
- install documentation into {doc}/package-version instead of {doc}/package
- added tetex-dvips to the build dependencies

* Sat Jan 03 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-1
- new release
- more detailed descriptions
- split the RPM into libcaca-devel and caca-utils
- packages are rpmlint clean

* Mon Dec 29 2003 Richard Zidlicky <rz@linux-m68k.org> 0.5-1
- created specfile

