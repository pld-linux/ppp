#
# _without_pppoe - without PPPoE support (which requires kernel 2.4)
# _without_pppoatm - without PPPoATM support (which requires kernel 2.4)
# _without_cbcp - without CBCP (MS CallBack Configuration Protocol)
Summary:	ppp daemon package for Linux 2.2.11 and greater
Summary(de):	ppp-D�monpaket f�r Linux 2.2.11 und h�her 
Summary(fr):	Paquetage du d�mon ppp pour Linux 2.2.11 et sup�rieur
Summary(pl):	Demon PPP dla Linuksa 2.2.11 i wy�szych
Summary(tr):	PPP sunucu s�reci
Name:		ppp
Version:	2.4.1
Release:	2
Epoch:		2
License:	Distributable
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
URL:		http://www.samba.org/ppp/
Source0:	ftp://ftp.linuxcare.com.au/pub/ppp/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Patch0:		%{name}-make.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-debian_scripts.patch
Patch3:		%{name}-static.patch
Patch4:		%{name}-CBCP.patch
Patch5:		%{name}-pam_session.patch
Patch6:		%{name}-wtmp.patch
Patch7:		%{name}-opt.patch
Patch8:		http://www.shoshin.uwaterloo.ca/~mostrows/%{name}-2.4.1-pppoe.patch2
Patch9:		%{name}-opt-%{name}oe.patch
#http://www.sfgoth.com/~mitch/linux/atm/pppoatm/pppoatm-pppd-vs-2.4.0b2+240600.diff.gz
Patch10:	%{name}-pppoatm.patch
BuildRequires:	pam-devel
%{?!_without_pppoatm:BuildRequires:	atm-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the daemon and documentation for PPP support. It requires a
kernel greater than 2.2.11 which is built with PPP support. The
default kernels include PPP support as a module. This version supports
IPv6, too.

%description -l de
Dies ist der D�mon und die Dokumentation f�r PPP-Support. Erfordert
einen Kernel h�her als 2.2.11, der mit PPP-Support gebaut ist. Die
Standard- Red-Hat-Kernel schlie�en PPP-Support als Modul ein. (IPv6)

%description -l fr
Ceci est le d�mon et la documentation pour le support PPP. Cela
r�clame un noyau sup�rieur au 2.2.11 et construit avec le support PPP.
Le noyau par d�faut de Red Hat contient le support PPP sous forme de
module. (IPv6)

%description -l pl
Pakiet zawiera demona i dokumentacj� umo�liwiaj�c� korzystanie z
protoko�u PPP. Wymaga jadra 2.2.11 - lub wy�szych - z wkompilowan�
obs�ug� protoko�u PPP. Standardowe j�dro z dytrybucji zawiera wsparcie
dla PPP skompilowane jako modu�. (IPv6)

%description -l tr
Bu paket PPP deste�i i�in belgeler ve sunucu s�recini i�erir. �ekirdek
s�r�m�nun 2.2.11'dan daha y�ksek olmas�n� gerektirir. �ntan�ml� Red
Hat �ekirde�i PPP deste�ini bir mod�l olarak i�erir. (IPv6)

%package pppoatm
Summary:	PPP Over ATM plugin
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description pppoatm
PPP Over ATM plugin.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1 
%patch2 -p1 
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%{?_without_pppoe:%patch7 -p1}
%{!?_without_pppoe:%patch8 -p1}
%{!?_without_pppoe:%patch9 -p1}
%{!?_without_pppoatm:%patch10 -p1}

%build
%configure
%{__make} OPT_FLAGS="%{rpmcflags}" \
	%{!?_without_cbcp:CBCP=1}

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
%dir %{_libdir}/pppd/%{version}
%attr(755,root,root) %{_libdir}/pppd/%{version}/minconn.so
%attr(755,root,root) %{_libdir}/pppd/%{version}/passprompt.so
%{!?_without_pppoe:%attr(755,root,root) %{_libdir}/pppd/%{version}/pppoe.so}
%{_mandir}/man8/*

%attr(600,root,root) %config(missingok) %verify(not md5 size mtime) %{_sysconfdir}/ppp/*-secrets
%attr(644,root,root) %config(missingok) %verify(not md5 size mtime) %{_sysconfdir}/ppp/options*
%attr(640,root,root) %config %verify(not md5 size mtime) /etc/pam.d/ppp

%dir %{_sysconfdir}/ppp/peers

%{!?_without_pppoatm:%files pppoatm}
%{!?_without_pppoatm:%defattr(644,root,root,755)}
%{!?_without_pppoatm:%attr(755,root,root) %{_libdir}/pppd/%{version}/pppoatm.so}
