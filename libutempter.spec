%define major 0
%define libname %mklibname utempter %{major}
%define devname %mklibname utempter -d

Summary:	Priviledged helper for utmp/wtmp updates
Name:		libutempter
Version:	1.2.3
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		ftp://ftp.altlinux.org/pub/people/ldv/utempter
Source0:	https://github.com/altlinux/libutempter/archive/%{version}-alt1/%{name}-%{version}-alt1.tar.gz
#Source0:	ftp://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		libutempter-pierelro.patch
Patch1:		libutempter-1.2.0-sanitize-linking-naming.patch
Requires:	%{libname} = %{EVRD}
Requires(pre):	shadow
%rename		utempter

%description
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.

%package -n %{libname}
Summary:	Library used by %{name}
Group:		System/Libraries

%description -n %{libname}
Libutempter is an library which allows some non-privileged
programs to have required root access without compromising system
security. It accomplishes this feat by acting as a buffer
between root and the programs.

%package -n %{devname}
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	utempter-devel = %{EVRD}
Requires:	%{name} = %{EVRD}
%rename		%{_lib}utempter0-devel

%description -n %{devname}
Header files for writing apps using libutempter.

%prep
%autosetup -n %{name}-%{version}-alt1 -p1

%build
%set_build_flags
%make_build CC="%{__cc}" CFLAGS="%{optflags}" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
%make_install libdir="%{_libdir}" libexecdir="%{_libexecdir}"

rm %{buildroot}%{_libdir}/libutempter.a
mkdir %{buildroot}%{_sbindir}
ln -sr %{buildroot}%{_libexecdir}/utempter/utempter %{buildroot}%{_sbindir}

%pre -p <lua>
st = posix.stat("/etc/mtab")
if st and st.type ~= "link" then
    posix.unlink("/etc/mtab")
end

if tonumber(arg[2]) >= 2 then
    if not posix.getgroup("utempter") then
	if not posix.exec("%{_sbindir}/groupadd", "-g", "35", "-r", "-f", "utempter") then
	    error("%{_sbindir}/groupadd: " ..  posix.errno())
	end
    end
end

%files
%attr(02755, root, utmp) %{_sbindir}/utempter
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
%{_mandir}/man3/*.3*

%files -n %{libname}
%{_libdir}/libutempter.so.%{major}*

%files -n %{devname}
%{_libdir}/libutempter.so
%{_includedir}/utempter.h
