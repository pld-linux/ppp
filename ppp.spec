Summary:	ppp daemon package for linux 2.2.11 and greater
Summary(de):	ppp-Dämonpaket für Linux 2.2.11 und höher 
Summary(fr):	Paquetage du démon ppp pour Linux 2.2.11 et supérieur
Summary(tr):	PPP sunucu süreci
Summary(pl):	Demon PPP dla Linux 2.2.11 i wy¿szych
Name:		ppp
Version:	2.4.0
Release:	6
Epoch:		2
License:	Distributable
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.linuxcare.com.au/pub/ppp/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Patch0:		%{name}-make.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-debian_scripts.patch
Patch3:		%{name}-static.patch
Patch4:		%{name}-CBCP.patch
Patch5:		%{name}-speed.patch
Patch6:		%{name}-pam_session.patch
Patch7:		%{name}-wtmp.patch
Patch8:		http://www.math.uwaterloo.ca/~mostrows/ppp-2.4.0-pppoe.patch2
Patch9:		%{name}-opt.patch
# Patch 10 was built out of the following:
#http://www.math.uwaterloo.ca/~mostrows/pppd.patch.240600
#http://www.sfgoth.com/~mitch/linux/atm/pppoatm/pppoatm-pppd-vs-2.4.0b2+240600.diff.gz
#Patch10:		ppp-pppoatm.patch
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the daemon and documentation for PPP support. It requires a
kernel greater than 2.2.11 which is built with PPP support. The
default kernels include PPP support as a module. This version supports
IPv6, too.

%description -l de
Dies ist der Dämon und die Dokumentation für PPP-Support. Erfordert
einen Kernel höher als 2.2.11, der mit PPP-Support gebaut ist. Die
Standard- Red-Hat-Kernel schließen PPP-Support als Modul ein. (IPv6)

%description -l fr
Ceci est le démon et la documentation pour le support PPP. Cela
réclame un noyau supérieur au 2.2.11 et construit avec le support PPP.
Le noyau par défaut de Red Hat contient le support PPP sous forme de
module. (IPv6)

%description -l pl
Pakiet zawiera demona i dokumentacjê umo¿liwiaj±c± korzystanie z
protoko³u PPP. Wymaga jadra 2.2.11 - lub wy¿szych - z wkompilowan±
obs³ug± protoko³u PPP. Standardowe j±dro z dytrybucji zawiera wsparcie
dla PPP skompilowane jako modu³. (IPv6)

%description -l tr
Bu paket PPP desteði için belgeler ve sunucu sürecini içerir. Çekirdek
sürümünun 2.2.11'dan daha yüksek olmasýný gerektirir. Öntanýmlý Red
Hat çekirdeði PPP desteðini bir modül olarak içerir. (IPv6)

%prep
%setup -q 
%patch0 -p1
%patch1 -p1 
%patch2 -p1 
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
%configure
%{__make} OPT_FLAGS="%{?debug:-O0 -g}%{!?debug:$RPM_OPT_FLAGS}" \
	%{!?no_cbcp:CBCP=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,ppp/peers}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/pon
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/poff
install debian/plog $RPM_BUILD_ROOT%{_bindir}

install etc.ppp/chap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/pap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/options $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/options.ttyXX $RPM_BUILD_ROOT%{_sysconfdir}/ppp

rm -f scripts/README

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

strip $RPM_BUILD_ROOT%{_sbindir}/*

gzip -9nf README.linux debian/README.debian debian/win95.ppp \
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
%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/plugins
%attr(755,root,root) %{_libdir}/pppd/plugins/*
%{_mandir}/man8/*

%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/ppp/*-secrets
%attr(644,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/ppp/options*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/ppp

%dir %{_sysconfdir}/ppp/peers
