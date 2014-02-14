%define	major	0
%define	libname	%mklibname utempter %{major}
%define	devname	%mklibname utempter -d

%bcond_without	uclibc

Summary:	Priviledged helper for utmp/wtmp updates
Name:		libutempter
Version:	1.1.6
Release:	3
License:	GPLv2+
Group:		System/Libraries
URL:		ftp://ftp.altlinux.org/pub/people/ldv/utempter
Source0:	ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.bz2
# Compile with PIE and RELRO flags.
Patch0:		libutempter-pierelro.patch
Patch1:		libutempter-1.1.6-sanitize-linking-naming.patch
Requires(pre):	shadow-utils
Requires:	%{libname} = %{version}-%{release}
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif
%rename		utempter

%description
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	uclibc-%{name}
Summary:	Priviledged helper for utmp/wtmp updates (uClibc build)
Group:		System/Libraries
%rename		uclibc-utempter

%description -n	uclibc-%{name}
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

%package -n	uclibc-%{name}
Summary:	Priviledged helper for utmp/wtmp updates (uClibc build)
Group:		System/Libraries
Requires:	uclibc-%{libname} = %{EVRD}

%description -n	uclibc-%{name}
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	uclibc-%{libname}
Summary:	Library used by %{name} (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
Libutempter is an library which allows some non-privileged
programs to have required root access without compromising system
security. It accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	%{devname}
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	utempter-devel = %{EVRD}}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif
%rename		%{_lib}utempter0-devel

%description -n	%{devname}
Header files for writing apps using libutempter.

%prep
%setup -q
%patch0 -p1 -b .pierelro~
%patch1 -p1 -b .linknaming~
%if %{with uclibc}
mkdir .uclibc
cp -a * .uclibc
%endif

%build
%if %{with uclibc}
pushd .uclibc
%make CC="%{uclibc_cc}" CFLAGS="%{uclibc_cflags}" libdir="%{uclibc_root}%{_libdir}" libexecdir="%{uclibc_root}%{_libexecdir}"
popd
%endif

%make CC="%{__cc}" CFLAGS="%{optflags}" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
%if %{with uclibc}
%makeinstall_std -C .uclibc bindir="%{uclibc_root}%{_sbindir}" libdir="%{uclibc_root}%{_libdir}" libexecdir="%{uclibc_root}%{_libexecdir}"
rm -r %{buildroot}%{_mandir}
rm %{buildroot}%{uclibc_root}%{_libdir}/libutempter.a
mkdir %{buildroot}%{uclibc_root}%{_sbindir}
ln -sr %{buildroot}%{uclibc_root}%{_libexecdir}/utempter/utempter %{buildroot}%{uclibc_root}%{_sbindir}
%endif

%makeinstall_std libdir="%{_libdir}" libexecdir="%{_libexecdir}"
rm %{buildroot}%{_libdir}/libutempter.a
mkdir %{buildroot}%{_sbindir}
ln -sr %{buildroot}%{_libexecdir}/utempter/utempter %{buildroot}%{_sbindir}

%pre 
%{_sbindir}/groupadd -g 35 -r -f utempter

%files
%attr(02755, root, utmp) %{_sbindir}/utempter
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
%{_mandir}/man3/*.3*

%if %{with uclibc}
%files -n uclibc-%{name}
%attr(02755, root, utmp) %{uclibc_root}%{_sbindir}/utempter
%dir %attr(755,root,utempter) %{uclibc_root}%{_libexecdir}/utempter
%attr(2755,root,utmp) %{uclibc_root}%{_libexecdir}/utempter/utempter
%endif

%files -n %{libname}
%{_libdir}/libutempter.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libutempter.so.%{major}*
%endif

%files -n %{devname}
%{_libdir}/libutempter.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libutempter.so
%endif
%{_includedir}/utempter.h
