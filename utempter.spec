%define	major	0
%define	libname	%mklibname %{name} %{major}

%bcond_without	uclibc

Summary:	Priviledged helper for utmp/wtmp updates
Name:		utempter
Version:	0.5.5
Release:	17
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.redhat.com/
Source0:	%{name}-%{version}.tar.bz2
Patch1:		utempter-0.5.2-biarch-utmp.patch
Requires(pre):	shadow-utils
Requires:	%{libname} = %{version}-%{release}
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

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

%package -n	%{libname}-devel
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}-%{release}
%endif

%description -n	%{libname}-devel
Header files for writing apps using libutempter.

%prep
%setup -q
%patch1 -p1 -b .biarch-utmp
%if %{with uclibc}
mkdir .uclibc
cp -a * .uclibc
%endif

%build
%if %{with uclibc}
pushd .uclibc
%make CC="%{uclibc_cc}" AR="%{__ar}" RANLIB="%{__ranlib}"  RPM_OPT_FLAGS="%{uclibc_cflags}"
popd
%endif

%make CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}"  RPM_OPT_FLAGS="%{optflags}"

%install
%if %{with uclibc}
%makeinstall_std -C .uclibc PREFIX=%{uclibc_root} LIBDIR=%{uclibc_root}%{_libdir}
mv %{buildroot}%{_sbindir} %{buildroot}%{uclibc_root}%{_prefix}
%endif

%makeinstall_std LIBDIR=%{_libdir}

%pre 
%{_sbindir}/groupadd -g 22 -r -f utmp

%files
%attr(02755, root, utmp) %{_sbindir}/utempter

%files -n %{libname}
%{_libdir}/libutempter.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{name}
%attr(02755, root, utmp) %{uclibc_root}%{_sbindir}/utempter

%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libutempter.so.%{major}*
%endif

%files -n %{libname}-devel
%{_libdir}/libutempter.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libutempter.so
%endif
%{_includedir}/utempter.h
