Summary: A GNU collection of binary utilities.
Name: binutils
Version: 2.10.0.18
Release: 5
Copyright: GPL
Group: Development/Tools
URL: http://sourceware.cygnus.com/binutils
Source: ftp://ftp.valinux.com/pub/support/hjl/binutils/binutils-%{version}.tar.bz2
Patch1: binutils-sparc-gas.patch
Patch2: binutils-sparc64-bfd.patch
Patch3: binutils-alpha-ld-relax.patch
Patch4: binutils-alpha-visibility.patch
Patch5: binutils-sparc64-ultraIII.patch
Patch6: binutils-alpha-fixes.patch
Buildroot: /var/tmp/binutils-root
ExcludeArch: ia64

%description
Binutils is a collection of binary utilities, including ar (for creating,
modifying and extracting from archives), nm (for listing symbols from
object files), objcopy (for copying and translating object files),
objdump (for displaying information from object files), ranlib (for
generating an index for the contents of an archive), size (for listing
the section sizes of an object or archive file), strings (for listing
printable strings from files), strip (for discarding symbols), c++filt
(a filter for demangling encoded C++ symbols), addr2line (for converting
addresses to file and line), and nlmconv (for converting object code into
an NLM). 

Install binutils if you need to perform any of these types of actions on
binary files.  Most programmers will want to install binutils.

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0

%build
ADDITIONAL_TARGETS=""
%ifos linux
%ifarch sparc
ADDITIONAL_TARGETS="--enable-targets=sparc64-linux"
%endif
%endif

%configure --enable-shared $ADDITIONAL_TARGETS
make tooldir=%{_prefix}usr all info

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}
%makeinstall
make prefix=${RPM_BUILD_ROOT}%{_prefix} infodir=${RPM_BUILD_ROOT}%{_infodir} install-info
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/*
gzip -q9f ${RPM_BUILD_ROOT}%{_infodir}/*.info*

#install -m 644 libiberty/libiberty.a ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}
install -m 644 include/libiberty.h ${RPM_BUILD_ROOT}%{_prefix}/include

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*

# This one comes from egcs
rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/c++filt

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/as.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/bfd.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/gasp.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/ld.info.gz
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/standards.info.gz

%preun
if [ $1 = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/as.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/bfd.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gasp.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/ld.info.gz
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/standards.info.gz
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_prefix}/bin/*
%{_mandir}/man1/*
%{_prefix}/include/*
%{_prefix}/%{_lib}/*
%{_infodir}/*info*

%changelog
* Tue Nov 21 2000 Jakub Jelinek <jakub@redhat.com>
- add one more alpha patch

* Wed Nov 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha visibility as problem
- add support for Ultra-III

* Fri Sep 15 2000 Jakub Jelinek <jakub@redhat.com>
- and one more alpha patch

* Fri Sep 15 2000 Jakub Jelinek <jakub@redhat.com>
- two sparc patches

* Mon Jul 24 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.18

* Mon Jul 10 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.12

* Mon Jun 26 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.9

* Thu Jun 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix ld -r

* Mon Jun  5 2000 Jakub Jelinek <jakub@redhat.com>
- 2.9.5.0.46
- use _mandir/_infodir/_lib

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.41

* Wed Apr 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.34

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.31

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- apply kingdon's patch from #5031

* Wed Jan 19 2000 Jeff Johnson <jbj@redhat.com>
- Permit package to be built with a prefix other than /usr.

* Thu Jan 13 2000 Cristian Gafton <gafton@redhat.com>
- add pacth from hjl to fix the versioning problems in ld

* Tue Jan 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add sparc patches from Jakub Jelinek <jakub@redhat.com>
- Add URL:

* Tue Dec 14 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.22

* Wed Nov 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.19

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.16

* Mon Sep 06 1999 Jakub Jelinek <jj@ultra.linux.cz>
- make shared non-pic libraries work on sparc with glibc 2.1.

* Fri Aug 27 1999 Jim Kingdon
- No source/spec changes, just rebuilding with egcs-1.1.2-18 because
  the older egcs was miscompling gprof.

* Mon Apr 26 1999 Cristian Gafton <gafton@redhat.com>
- back out very *stupid* sparc patch done by HJLu. People, keep out of
  things you don't understand.
- add alpha relax patch from rth

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- version  2.9.1.0.23
- patch to make texinfo documentation compile
- auto rebuild in the new build environment (release 2)

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.21
- merged with UltraPenguin

* Mon Jan 04 1999 Cristian Gafton <gafton@redhat.com>
- added ARM patch from philb
- version 2.9.1.0.19a
- added a patch to allow arm* arch to be identified as an ARM

* Thu Oct 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.14.

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.13.

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.12

* Thu Jul  2 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.7.

* Wed Jun 03 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.6.

* Tue Jun 02 1998 Erik Troan <ewt@redhat.com>
- added patch from rth to get right offsets for sections in relocateable
  objects on sparc32

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- version 2.9.1.0.4 is out; even more, it is public !

* Tue May 05 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.3.

* Mon Apr 20 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.0.3

* Tue Apr 14 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.9.0.2

* Sun Apr 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8.1.0.29 (HJ warned me that this thing is a moving target...
  :-)
- "fixed" the damn make install command so that all tools get installed

* Thu Apr 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded again to 2.8.1.0.28 (at least on alpha now egcs will compile)
- added info packages handling

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.8.1.0.23

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8.1.0.15 (required to compile the newer glibc)
- all patches are obsoleted now

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added 2.8.1.0.1 patch from hj
- added patch for alpha palcode form rth
