Summary:	ppp daemon package for linux 1.3.xx and greater
Summary(de):	ppp-Dämonpaket für Linux 1.3.xx und höher 
Summary(fr):	Paquetage du démon ppp pour Linux 1.3.xx et supérieur
Summary(tr):	PPP sunucu süreci
Summary(pl):	Demon PPP dla Linux 1.3.x i wy¿szych
Name:		ppp
Version:	2.3.7
Release:	1 
Copyright:	distributable
Group:		Networking/Daemons
Group(pl):	Sieciowe/Demony
Source0:	ftp://cs.anu.edu.au/pub/software/ppp/%{name}-%{version}.tar.gz
Source1:	pppd-2.3.7-pamd.conf
Patch0:		ppp-make.patch
Patch1:		ppp-auth.patch
Patch2:		ppp-expect.patch
Patch3:		ppp-debian_scripts.patch
Patch4:		ppp-static.patch
Patch5:		ppp-log.patch
Buildroot:	/tmp/%{name}-%{version}-root

%description
This is the daemon and documentation for PPP support.  It requires a kernel
greater than 2.0 which is built with PPP support. The default kernels include 
PPP support as a module.

%description -l de
Dies ist der Dämon und die Dokumentation für PPP-Support. Erfordert
einen Kernel höher als 2.0, der mit PPP-Support gebaut ist. Die Standard-
Red-Hat-Kernel schließen PPP-Support als Modul ein.

%description -l fr
Ceci est le démon et la documentation pour le support PPP. Cela réclame
un noyau supérieur au 2.0 et construit avec le support PPP. Le noyau par
défaut de Red Hat contient le support PPP sous forme de module.

%description -l tr
Bu paket PPP desteði için belgeler ve sunucu sürecini içerir. Çekirdek
sürümünun 2.0'dan daha yüksek olmasýný gerektirir. Öntanýmlý Red Hat
çekirdeði PPP desteðini bir modül olarak içerir.

%description -l pl
Pakiet zawiera demona i dokumentacjê umo¿liwiaj±c± korzystanie z protoko³u
PPP. Wymaga jadra 2.0 - lub wy¿szych - z wkompilowan± obs³ug± protoko³u PPP. 
Standardowe j±dro z dytrybucji zawiera wsparcie dla PPP skompilowane jako 
modu³.

%prep
%setup -q 
%patch0 -p1 
%patch1 -p1 -b .auth
%patch2 -p1 
%patch3 -p1 
%patch4 -p1
%patch5 -p1

%build
./configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{sbin,bin,man/man{1,8}} \
	$RPM_BUILD_ROOT/etc/{ppp/{chatscripts,peers},pam.d}

make install TOPDIR=$RPM_BUILD_ROOT

install etc.ppp/chap-secrets 	   $RPM_BUILD_ROOT/etc/ppp
install debian/{plog,poff,pon}	   $RPM_BUILD_ROOT/usr/bin
install debian/*.1		   $RPM_BUILD_ROOT/usr/man/man1
install debian/pap-secrets	   $RPM_BUILD_ROOT/etc/ppp
install debian/options		   $RPM_BUILD_ROOT/etc/ppp
install debian/options.ttyXX	   $RPM_BUILD_ROOT/etc/ppp
install debian/provider		   $RPM_BUILD_ROOT/etc/ppp/peers
install debian/provider.chatscript $RPM_BUILD_ROOT/etc/ppp/chatscripts/provider

rm -f scripts/README

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

strip $RPM_BUILD_ROOT/usr/sbin/*

gzip -9nf $RPM_BUILD_ROOT/usr/man/man[18]/* \
	README.linux debian/README.debian debian/win95.ppp \
	README.MSCHAP80 FAQ debian/ppp-2.3.0.STATIC.README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README.linux,debian/README.debian}.gz scripts
%doc {debian/win95.ppp,README.MSCHAP80,FAQ,debian/ppp-2.3.0.STATIC.README}.gz

%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/chat
%attr(755,root,root) /usr/sbin/pppstats
%attr(0755,root,root) /usr/sbin/pppd
/usr/man/man[18]/*

%attr(711,root,root) %dir /etc/ppp/peers
%attr(711,root,root) %dir /etc/ppp/chatscripts

%attr(600,root,root) %config %verify(not size mtime md5) /etc/ppp/*-secrets
%attr(644,root,root) %config %verify(not size mtime md5) /etc/ppp/options*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/ppp
%attr(640,root,root) %config %verify(not size mtime md5) /etc/ppp/peers/provider
%attr(640,root,root) %config %verify(not size mtime md5) /etc/ppp/chatscripts/provider

%changelog
* Wed Apr 28 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [2.3.7-1]
- updated to 2.3.7,
- removed ppp-2.3.5-glibc.diff,
- added ppp-auth.patch,
- split ppp-2.3.5.debian.patch into separate patches,
- updated all patches for new version,
- simplifications in %install,
- changes in %files,
- fixed passing RPM_OPT_FLAGS during compilation,
- added stripping binaries,
- major changes,
- recompiled on rpm 3.

* Tue Feb 02 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [2.3.5-3d]
- added debian patch
- corrected permissions

* Mon Aug 31 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.3.5-1d]
- build against glibc-2.1,
- changed permissions of all binaries to 711,
- build from non root's account,
- build with PAM support,
- added md5 support.

* Wed Aug 26 1998 Krzysztof G. Baranowski <kgb@knm.org.pl>
  [2.3.5-1]
- build against glibc-2.0.7,
- translations modified for pl,
- added small patch to solve problems with glibc.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Mar 18 1998 Cristian Gafton <gafton@redhat.com>
- requires glibc 2.0.6 or later

* Wed Mar 18 1998 Michael K. Johnson <johnsonm@redhat.com>
- updated PAM patch to not turn off wtmp/utmp/syslog logging.

* Wed Jan  7 1998 Cristian Gafton <gafton@redhat.com>
- added the /etc/pam.d config file
- updated PAM patch to include session support

* Tue Jan  6 1998 Cristian Gafton <gafton@redhat.com>
- updated to ppp-2.3.3, build against glibc-2.0.6 - previous patches not
  required any more.
- added buildroot
- fixed the PAM support, which was really, completely broken and against any
  standards (session support is still not here... :-( )
- we build against running kernel and pray that it will work
- added a samples patch; updated glibc patch

* Thu Dec 18 1997 Erik Troan <ewt@redhat.com>
- added a patch to use our own route.h, rather then glibc's (which has
  alignment problems on Alpha's) -- I only applied this patch on the Alpha,
  though it should be safe everywhere

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- turned off the execute bit for scripts in /usr/doc

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Integrated new patch from David Mosberger
- Improved description%files
