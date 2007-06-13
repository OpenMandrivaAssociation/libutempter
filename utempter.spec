%define major 0
%define libname_orig lib%{name}
%define libname %mklibname %{name} %{major}


Summary:	Priviledged helper for utmp/wtmp updates
Name:		utempter
Version:	0.5.5
Release:	%mkrel 3
License:	GPL
Group:		System/Libraries
URL:		http://www.redhat.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		utempter-0.5.5-makevars.patch
Patch1:		utempter-0.5.2-biarch-utmp.patch
Requires(pre):	shadow-utils
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}--buildroot

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
Header files for writing apps using libutempter

%prep
%setup -q
%patch0 -p1 -b .makevars
%patch1 -p1 -b .biarch-utmp

%build
%make RPM_OPT_FLAGS="%{optflags}"

%install
rm -rf %{buildroot}
%makeinstall_std

ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}

%clean
rm -rf %{buildroot}

%pre 
%{_sbindir}/groupadd -g 22 -r -f utmp

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING
%attr(02755, root, utmp) %{_sbindir}/utempter

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libutempter.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libutempter.so
%{_includedir}/utempter.h
