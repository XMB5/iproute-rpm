Summary: Advanced IP routing and network device configuration tools.
Name: iproute
Version: 2.4.7
Release: 1
Group: Applications/System
Source: ftp://ftp.inr.ac.ru/ip-routing/iproute2-2.4.7-now-ss010824.tar.gz
Source1: ip.8
Patch0: iproute2-2.2.4-docmake.patch
Patch1: iproute2-misc.patch
Patch2: iproute2-config.patch
Patch4:	iproute2-in_port_t.patch
Patch5: iproute2-makefile.patch
Patch6: iproute2-flags.patch
License: GNU GPL
BuildRoot: %{_tmppath}/%{name}-root
BuildPrereq: tetex-latex tetex-dvips psutils

%description
The iproute package contains networking utilities (ip and rtmon, for
example) which are designed to use the advanced networking
capabilities of the Linux 2.2.x kernel.

%prep
%setup -q -n iproute2
%patch0 -p1 -b .doc
%patch1 -p1 -b .misc
%patch2 -p1
%patch4 -p1 -b .glibc22
%patch5 -p1 -b .kernel
%patch6 -p1 -b .flags

%build
%define optflags -ggdb

make
make -C doc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin \
 	 $RPM_BUILD_ROOT%{_sbindir} \
         $RPM_BUILD_ROOT%{_mandir}/man8 \
         $RPM_BUILD_ROOT/etc/iproute2

install -s -m 755 ip/ip ip/ifcfg ip/rtmon tc/tc $RPM_BUILD_ROOT/sbin
install -s -m 755 ip/rtacct $RPM_BUILD_ROOT%{_sbindir}
install -s -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_mandir}/man8

cp -f etc/iproute2/* $RPM_BUILD_ROOT/etc/iproute2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /etc/iproute2
%doc README.decnet README.iproute2+tc RELNOTES
%doc doc/*.ps examples
/sbin/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
%{_sbindir}/*

%changelog
* Fri Mar 15 2002 Phil Knirsch <pknirsch@redhat.com>
- Update to latest stable release 2.4.7-now-ss010824.
- Added simple man page for ip.

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- allow setting of allmulti & promisc flags (#48669)

* Mon Jul 02 2001 Than Ngo <than@redhat.com>
- fix build problem in beehive if kernel-sources is not installed

* Fri May 25 2001 Helge Deller <hdeller@redhat.de>
- updated to iproute2-2.2.4-now-ss001007.tar.gz 
- bzip2 source tar file
- "License" replaces "Copyright"
- added "BuildPrereq: tetex-latex tetex-dvips psutils"
- rebuilt for 7.2

* Tue May  1 2001 Bill Nottingham <notting@redhat.com>
- use the system headers - the included ones are broken
- ETH_P_ECHO went away

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
