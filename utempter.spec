%define	name	utempter
%define	version	0.5.5
%define	release	%mkrel 2

%define major		0
%define lib_name_orig	lib%{name}
%define lib_name	%mklibname %{name} %{major}


Summary:	Priviledged helper for utmp/wtmp updates
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.redhat.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		utempter-0.5.5-makevars.patch
Patch1:		utempter-0.5.2-biarch-utmp.patch
Prereq:		/usr/sbin/groupadd /sbin/ldconfig fileutils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	%{lib_name} = %{version}

%description
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	%{lib_name}
Summary:	Library used by %{name}
Group:		System/Libraries

%description -n	%{lib_name}
Libutempter is an library which allows some non-privileged
programs to have required root access without compromising system
security. It accomplishes this feat by acting as a buffer
between root and the programs.

%package -n	%{lib_name}-devel
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	%{lib_name_orig}-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}

%description -n	%{lib_name}-devel
Header files for writing apps using libutempter

%prep
%setup -q
%patch0 -p1 -b .makevars
%patch1 -p1 -b .biarch-utmp

%build
%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall}

ln -sf lib%{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.%{major}

%clean
rm -rf $RPM_BUILD_ROOT

%pre 
%{_sbindir}/groupadd -g 22 -r -f utmp

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc COPYING
%attr(02755, root, utmp) %{_sbindir}/utempter

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libutempter.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libutempter.so
%{_includedir}/utempter.h


