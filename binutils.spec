Summary: A GNU collection of binary utilities.
Name: binutils
Version: 2.11.90.0.8
Release: 9
Copyright: GPL
Group: Development/Tools
URL: http://sourceware.cygnus.com/binutils
Source: ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
Patch1: binutils-2.10.1.0.7-oformat.patch
Patch2: binutils-2.11.90.0.4-glibc21.patch
Patch3: binutils-2.11.90.0.8-combreloc.patch
Patch4: binutils-2.11.90.0.8-alpha.patch
Patch5: binutils-2.11.90.0.8-orphan.patch
Patch6: binutils-2.11.90.0.8-orphan2.patch
Patch7: binutils-2.11.90.0.8-ia64funcsize.patch
Patch8: binutils-2.11.90.0.8-combreloc-default.patch
Patch9: binutils-2.11.90.0.8-ia64unwind.patch
Patch10: binutils-2.11.90.0.8-alpharelative.patch
Buildroot: /var/tmp/binutils-root
Prereq: /sbin/install-info
%ifarch ia64
Obsoletes: gnupro
%endif

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), size (for listing the section sizes of an
object or archive file), strings (for listing printable strings from
files), strip (for discarding symbols), and addr2line (for converting
addresses to file and line).

%prep
%setup -q
%patch1 -p0 -b .oformat
%patch2 -p1 -b .glibc21
%patch3 -p0 -b .combreloc
%patch4 -p0 -b .alpha
%patch5 -p0 -b .orphan
%patch6 -p0 -b .orphan2
%patch7 -p0 -b .ia64funcsize
%ifarch i386 alpha ia64 sparc sparc64
%patch8 -p0 -b .combreloc-default
%endif
%patch9 -p0 -b .ia64unwind
%patch10 -p0 -b .alpharelative
mv -f ld/Makefile.in ld/Makefile.in.tmp
sed -e '/^ALL_EMULATIONS/s/eelf_i386_chaos.o/& eelf_i386_glibc21.o/' < ld/Makefile.in.tmp > ld/Makefile.in
rm -f ld/Makefile.in.tmp

%build
# Binutils come with its own custom libtool
%define __libtoolize echo
%configure --enable-shared
make tooldir=%{_prefix} all info

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

# This one comes from gcc
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
* Fri Aug 31 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-9
- on Alpha, copy *r_offset to R_ALPHA_RELATIVE's r_addend

* Thu Aug 30 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-8
- on IA-64, put crtend{,S}.o's .IA_64.unwind section last in
  .IA_64.unwind output section (for compatibility with 7.1 eh)

* Fri Aug 24 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-7
- put RELATIVE relocs first, not last
- enable -z combreloc by default on IA-{32,64}, Alpha, Sparc*

* Thu Aug 23 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-6
- support for -z combreloc
- remove .dynamic patch, -z combreloc patch does this better
- set STT_FUNC default symbol sizes in .endp directive on IA-64

* Mon Jul 16 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-5
- fix last patch (H.J.Lu)

* Fri Jul 13 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-4
- fix placing of orphan sections

* Sat Jun 23 2001 Jakub Jelinek <jakub@redhat.com>
- fix SHF_MERGE support on Alpha

* Fri Jun  8 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.8
  - some SHF_MERGE suport fixes
- don't build with tooldir /usrusr instead of /usr (#40937)
- reserve few .dynamic entries for prelinking

* Mon Apr 16 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.5
  - SHF_MERGE support

* Tue Apr  3 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.4
  - fix uleb128 support, so that CVS gcc bootstraps
  - some ia64 fixes

* Mon Mar 19 2001 Jakub Jelinek <jakub@redhat.com>
- add -Bgroup support from Ulrich Drepper

* Fri Mar  9 2001 Jakub Jelinek <jakub@redhat.com>
- hack - add elf_i386_glibc21 emulation

* Fri Feb 16 2001 Jakub Jelinek <jakub@redhat.com>
- 2.10.91.0.2

* Fri Feb  9 2001 Jakub Jelinek <jakub@redhat.com>
- 2.10.1.0.7
- remove ExcludeArch ia64
- back out the -oformat, -omagic and -output change for now

* Fri Dec 15 2000 Jakub Jelinek <jakub@redhat.com>
- Prereq /sbin/install-info

* Tue Nov 21 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.1.0.2

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
