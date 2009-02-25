##%define date_version 070710
%define cbq_version v0.7.3

Summary: Advanced IP routing and network device configuration tools
Name: iproute
Version: 2.6.28
Release: 3%{?dist}
Group: Applications/System
Source: http://developer.osdl.org/dev/iproute2/download/iproute2-%{version}.tar.bz2
#Source1: iproute-doc-2.6.22.tar.gz
URL:	http://linux-net.osdl.org/index.php/Iproute2
Patch1: iproute2-2.6.9-kernel.patch
Patch2: iproute2-ss050901-opt_flags.patch
Patch3: iproute-ip-man.patch
Patch4: iproute2-2.6.25-segfault.patch
Patch5: iproute2-sharepath.patch
Patch6: iproute2-ddr_support.patch

License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: tetex-latex tetex-dvips linuxdoc-tools
BuildRequires: flex linux-atm-libs-devel psutils db4-devel bison

%description
The iproute package contains networking utilities (ip and rtmon, for
example) which are designed to use the advanced networking
capabilities of the Linux 2.4.x and 2.6.x kernel.

%prep
%setup -q -c iproute-%{version}
%patch1 -p1 -b .kernel
%patch2 -p1 -b .opt_flags
%patch3 -p1
%patch4 -p1 -b .seg
%patch5 -p1 -b .share
%patch6 -p1 -b .ddr

%build
export LIBDIR=%{_libdir}

cd iproute2-%{version}
make %{?_smp_mflags}
make -C doc

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_mandir}/man8 \
	$RPM_BUILD_ROOT/%{_sysconfdir}/iproute2 \
	$RPM_BUILD_ROOT%{_datadir}/tc \
	$RPM_BUILD_ROOT%{_libdir}/tc

cd iproute2-%{version}
install -m 755 ip/ip ip/ifcfg ip/rtmon tc/tc $RPM_BUILD_ROOT/sbin
install -m 755 misc/ss misc/nstat misc/rtacct misc/lnstat misc/arpd $RPM_BUILD_ROOT%{_sbindir}
#netem is static
#install -m 755 tc/q_netem.so $RPM_BUILD_ROOT%{_libdir}/tc
install -m 755 tc/q_atm.so $RPM_BUILD_ROOT%{_libdir}/tc
install -m 644 netem/normal.dist netem/pareto.dist netem/paretonormal.dist $RPM_BUILD_ROOT%{_datadir}/tc
install -m 644 man/man8/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8
rm -r $RPM_BUILD_ROOT/%{_mandir}/man8/ss.8
iconv -f latin1 -t utf8 < man/man8/ss.8 > $RPM_BUILD_ROOT/%{_mandir}/man8/ss.8
install -m 755 examples/cbq.init-%{cbq_version} $RPM_BUILD_ROOT/sbin/cbq
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/cbq

cp -f etc/iproute2/* $RPM_BUILD_ROOT/%{_sysconfdir}/iproute2
rm -rf $RPM_BUILD_ROOT/%{_libdir}/debug/*

#copy the tex file from source for time when tex was broken
#source1 was created from last functional version
#tar -xvzf %{SOURCE1}
#mkdir -p $RPM_BUILD_ROOT/%{_defaultdocdir}/%{name}-%{version}
#cd %{name}-doc-2.6.22
#cp -pR *.ps ../doc

#create example avpkt file
cat <<EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/cbq/cbq-0000.example
DEVICE=eth0,10Mbit,1Mbit
RATE=128Kbit
WEIGHT=10Kbit
PRIO=5
RULE=192.168.1.0/24
EOF

cat <<EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/cbq/avpkt
AVPKT=3000
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/iproute2
%doc iproute2-%{version}/README.decnet iproute2-%{version}/README.iproute2+tc iproute2-%{version}/RELNOTES iproute2-%{version}/examples/README.cbq
%doc iproute2-%{version}/doc/*.ps 
%doc iproute2-%{version}/examples
/sbin/*
%{_mandir}/man8/*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%dir %{_datadir}/tc
%{_datadir}/tc/*
%dir %{_libdir}/tc/
%{_libdir}/tc/*
%dir %{_sysconfdir}/sysconfig/cbq
%config(noreplace) %{_sysconfdir}/sysconfig/cbq/*

%changelog
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-2
- 483484 install distribution files into /usr/share and also fixed
 install paths in spec
- add the latest change from git which add DRR support
 c86f34942a0ce9f8203c0c38f9fe9604f96be706

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.28-1
- previous two patches were included into 2.6.28 release.
- update

* Mon Jan 12 2009 Marcela Mašláňová <mmaslano@redhat.com> - 2.6.27-2
- 475130 - Negative preferred lifetimes of IPv6 prefixes/addresses
  displayed incorrectly
- 472878 - “ip maddr show” in IB interface causes a stack corruption
- both patches will be probably in iproute v2.6.28

* Thu Dec 4 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.27-1
- aead support was included into upstream version
- patch for moving libs is now deprecated
- update to 2.6.27

* Tue Aug 12 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.26-1
- update to 2.6.26
- clean patches

* Tue Jul 22 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-5
- fix iproute2-2.6.25-segfault.patch

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6.25-4
- rebuild for new db4-4.7

* Thu Jul  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-3
- 449933 instead of failing strncpy use copying byte after byte

* Wed May 14 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-2
- allow replay setting, solve also 444724

* Mon Apr 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.25-1
- update
- remove patch for backward compatibility
- add patch for AEAD compatibility

* Thu Feb 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-4
- add creating ps file again. Fix was done in texlive

* Wed Feb  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-3
- rebuild without tetex files. It isn't working in rawhide yet. Added
	new source for ps files. 
- #431179 backward compatibility for previous iproute versions

* Mon Jan 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-2
- rebuild with fix tetex and linuxdoc-tools -> manual pdf
- clean unnecessary patches
- add into spec *.so objects, new BR linux-atm-libs-devel

* Tue Oct 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.23-1
- new version from upstrem 2.3.23

* Tue Oct 23 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-5
- move files from /usr/lib/tc to /usr/share/tc
- remove listing files twice

* Fri Aug 30 2007 Marcela Maslanova <mmaslano@redhat.com> - 2.6.22-3
- package review #225903

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 2.6.22-2
- rebuild for new db4

* Wed Jul 11 2007 Radek Vokál <rvokal@redhat.com> - 2.6.22-1
- upgrade to 2.6.22

* Mon Mar 19 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-2
- fix broken tc-pfifo man page (#232891)

* Thu Mar 15 2007 Radek Vokál <rvokal@redhat.com> - 2.6.20-1
- upgrade to 2.6.20

* Fri Dec 15 2006 Radek Vokál <rvokal@redhat.com> - 2.6.19-1
- upgrade to 2.6.19

* Mon Dec 11 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-5
- fix snapshot version

* Fri Dec  1 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-4
- spec file cleanup
- one more rebuilt against db4

* Thu Nov 16 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-3
- fix defective manpage for tc-pfifo (#215399)

* Mon Nov 13 2006 Radek Vokál <rvokal@redhat.com> - 2.6.18-2
- rebuilt against new db4

* Tue Oct  3 2006 Radek Vokal <rvokal@redhat.com> - 2.6.18-1
- upgrade to upstream 2.6.18
- initcwnd patch merged
- bug fix for xfrm monitor
- alignment fixes for cris
- documentation corrections
        
* Mon Oct  2 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-7
- fix ip.8 man page, add initcwnd option

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Radek Vokal <rvokal@redhat.com> - 2.6.16-5
- fix crash when resolving ip address

* Mon Aug 21 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-4
- add LOWER_UP and DORMANT flags (#202199)
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.16-3.1
- rebuild

* Mon Jun 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-3
- improve handling of initcwnd value (#179719)

* Sun May 28 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-2
- fix BuildRequires: flex (#193403)

* Sun Mar 26 2006 Radek Vokál <rvokal@redhat.com> - 2.6.16-1
- upgrade to 2.6.16-060323
- don't hardcode /usr/lib in tc (#186607)

* Wed Feb 22 2006 Radek Vokál <rvokal@redhat.com> - 2.6.15-2
- own /usr/lib/tc (#181953)
- obsoletes shapecfg (#182284)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6.15-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Radek Vokal <rvokal@redhat.com> 2.6.15-1
- upgrade to 2.6.15-060110

* Mon Dec 12 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-11
- rebuilt

* Fri Dec 09 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-10
- remove backup of config files (#175302)

* Fri Nov 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-9
- use tc manpages and cbq.init from source tarball (#172851)

* Thu Nov 10 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-8
- new upstream source 

* Mon Oct 31 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-7
- add warning to ip tunnel add command (#128107)

* Fri Oct 07 2005 Bill Nottingham <notting@redhat.com> 2.6.14-6
- update from upstream (appears to fix #170111)

* Fri Oct 07 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-5
- update from upstream
- fixed host_len size for memcpy (#168903) <Matt_Domsch@dell.com>

* Fri Sep 23 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-4
- add RPM_OPT_FLAGS

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-3
- forget to apply the patch :( 

* Mon Sep 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-2
- make ip help work again (#168449)

* Wed Sep 14 2005 Radek Vokal <rvokal@redhat.com> 2.6.14-1
- upgrade to ss050901 for 2.6.14 kernel headers

* Fri Aug 26 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-3
- added /sbin/cbq script and sample configuration files (#166301)

* Fri Aug 19 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-2
- upgrade to iproute2-050816

* Thu Aug 11 2005 Radek Vokal <rvokal@redhat.com> 2.6.13-1
- update to snapshot for 2.6.13+ kernel

* Tue May 24 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-2
- removed useless initvar patch (#150798)
- new upstream source 

* Tue Mar 15 2005 Radek Vokal <rvokal@redhat.com> 2.6.11-1
- update to iproute-2.6.11

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 2.6.10-2
- gcc4 rebuilt

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
