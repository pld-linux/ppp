# _with_pppoatm - with PPPoATM support (which requires kernel 2.4 and atm-devel)
# TODO:
# - fix ppp over atm
%define snap	20020901
Summary:	ppp daemon package for Linux
Summary(de):	ppp-Dämonpaket für Linux
Summary(es):	Servidor ppp para Linux
Summary(fr):	Paquetage du démon ppp pour Linux
Summary(pl):	Demon PPP dla Linuksa
Summary(pt_BR):	Servidor ppp para Linux
Summary(ru):	äÅÍÏÎ ppp
Summary(tr):	PPP sunucu süreci
Summary(zh_CN):	PPP ÅäÖÃºÍ¹ÜÀíÈí¼þ°ü.
Name:		ppp
Version:	2.4.2
Release:	0.%{snap}.3
Epoch:		2
License:	distributable
Group:		Networking/Daemons
Source0:	cvs://pserver.samba.org/ppp/%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	d8a577cb40eb9a6ea6e5bdf9a7fd7e91
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Source4:	%{name}-non-english-man-pages.tar.bz2
# Source4-md5:	3801b59005bef8f52856300fe3167a64
Source5:	%{name}.logrotate
Patch0:		%{name}-make.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-debian_scripts.patch
Patch3:		%{name}-static.patch
#http://www.sfgoth.com/~mitch/linux/atm/pppoatm/pppoatm-pppd-vs-2.4.0b2+240600.diff.gz
Patch4:		%{name}-pppoatm.patch
Patch5:		%{name}-pidfile-owner.patch
Patch6:		%{name}-typos.patch
Patch7:		%{name}-rp-pppoe-update.patch
Patch8:		%{name}-rp-pppoe-macaddr.patch
URL:		http://www.samba.org/ppp/
BuildRequires:	pam-devel
%{?_with_pppoatm:BuildRequires:	linux-atm-devel}
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
protoko³u PPP. Wymaga j±dra 2.2.11 - lub pó¼niejszego - z wkompilowan±
obs³ug± protoko³u PPP. Standardowe j±dro z dystrybucji zawiera
wsparcie dla PPP skompilowane jako modu³. (IPv6)

%description -l pt_BR
Este é o servidor e a documentação para suporte PPP. Ele requer um
kernel superior ao 2.0. Os kernels-padrão da Conectiva incluem suporte
PPP como módulo.

%description -l ru
äÅÍÏÎ, ËÏÎÆÉÇÕÒÁÃÉÏÎÎÙÅ ÆÁÊÌÙ É ÄÏËÕÍÅÎÔÁÃÉÑ ÄÌÑ ÐÏÄÄÅÒÖËÉ PPP.

%description -l tr
Bu paket PPP desteði için belgeler ve sunucu sürecini içerir. Çekirdek
sürümünun 2.2.11'dan daha yüksek olmasýný gerektirir. Öntanýmlý Red
Hat çekirdeði PPP desteðini bir modül olarak içerir. (IPv6)

%package plugin-devel
Summary:        Stuff needed to build plugins for pppd
Summary(pl):    Rzeczy potrzebne do budowania wtyczek dla pppd
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description plugin-devel
Development files needed to build plugins for pppd.

%description plugin-devel -l pl
Pliki nag³ówkowe potrzebne do budowania wtyczek dla pppd.

%prep
%setup -q -n %{name}-%{version}-%{snap}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{?_with_pppoatm:%patch4 -p1}
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
find pppd/plugins/radius/radiusclient -exec touch "{}" ";"
%configure
%{__make} \
	OPT_FLAGS="%{rpmcflags}" \
	CC=%{__cc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/{pam.d,ppp/peers},/var/log} \
	$RPM_BUILD_ROOT/etc/logrotate.d \
	$RPM_BUILD_ROOT/%{_includedir}/pppd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/pon
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/poff
install debian/plog $RPM_BUILD_ROOT%{_bindir}

install etc.ppp/chap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/pap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/options $RPM_BUILD_ROOT%{_sysconfdir}/ppp
install debian/options.ttyXX $RPM_BUILD_ROOT%{_sysconfdir}/ppp

install pppd/patchlevel.h $RPM_BUILD_ROOT/%{_includedir}/pppd
install pppd/pppd.h $RPM_BUILD_ROOT/%{_includedir}/pppd

bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

install %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/ppp
> $RPM_BUILD_ROOT/var/log/ppp.log

rm -f scripts/README

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.linux debian/README.debian scripts
%doc debian/win95.ppp README.MSCHAP8* FAQ debian/ppp-2.3.0.STATIC.README
%doc README.MPPE README.pppoe README.cbcp README.pwfd TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/chat
%attr(755,root,root) %{_sbindir}/ppp*
%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/*.*
%attr(755,root,root) %{_libdir}/pppd/*.*/minconn.so
%attr(755,root,root) %{_libdir}/pppd/*.*/pass*.so
%attr(755,root,root) %{_libdir}/pppd/*.*/rp-pppoe.so
%attr(755,root,root) %{_libdir}/pppd/*.*/rad*.so
%{?_with_pppoatm:%attr(755,root,root) %{_libdir}/pppd/*.*/pppoatm.so}

%{_mandir}/man8/*
%lang(fr) %{_mandir}/fr/man8/*
%lang(ja) %{_mandir}/ja/man8/*
%lang(ko) %{_mandir}/ko/man8/*
%lang(pl) %{_mandir}/pl/man8/*

%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ppp/*-secrets
%attr(644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ppp/options*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/pam.d/ppp
%attr(640,root,root) /etc/logrotate.d/ppp
%attr(640,root,root) %ghost /var/log/ppp.log

%dir %{_sysconfdir}/ppp/peers

%files plugin-devel
%defattr(644,root,root,755)
%dir %{_includedir}/pppd
%{_includedir}/pppd/pppd.h
%{_includedir}/pppd/patchlevel.h
