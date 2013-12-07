%define major 0
%define libname_orig lib%{name}
%define libname %mklibname %{name} %{major}

Summary:	Priviledged helper for utmp/wtmp updates
Name:		utempter
Version:	0.5.5
Release:	19
License:	GPL
Group:		System/Libraries
URL:		http://www.redhat.com/
Source0:	%{name}-%{version}.tar.bz2
Patch1:		utempter-0.5.2-biarch-utmp.patch
Requires(pre):	shadow-utils
Requires:	%{libname} = %{version}-%{release}

%description
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	%{libname}
Summary:	Library used by %{name}
Group:		System/Libraries

%description -n	%{libname}
Libutempter is an library which allows some non-privileged
programs to have required root access without compromising system
security. It accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	%{libname}-devel
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
Header files for writing apps using libutempter.

%prep
%setup -q
%patch1 -p1 -b .biarch-utmp

%build
%make CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}"  RPM_OPT_FLAGS="%{optflags}"

%install
%makeinstall_std LIBDIR=%{_libdir}

chmod 0755 %{buildroot}%{_libdir}/libutempter.so.%{major}*

# Workaround for a debuginfo bug
%{__strip} %{buildroot}%{_libdir}/*.so*

%pre 
%{_sbindir}/groupadd -g 22 -r -f utmp

%files
%attr(02755, root, utmp) %{_sbindir}/utempter

%files -n %{libname}
%{_libdir}/libutempter.so.%{major}*

%files -n %{libname}-devel
%doc COPYING
%{_libdir}/libutempter.so
%{_includedir}/utempter.h


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.5.5-12mdv2011.0
+ Revision: 670756
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.5-11mdv2011.0
+ Revision: 608118
- rebuild

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.5.5-10mdv2010.1
+ Revision: 540363
- rebuild so that shared libraries are properly stripped again

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 0.5.5-9mdv2010.1
+ Revision: 540043
- rebuild so that shared libraries are properly stripped again

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.5-8mdv2010.1
+ Revision: 524306
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.5.5-7mdv2010.0
+ Revision: 427485
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.5.5-6mdv2009.1
+ Revision: 351444
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.5.5-5mdv2009.0
+ Revision: 225913
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5.5-4mdv2008.1
+ Revision: 179674
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Jun 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.5.5-3mdv2008.0
+ Revision: 38648
- drop patch 0 (it only spoils things)
- drop prereq, use instead requires(pre)
- spec file clean
- adjust requires/provides


* Sun Jan 14 2007 Götz Waschk <waschk@mandriva.org> 0.5.5-2mdv2007.0
+ Revision: 108712
- Import utempter

* Sun Jan 14 2007 Götz Waschk <waschk@mandriva.org> 0.5.5-2mdv2007.1
- drop patch

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.5.5-2mdk
- Rebuild

* Fri Dec 17 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.5.5-1mdk
- 0.5.5
- regenerate P0
- fix provides
- cleanups

* Thu Apr 22 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-13mdk
- security update, issue uncovered by Steve Grubb (patch2)

