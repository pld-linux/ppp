#
# _with_pppoe - with PPPoE support (which requires kernel 2.4)
# _with_pppoatm - with PPPoATM support (which requires kernel 2.4 and atm-devel)
# _without_cbcp - without CBCP (MS CallBack Configuration Protocol)
Summary:	ppp daemon package for Linu
Summary(de):	ppp-Dämonpaket für Linux
Summary(es):	Servidor ppp para Linux
Summary(fr):	Paquetage du démon ppp pour Linux
Summary(pl):	Demon PPP dla Linuksa
Summary(pt_BR):	Servidor ppp para Linux
Summary(tr):	PPP sunucu süreci
Name:		ppp
Version:	2.4.1
Release:	4
Epoch:		2
License:	distributable
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.linuxcare.com.au/pub/ppp/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Source4:	%{name}-non-english-man-pages.tar.bz2
Patch0:		%{name}-make.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-debian_scripts.patch
Patch3:		%{name}-static.patch
Patch4:		%{name}-CBCP.patch
Patch5:		%{name}-pam_session.patch
Patch6:		%{name}-wtmp.patch
Patch7:		%{name}-opt.patch
Patch8:		http://www.shoshin.uwaterloo.ca/~mostrows/%{name}-2.4.1-%{name}oe.patch2
Patch9:		%{name}-opt-%{name}oe.patch
#http://www.sfgoth.com/~mitch/linux/atm/pppoatm/pppoatm-pppd-vs-2.4.0b2+240600.diff.gz
Patch10:	%{name}-%{name}oatm.patch
Patch11:	%{name}-reap.patch
Patch12:	%{name}-warnings.patch
URL:		http://www.samba.org/ppp/
BuildRequires:	pam-devel
%{?_with_pppoatm:BuildRequires:	atm-devel}
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

%description -l es
Este es el servidor y la documentación para soporte PPP. Requiere un
kernel superior al 2.0. Los kernels padrón de la Conectiva incluyen
soporte PPP como módulo.

%description -l fr
Ceci est le démon et la documentation pour le support PPP. Cela
réclame un noyau supérieur au 2.2.11 et construit avec le support PPP.
Le noyau par défaut de Red Hat contient le support PPP sous forme de
module. (IPv6)

%description -l pl
Pakiet zawiera demona i dokumentacjê umo¿liwiaj±c± korzystanie z
protoko³u PPP. Wymaga j±dra 2.2.11 - lub wy¿szych - z wkompilowan±
obs³ug± protoko³u PPP. Standardowe j±dro z dytrybucji zawiera wsparcie
dla PPP skompilowane jako modu³. (IPv6)

%description -l pt_BR
Este é o servidor e a documentação para suporte PPP. Ele requer um
kernel superior ao 2.0. Os kernels-padrão da Conectiva incluem suporte
PPP como módulo.

%description -l tr
Bu paket PPP desteði için belgeler ve sunucu sürecini içerir. Çekirdek
sürümünun 2.2.11'dan daha yüksek olmasýný gerektirir. Öntanýmlý Red
Hat çekirdeði PPP desteðini bir modül olarak içerir. (IPv6)

%package pppoatm
Summary:	PPP Over ATM plugin
Summary(pl):	Wtyczka PPP-po-ATM
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	%{name} = %{version}

%description pppoatm
PPP Over ATM plugin.

%description pppoatm -l pl
Wtyczka PPP-po-ATM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%{!?_with_pppoe:%patch7 -p1}
%{?_with_pppoe:%patch8 -p1}
%{?_with_pppoe:%patch9 -p1}
%{?_with_pppoatm:%patch10 -p1}
%patch11 -p1
%patch12 -p1

%build
%configure
%{__make} OPT_FLAGS="%{rpmcflags}" \
	CC=%{__cc} \
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

bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

rm -f scripts/README

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

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
%if %{?_with_pppoatm:1}%{!?_with_pppoatm:0}%{?_with_pppoatm:1}%{!?_with_pppoatm:0}
%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/%{version}
%endif
%{?_with_pppoatm:%attr(755,root,root) %{_libdir}/pppd/%{version}/minconn.so}
%{?_with_pppoatm:%attr(755,root,root) %{_libdir}/pppd/%{version}/passprompt.so}
%{?_with_pppoe:%attr(755,root,root) %{_libdir}/pppd/%{version}/pppoe.so}
%{_mandir}/man8/*
%lang(fr) %{_mandir}/fr/man8/*
%lang(ja) %{_mandir}/ja/man8/*
%lang(ko) %{_mandir}/ko/man8/*
%lang(pl) %{_mandir}/pl/man8/*

%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ppp/*-secrets
%attr(644,root,root) %config(missingok) %verify(not md5 size mtime) %{_sysconfdir}/ppp/options*
%attr(640,root,root) %config %verify(not md5 size mtime) /etc/pam.d/ppp

%dir %{_sysconfdir}/ppp/peers

%{?_with_pppoatm:%files pppoatm}
%{?_with_pppoatm:%defattr(644,root,root,755)}
%{?_with_pppoatm:%attr(755,root,root) %{_libdir}/pppd/%{version}/pppoatm.so}
