Summary:	ppp daemon package for linux 2.2.11 and greater
Summary(de):	ppp-D�monpaket f�r Linux 2.2.11 und h�her 
Summary(fr):	Paquetage du d�mon ppp pour Linux 2.2.11 et sup�rieur
Summary(tr):	PPP sunucu s�reci
Summary(pl):	Demon PPP dla Linux 2.2.11 i wy�szych
Name:		ppp
Version:	2.3.11
Release:	4
Copyright:	distributable
Group:		Networking/Daemons
Group(pl):	Sieciowe/Demony
Source0:	ftp://cs.anu.edu.au/pub/software/ppp/%{name}-%{version}.tar.gz
Source1:	ppp.pamd
Source2:	ppp.pon
Source3:	ppp.poff
Patch0:		ppp-make.patch
Patch1:		ppp-expect.patch
Patch2:		ppp-debian_scripts.patch
Patch3:		ppp-static.patch
Patch4:		ppp-ipv6.patch
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the daemon and documentation for PPP support.  It requires a kernel
greater than 2.2.11 which is built with PPP support. The default kernels
include PPP support as a module. This version supports IPv6, too.

%description -l de
Dies ist der D�mon und die Dokumentation f�r PPP-Support. Erfordert
einen Kernel h�her als 2.2.11, der mit PPP-Support gebaut ist. Die Standard-
Red-Hat-Kernel schlie�en PPP-Support als Modul ein. (IPv6)

%description -l fr
Ceci est le d�mon et la documentation pour le support PPP. Cela r�clame
un noyau sup�rieur au 2.2.11 et construit avec le support PPP. Le noyau par
d�faut de Red Hat contient le support PPP sous forme de module. (IPv6)

%description -l pl
Pakiet zawiera demona i dokumentacj� umo�liwiaj�c� korzystanie z protoko�u
PPP. Wymaga jadra 2.2.11 - lub wy�szych - z wkompilowan� obs�ug� protoko�u PPP. 
Standardowe j�dro z dytrybucji zawiera wsparcie dla PPP skompilowane jako 
modu�. (IPv6)

%description -l tr
Bu paket PPP deste�i i�in belgeler ve sunucu s�recini i�erir. �ekirdek
s�r�m�nun 2.2.11'dan daha y�ksek olmas�n� gerektirir. �ntan�ml� Red Hat
�ekirde�i PPP deste�ini bir mod�l olarak i�erir. (IPv6)

%prep
%setup -q 
%patch0 -p1
%patch1 -p1 
%patch2 -p1 
%patch3 -p1
%patch4 -p1

%build
%configure
make OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/etc/{pam.d,ppp}

make install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2}		   	$RPM_BUILD_ROOT%{_bindir}/pon
install %{SOURCE3}		   	$RPM_BUILD_ROOT%{_bindir}/poff
install debian/plog			$RPM_BUILD_ROOT%{_bindir}
install etc.ppp/chap-secrets		$RPM_BUILD_ROOT/etc/ppp
install debian/pap-secrets		$RPM_BUILD_ROOT/etc/ppp
install debian/options			$RPM_BUILD_ROOT/etc/ppp
install debian/options.ttyXX		$RPM_BUILD_ROOT/etc/ppp

rm -f scripts/README

install %{SOURCE1}			$RPM_BUILD_ROOT/etc/pam.d/ppp

strip $RPM_BUILD_ROOT%{_sbindir}/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	README.linux debian/README.debian debian/win95.ppp \
	README.MSCHAP80 FAQ debian/ppp-2.3.0.STATIC.README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README.linux,debian/README.debian}.gz scripts
%doc {debian/win95.ppp,README.MSCHAP80,FAQ,debian/ppp-2.3.0.STATIC.README}.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/chat
%attr(755,root,root) %{_sbindir}/pppstats
%attr(755,root,root) %{_sbindir}/pppd
%{_mandir}/man8/*

%attr(600,root,root) %config %verify(not size mtime md5) /etc/ppp/*-secrets
%attr(644,root,root) %config %verify(not size mtime md5) /etc/ppp/options*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/ppp
