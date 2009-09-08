Summary:	Web-based Distributed Authoring and Versioning - caching version
Summary(pl.UTF-8):	Bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie - wersja z cache
Name:		davfs2
Version:	1.4.1
Release:	0.2
License:	GPL
Group:		Networking/Utilities
Source0:	http://download.savannah.gnu.org/releases-noredirect/%{name}/%{name}-%{version}.tar.gz
URL:		http://savannah.nongnu.org/projects/davfs2
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	neon-devel >= 0.24
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.118
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

#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
%configure --sbindir=/sbin

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_var}/cache/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 242 davfs2
%useradd -u 242 -r -d /var/cache/%{name} -s /bin/false -c "DAVfs User" -g davfs2 davfs2

%postun
if [ "$1" = "0" ]; then
	%userremove davfs2
	%groupremove davfs2
fi

%files -f %{name}.lang
%defattr(644,root,root,755)

%doc %{_docdir}/*

%{_mandir}/man5/*
%{_mandir}/man8/*
%{_usr}/share/%{name}/*

%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/%{name}/secrets
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%attr(755,root,root) /sbin/mount.davfs
%attr(755,root,root) /sbin/umount.davfs
%attr(755,davfs2,davfs2) %{_var}/cache/%{name}

%lang(de) %{_mandir}/de/man5/*
%lang(de) %{_mandir}/de/man8/*

%lang(es) %{_mandir}/es/man5/*
