Summary:	Web-based Distributed Authoring and Versioning - caching version
Summary(pl.UTF-8):	Bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie - wersja z cache
Name:		davfs2
Version:	1.4.1
Release:	0.1
License:	GPL
Group:		Networking/Utilities
Source0:	http://download.savannah.gnu.org/releases-noredirect/%{name}/%{name}-%{version}.tar.gz
URL:		http://savannah.nongnu.org/projects/davfs2
BuildRequires:	autoconf
BuildRequires:	neon-devel >= 0.24
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	neon >= 0.24
Provides:	group(davfs2)
Provides:	user(davfs2)
Conflicts:	davfs

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually HTTP is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

This package contains the caching version of davfs.

%description -l pl.UTF-8
WebDAV to bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protokół HTTP jest protokołem tylko do odczytu ale po
zainstalowaniu DAVa staje się on również zapisywalnym. Co więcej jeśli
używasz DAVfs to możesz montować swój serwer WWW jako system plików i
używać tak jak normalnego dysku.

Ten pakiet zawiera wersję davfs korzystającą z cache'u.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{_mandir}/{man5,man8}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -d $RPM_BUILD_ROOT%{_var}/cache/%{name}

install src/{,u}mount.davfs $RPM_BUILD_ROOT/sbin
install etc/{davfs2.conf,secrets} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 322 davfs2
%useradd -u 322 -r -d /var/cache/%{name} -s /bin/false -c "DAVfs User" -g davfs2 davfs2

%postun
if [ "$1" = "0" ]; then
	%userremove davfs2
	%groupremove davfs2
fi

%files
%defattr(644,root,root,755)

%doc ABOUT-NLS COPYING INSTALL README.translators aclocal.m4 AUTHORS ChangeLog NEWS THANKS BUGS FAQ README TODO
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/%{name}/secrets
%config %{_sysconfdir}/%{name}/davfs2.conf

%attr(755,root,root) /sbin/*
%attr(755,davfs2,davfs2) %{_var}/cache/%{name}
