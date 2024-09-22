# TODO:
# - check mppc patch
# - check if %{_libdir}/pppd/%{version} path is needed, if not drop the symlink

# Conditional build:
%bcond_with	mppc	# MPPC/MPPE-56/LZS support (upstream-incompatible configuration, support not in mainline/PLD kernel)
%bcond_without	system_libatm	# link PPPoATM plugin against system libatm
%bcond_with	srp	# SRP support (pppd/srp-entry.8 missing in dist)
%bcond_without	systemd	# systemd notifications
#
Summary:	ppp daemon package for Linux
Summary(de.UTF-8):	ppp-Dämonpaket für Linux
Summary(es.UTF-8):	Servidor ppp para Linux
Summary(fr.UTF-8):	Paquetage du démon ppp pour Linux
Summary(pl.UTF-8):	Demon PPP dla Linuksa
Summary(pt_BR.UTF-8):	Servidor ppp para Linux
Summary(ru.UTF-8):	Демон ppp
Summary(tr.UTF-8):	PPP sunucu süreci
Summary(zh_CN.UTF-8):	PPP 配置和管理软件包
Name:		ppp
Version:	2.5.1
Release:	1
Epoch:		3
License:	distributable
Group:		Networking/Daemons
Source0:	https://download.samba.org/pub/ppp/%{name}-%{version}.tar.gz
# Source0-md5:	c2d96ac7eb2020d3ed0e6e05fe996afe
Source1:	%{name}.pamd
Source2:	%{name}.pon
Source3:	%{name}.poff
Source4:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source4-md5:	3801b59005bef8f52856300fe3167a64
Source5:	%{name}.logrotate
Patch2:		%{name}-debian_scripts.patch
Patch4:		%{name}-pidfile-owner.patch
# http://public.planetmirror.com/pub/mppe/pppd-2.4.2-chapms-strip-domain.patch.gz
Patch7:		pppd-2.4.2-chapms-strip-domain.patch
# http://mppe-mppc.alphacron.de/%{name}-2.4.3-mppe-mppc-1.1.patch.gz
Patch10:	%{name}-2.4.3-mppe-mppc-1.1.patch
URL:		https://ppp.samba.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	libpcap-devel >= 2:0.8.1
BuildRequires:	libtool >= 2:2
%{?with_system_libatm:BuildRequires:	linux-atm-devel}
# <linux/if_pppol2tp.h>
BuildRequires:	linux-libc-headers >= 7:2.6.23
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
%{?with_srp:BuildRequires:	srp-devel}
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
Requires:	pam >= 0.77.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the daemon and documentation for PPP support. It requires a
kernel greater than 2.2.11 which is built with PPP support. The
default kernels include PPP support as a module. This version supports
IPv6, too.

%description -l de.UTF-8
Dies ist der Dämon und die Dokumentation für PPP-Support. Erfordert
einen Kernel höher als 2.2.11, der mit PPP-Support gebaut ist. Die
Standard-Kernel schließen PPP-Support als Modul ein. (IPv6)

%description -l es.UTF-8
Este es el servidor y la documentación para soporte PPP. Requiere un
kernel superior al 2.0.

%description -l fr.UTF-8
Ceci est le démon et la documentation pour le support PPP. Cela
réclame un noyau supérieur au 2.2.11 et construit avec le support PPP.

%description -l pl.UTF-8
Pakiet zawiera demona i dokumentację umożliwiającą korzystanie z
protokołu PPP. Wymaga jądra 2.2.11 - lub późniejszego - z wkompilowaną
obsługą protokołu PPP. Standardowe jądro z dystrybucji zawiera
wsparcie dla PPP skompilowane jako moduł. (IPv6)

%description -l pt_BR.UTF-8
Este é o servidor e a documentação para suporte PPP. Ele requer um
kernel superior ao 2.0.

%description -l ru.UTF-8
Демон, конфигурационные файлы и документация для поддержки PPP.

%description -l tr.UTF-8
Bu paket PPP desteği için belgeler ve sunucu sürecini içerir. Çekirdek
sürümünun 2.2.11'dan daha yüksek olmasını gerektirir.

%package plugin-devel
Summary:	Stuff needed to build plugins for pppd
Summary(pl.UTF-8):	Rzeczy potrzebne do budowania wtyczek dla pppd
Group:		Development/Libraries
# doesn't require base but enforce new version
Conflicts:	%{name} < %{epoch}:%{version}-%{release}

%description plugin-devel
Development files needed to build plugins for pppd.

%description plugin-devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do budowania wtyczek dla pppd.

%package plugin-pppoatm
Summary:	PPPoATM plugin for pppd
Summary(pl.UTF-8):	Wtyczka PPPoATM dla pppd
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description plugin-pppoatm
PPPoATM plugin for pppd.

%description plugin-pppoatm -l pl.UTF-8
Wtyczka PPPoATM dla pppd.

%prep
%setup -q
%patch2 -p1
%patch4 -p1
%patch7 -p1
%if %{with mppc}
%patch10 -p1
%endif

# use headers from llh instead of older supplied by ppp, incompatible with current llh
%{__rm} include/linux/*.h

%{__sed} -i -e 's,/usr/lib64/openssl/engines/,/%{_lib}/engines-3/,' \
	-e 's,/usr/lib64/,%{_libdir}/,' etc.ppp/openssl.cnf.example

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-cbcp \
	--enable-mslanman \
	--enable-multilink \
	--disable-silent-rules \
	%{?with_systemd:--enable-systemd} \
	--with-plugin-dir=%{_libdir}/pppd/plugins \
	%{!?with_srp:--without-srp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/ppp/peers,/var/log} \
	$RPM_BUILD_ROOT/etc/{pam.d,logrotate.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/pppd/plugins/*.la

install -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/pon
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/poff
install -p debian/plog $RPM_BUILD_ROOT%{_bindir}

for f in $RPM_BUILD_ROOT%{_sysconfdir}/ppp/*.example ; do
	%{__mv} "$f" "${f%.example}"
done
cp -p debian/pap-secrets $RPM_BUILD_ROOT%{_sysconfdir}/ppp
cp -p debian/options $RPM_BUILD_ROOT%{_sysconfdir}/ppp
cp -p debian/options.ttyXX $RPM_BUILD_ROOT%{_sysconfdir}/ppp

bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/README.ppp-non-english-man-pages

cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/logrotate.d/ppp
> $RPM_BUILD_ROOT/var/log/ppp.log

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ppp

[ ! -d example-scripts ] || %{__rm} -r example-scripts  # make install reentrant
cp -pr scripts example-scripts
%{__rm} example-scripts/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# %{version} used to be directory
if [ -d %{_libdir}/pppd/%{version} -a ! -L %{_libdir}/pppd/%{version} ]; then
	set -e
	rm -f %{_libdir}/pppd/plugins
	mv -f %{_libdir}/pppd/{%{version},plugins}
	ln -snf plugins %{_libdir}/pppd/%{version}
fi

%files
%defattr(644,root,root,755)
%doc Changes-2.3 FAQ NEWS README README.{MPPE,MSCHAP80,MSCHAP81,cbcp,eap-tls,linux,pppoe,pppol2tp,pwfd} %{?with_srp:README.eap-srp} SETUP debian/{README.debian,win95.ppp} example-scripts
%attr(755,root,root) %{_bindir}/plog
%attr(755,root,root) %{_bindir}/poff
%attr(755,root,root) %{_bindir}/pon
%attr(755,root,root) %{_sbindir}/chat
%attr(755,root,root) %{_sbindir}/pppd
%attr(755,root,root) %{_sbindir}/pppdump
%attr(755,root,root) %{_sbindir}/pppoe-discovery
%attr(755,root,root) %{_sbindir}/pppstats
%{?with_srp:%attr(755,root,root) %{_sbindir}/srp-entry}
%dir %{_libdir}/pppd
%dir %{_libdir}/pppd/plugins
%attr(755,root,root) %{_libdir}/pppd/plugins/minconn.so
%attr(755,root,root) %{_libdir}/pppd/plugins/openl2tp.so
%attr(755,root,root) %{_libdir}/pppd/plugins/passprompt.so
%attr(755,root,root) %{_libdir}/pppd/plugins/passwordfd.so
%attr(755,root,root) %{_libdir}/pppd/plugins/pppoe.so
%attr(755,root,root) %{_libdir}/pppd/plugins/pppol2tp.so
%attr(755,root,root) %{_libdir}/pppd/plugins/radattr.so
%attr(755,root,root) %{_libdir}/pppd/plugins/radius.so
%attr(755,root,root) %{_libdir}/pppd/plugins/radrealms.so
%attr(755,root,root) %{_libdir}/pppd/plugins/winbind.so

%{_mandir}/man8/chat.8*
%{_mandir}/man8/pppd.8*
%{_mandir}/man8/pppd-radattr.8*
%{_mandir}/man8/pppd-radius.8*
%{_mandir}/man8/pppdump.8*
%{_mandir}/man8/pppoe-discovery.8*
%{_mandir}/man8/pppstats.8*
%lang(fr) %{_mandir}/fr/man8/*
%lang(ja) %{_mandir}/ja/man8/*
%lang(ko) %{_mandir}/ko/man8/*
%lang(pl) %{_mandir}/pl/man8/*

%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/chap-secrets
%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/pap-secrets
%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/eaptls-client
%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/eaptls-server
%attr(600,root,root) %config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/openssl.cnf
%config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/options
%config(missingok,noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ppp/options.ttyXX
%dir %{_sysconfdir}/ppp/peers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/ppp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ppp
%attr(640,root,root) %ghost /var/log/ppp.log

%files plugin-devel
%defattr(644,root,root,755)
%doc PLUGINS
%{_includedir}/pppd
%{_pkgconfigdir}/pppd.pc

%files plugin-pppoatm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pppd/plugins/pppoatm.so
