Summary: Enhanced IP routing and network devices configuration tools
Name: iproute
Version: 2.2.4
Release: 10
Group: Applications/System
Source: ftp://ftp.inr.ac.ru/ip-routing/iproute2-current.tar.gz
Patch0: iproute2-2.2.4-docmake.patch
Patch1: iproute2-2.2.4-glibc22.patch
Patch2: iproute2-misc.patch
Patch3: iproute2-config.patch
Copyright: GPL
BuildRoot: %{_tmppath}/%{name}-root

%description
Linux 2.2 maintains compatibility with the basic configuration utilities of
the network (ifconfig, route) but a new utility is required to exploit the new
characteristics and features of the kernel. This package includes the new
utilities (/sbin/ip, /sbin/rtmon).

%prep
%setup -q -n iproute2
%patch0 -p1 -b .doc
%patch1 -p1 -b .glibc22
%patch2 -p1 -b .misc
%patch3 -p1

%build
if [ -d /usr/src/linux-2.4 ]; then
    make KERNEL_INCLUDE=/usr/src/linux-2.4/include
elif [ -d /usr/src/linux ]; then
    make KERNEL_INCLUDE=/usr/src/linux/include
else
    make
fi
make -C doc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin \
 	 $RPM_BUILD_ROOT%{_sbindir} \
         $RPM_BUILD_ROOT/etc/iproute2

install -s -m 755 ip/ip ip/ifcfg ip/rtmon tc/tc $RPM_BUILD_ROOT/sbin
install -s -m 755 ip/rtacct $RPM_BUILD_ROOT%{_sbindir}

cp -f etc/iproute2/* $RPM_BUILD_ROOT/etc/iproute2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /etc/iproute2
%doc README.decnet README.iproute2+tc RELNOTES
%doc doc/*.ps examples
/sbin/*
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
%{_sbindir}/*

%changelog
* Sat Jan  6 2001 Jeff Johnson <jbj@redhat.com>
- test for specific KERNEL_INCLUDE directories.

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- rebuild for 7.1

* Thu Oct 12 2000 Than Ngo <than@redhat.com>
- add default configuration files for iproute (Bug #10549, #18887)

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- fix include-glibc/ to cope with glibc 2.2 new resolver headers

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- use RPM macros
- handle RPM_OPT_FLAGS

* Sat Jun 03 2000 Than Ngo <than@redhat.de>
- fix iproute to build with new glibc

* Fri May 26 2000 Ngo Than <than@redhat.de>
- update to 2.2.4-now-ss000305
- add configuration files

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Mon Aug 16 1999 Cristian Gafton <gafton@redhat.com>
- first build
