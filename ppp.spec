#
# Conditional build:
%bcond_without	pppoatm	# without PPPoATM plugin (which requires kernel 2.4 and atm-devel)
#
Summary:	ppp daemon package for Linux
Summary(de):	ppp-D�monpaket f�r Linux
Summary(es):	Servidor ppp para Linux
Summary(fr):	Paquetage du d�mon ppp pour Linux
Summary(pl):	Demon PPP dla Linuksa
Summary(pt_BR):	Servidor ppp para Linux
Summary(ru):	����� ppp
Summary(tr):	PPP sunucu s�reci
Summary(zh_CN):	PPP ���ú͹���������.
Name:		ppp
Version:	2.4.2
Release:	0.1
Epoch:		3
License:	distributable
Group:		Networking/Daemons
Source0:	ftp://ftp.samba.org/pub/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	362bcf218fba8afbb9afbee7471e5dac
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Source4:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source4-md5:	3801b59005bef8f52856300fe3167a64
Source5:	%{name}.logrotate
Patch0:		%{name}-make.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-debian_scripts.patch
Patch3:		%{name}-static.patch
#http://www.sfgoth.com/~mitch/linux/atm/pppoatm/pppoatm-pppd-vs-2.4.0b2+240600.diff.gz
Patch4:		%{name}-pppoatm.patch
Patch5:		%{name}-pidfile-owner.patch
Patch6:		%{name}-rp-pppoe-update.patch
Patch7:		%{name}-rp-pppoe-macaddr.patch
Patch8:		%{name}-radius.patch
Patch9:		%{name}-pcap.patch
URL:		http://www.samba.org/ppp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_pppoatm:BuildRequires:	linux-atm-devel}
BuildRequires:	pam-devel
Requires:	pam >= 0.77.3
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

%description -l es
Este es el servidor y la documentaci�n para soporte PPP. Requiere un
kernel superior al 2.0. Los kernels padr�n de la Conectiva incluyen
soporte PPP como m�dulo.

%description -l fr
Ceci est le d�mon et la documentation pour le support PPP. Cela
r�clame un noyau sup�rieur au 2.2.11 et construit avec le support PPP.
Le noyau par d�faut de Red Hat contient le support PPP sous forme de
module. (IPv6)

%description -l pl
Pakiet zawiera demona i dokumentacj� umo�liwiaj�c� korzystanie z
protoko�u PPP. Wymaga j�dra 2.2.11 - lub p�niejszego - z wkompilowan�
obs�ug� protoko�u PPP. Standardowe j�dro z dystrybucji zawiera
wsparcie dla PPP skompilowane jako modu�. (IPv6)

%description -l pt_BR
Este � o servidor e a documenta��o para suporte PPP. Ele requer um
kernel superior ao 2.0. Os kernels-padr�o da Conectiva incluem suporte
PPP como m�dulo.

%description -l ru
�����, ���������������� ����� � ������������ ��� ��������� PPP.

%description -l tr
Bu paket PPP deste�i i�in belgeler ve sunucu s�recini i�erir. �ekirdek
s�r�m�nun 2.2.11'dan daha y�ksek olmas�n� gerektirir. �ntan�ml� Red
Hat �ekirde�i PPP deste�ini bir mod�l olarak i�erir. (IPv6)

%package plugin-devel
Summary:	Stuff needed to build plugins for pppd
Summary(pl):	Rzeczy potrzebne do budowania wtyczek dla pppd
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description plugin-devel
Development files needed to build plugins for pppd.

%description plugin-devel -l pl
Pliki nag��wkowe potrzebne do budowania wtyczek dla pppd.

%package plugin-pppoatm
Summary:	PPPoATM plugin for pppd
Summary(pl):	Wtyczka PPPoATM dla pppd
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}

%description plugin-pppoatm
PPPoATM plugin for pppd.

%description plugin-pppoatm -l pl
Wtyczka PPPoATM dla pppd.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{?with_pppoatm:%patch4 -p1}
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
cd pppd/plugins/radius/radiusclient
# cannot use system radiusclient 0.3.2 - this version is modified
# (contains some extensions which made it incompatible with original)
# lt must be rebuilt (old libtool didn't use PIC on ppc-linux)
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
cd ../../../..
# note: not autoconf configure
%configure
%{__make} \
	OPT_FLAGS="%{rpmcflags}" \
	CC=%{__cc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/{pam.d,ppp/peers},/var/log} \
	$RPM_BUILD_ROOT/etc/logrotate.d

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

install %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/ppp
> $RPM_BUILD_ROOT/var/log/ppp.log

rm -f scripts/README

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

cd $RPM_BUILD_ROOT%{_libdir}/pppd
ln -s %{version}* plugins

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.linux debian/README.debian scripts
%doc debian/win95.ppp README.MSCHAP8* FAQ debian/ppp-2.3.0.STATIC.README
%doc README.MPPE README.pppoe README.cbcp README.pwfd 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/chat
%attr(755,root,root) %{_sbindir}/ppp*
%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/*.*
%{_libdir}/pppd/plugins
%attr(755,root,root) %{_libdir}/pppd/*.*/minconn.so
%attr(755,root,root) %{_libdir}/pppd/*.*/pass*.so
%attr(755,root,root) %{_libdir}/pppd/*.*/rp-pppoe.so
%attr(755,root,root) %{_libdir}/pppd/*.*/rad*.so

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

%if %{with pppoatm}
%files plugin-pppoatm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pppd/*.*/pppoatm.so
%endif
