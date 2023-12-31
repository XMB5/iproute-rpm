Summary:            Advanced IP routing and network device configuration tools
Name:               iproute
Version:            6.4.0
Release:            %autorelease
%if 0%{?rhel}
Group:              Applications/System
%endif
URL:                https://kernel.org/pub/linux/utils/net/%{name}2/
Source0:            https://kernel.org/pub/linux/utils/net/%{name}2/%{name}2-%{version}.tar.xz
Source100:          colorip.sh
Source101:          colorip.csh
Source102:          colortc.sh
Source103:          colortc.csh


License:            GPL-2.0-or-later AND NIST-PD
BuildRequires:      bison
BuildRequires:      elfutils-libelf-devel
BuildRequires:      flex
BuildRequires:      gcc
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libbpf-devel
BuildRequires:      libcap-devel
BuildRequires:      libdb-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      make
BuildRequires:      pkgconfig
%if ! 0%{?_module_build}
%if 0%{?fedora}
BuildRequires:      linux-atm-libs-devel
%endif
%endif
Requires:           libbpf
Requires:           psmisc
Provides:           /sbin/ip

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.

%package tc
Summary:            Linux Traffic Control utility
%if 0%{?rhel}
Group:              Applications/System
%endif
License:            GPL-2.0-or-later
Requires:           %{name}%{?_isa} = %{version}-%{release}
Provides:           /sbin/tc

%description tc
The Traffic Control utility manages queueing disciplines, their classes and
attached filters and actions. It is the standard tool to configure QoS in
Linux.

%if ! 0%{?_module_build}
%package doc
Summary:            Documentation for iproute2 utilities with examples
%if 0%{?rhel}
Group:              Applications/System
%endif
License:            GPL-2.0-or-later
Requires:           %{name} = %{version}-%{release}

%description doc
The iproute documentation contains howtos and examples of settings.
%endif

%package devel
Summary:            iproute development files
%if 0%{?rhel}
Group:              Development/Libraries
%endif
License:            GPL-2.0-or-later
Requires:           %{name} = %{version}-%{release}
Provides:           iproute-static = %{version}-%{release}

%description devel
The libnetlink static library.

%prep
%autosetup -p1 -n %{name}2-%{version}

%build
%configure --libdir %{_libdir}
echo -e "\nPREFIX=%{_prefix}\nCONFDIR:=%{_sysconfdir}/iproute2\nSBINDIR=%{_sbindir}" >> config.mk
%make_build

%install
%make_install

# ip command colorization
%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE100} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE101} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE102} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE103} %{buildroot}%{profiledir}

echo '.so man8/tc-cbq.8' > %{buildroot}%{_mandir}/man8/cbq.8

# libnetlink
install -D -m644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -D -m644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a

# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_docdir}'

# append deprecated values to rt_dsfield for compatibility reasons
%if 0%{?rhel} && ! 0%{?eln}
cat %{SOURCE1} >>%{buildroot}%{_sysconfdir}/iproute2/rt_dsfield
%endif

%files
%dir %{_sysconfdir}/iproute2
%license COPYING
%doc README README.devel
%{_mandir}/man7/*
%exclude %{_mandir}/man7/tc-*
%{_mandir}/man8/*
%exclude %{_mandir}/man8/tc*
%exclude %{_mandir}/man8/cbq*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%exclude %{_sbindir}/tc
%exclude %{_sbindir}/routel
%{_datadir}/bash-completion/completions/devlink
%{profiledir}/colorip.*

%files tc
%license COPYING
%{_mandir}/man7/tc-*
%{_mandir}/man8/tc*
%{_mandir}/man8/cbq*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%{_sbindir}/tc
%{_datadir}/bash-completion/completions/tc
%{profiledir}/colortc.*

%if ! 0%{?_module_build}
%files doc
%license COPYING
%doc examples
%endif

%files devel
%license COPYING
%{_mandir}/man3/*
%{_libdir}/libnetlink.a
%{_includedir}/libnetlink.h
%{_includedir}/iproute2/bpf_elf.h

%changelog
%autochangelog
