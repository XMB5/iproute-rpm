Summary: Advanced IP routing and network device configuration tools.
Name: iproute
Version: 2.6.10
Release: 1
Group: Applications/System
Source: http://developer.osdl.org/dev/iproute2/download/iproute2-%{version}-050209.tar.gz
URL:    http://developer.osdl.org/dev/iproute2/
Source1: ip.8
Source2: tc.8
Source3: tc-cbq.8
Source4: tc-cbq-details.8
Source5: tc-htb.8
Source6: tc-pbfifo.8
Source7: tc-pfifo_fast.8
Source8: tc-prio.8
Source9: tc-red.8
Source10: tc-sfq.8
Source11: tc-tbf.8
Patch0: iproute2-2.4.7-docmake.patch
Patch1: iproute2-2.4.7-rt_config.patch
Patch2: iproute2-2.6.9-kernel.patch
Patch4: iproute2-2.4.7-initvar.patch
Patch7: iproute-debug.patch
License: GNU GPL
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: tetex-latex tetex-dvips psutils linuxdoc-tools db4-devel bison

%description
The iproute package contains networking utilities (ip and rtmon, for
example) which are designed to use the advanced networking
capabilities of the Linux 2.4.x and 2.6.x kernel.

%prep
%setup -q -n iproute2-%{version}
%patch0 -p1 -b .docmake
%patch1 -p1 -b .rt_config
%patch2 -p1 -b .kernel
%patch4 -p1 -b .initvar
%patch7 -p1 -b .debug

%build
make
make -C doc

%install
#rm -rf $RPM_BUILD_ROOT
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin \
 	 $RPM_BUILD_ROOT%{_sbindir} \
         $RPM_BUILD_ROOT%{_mandir}/man8 \
         $RPM_BUILD_ROOT/etc/iproute2 \
	 $RPM_BUILD_ROOT%{_libdir}/tc

install -m 755 ip/ip ip/ifcfg ip/rtmon tc/tc $RPM_BUILD_ROOT/sbin
install -m 755 misc/ss misc/nstat misc/rtacct misc/lnstat misc/arpd $RPM_BUILD_ROOT%{_sbindir}
install -m 755 tc/q_netem.so $RPM_BUILD_ROOT%{_libdir}/tc
install -m 644 netem/normal.dist netem/pareto.dist netem/paretonormal.dist $RPM_BUILD_ROOT%{_libdir}/tc
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT/%{_mandir}/man8

cp -f etc/iproute2/* $RPM_BUILD_ROOT/etc/iproute2
rm -rf $RPM_BUILD_ROOT/%{_libdir}/debug/*

%clean
#rm -rf $RPM_BUILD_ROOT
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /etc/iproute2
%doc README.decnet README.iproute2+tc RELNOTES
%doc doc/*.ps examples
/sbin/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) /etc/iproute2/*
%{_sbindir}/*
%{_libdir}/tc/*

%changelog
* Wed Feb 16 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-1
- update to iproute-2.6.10

* Thu Dec 23 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-6
- added arpd into sbin

* Mon Nov 29 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-5
- debug info removed from makefile and from spec (#140891)

* Tue Nov 16 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-4
- source file updated from snapshot version
- endian patch adding <endian.h> 

* Sat Sep 18 2004 Joshua Blanton <jblanton@cs.ohiou.edu> 2.6.9-3
- added installation of netem module for tc

* Mon Sep 06 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-2
- fixed possible buffer owerflow, path by Steve Grubb <linux_4ever@yahoo.com>

* Wed Sep 01 2004 Radek Vokal <rvokal@redhat.com> 2.6.9-1
- updated to iproute-2.6.9, spec file change, patches cleared

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 26 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-16
- Took tons of manpages from debian, much more complete (#123952).

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-15
- rebuilt

* Thu May 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-13.2
- Built security errata version for FC1.

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.7-14
- Fixed -f option for ss (#118355).
- Small description fix (#110997).
- Added initialization of some vars (#74961). 
- Added patch to initialize "default" rule as well (#60693).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Nov 05 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-12
- Security errata for netlink (CAN-2003-0856).

* Thu Oct 23 2003 Phil Knirsch <pknirsch@redhat.com>
- Updated to latest version. Used by other distros, so seems stable. ;-)
- Quite a few patches needed updating in that turn.
- Added ss (#107363) and several other new nifty tools.

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Phil Knirsch <pknirsch@redhat.com> 2.4.7-7
- Added htb3-tc patch from http://luxik.cdi.cz/~devik/qos/htb/ (#75486).

* Fri Oct 11 2002 Bill Nottingham <notting@redhat.com> 2.4.7-6
- remove flags patch at author's request

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-4
- Don't forcibly strip binaries

* Mon May 27 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-3
- Fixed missing diffserv and atm support in config (#57278).
- Fixed inconsistent numeric base problem for command line (#65473).

* Tue May 14 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-2
- Added patch to fix crosscompiling by Adrian Linkins.

* Fri Mar 15 2002 Phil Knirsch <pknirsch@redhat.com> 2.4.7-1
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
