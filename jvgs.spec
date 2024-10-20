# rpm package built based on ArchLinux jvgs package
# https://aur.archlinux.org/packages.php?ID=34795

Name:		jvgs
Version:	0.5
Release:	1%{?dist}
Summary:	Minimalistic platform game loosely based on xkcd webcomic
License:	WTFPL
Group:		Games/Arcade
URL:		https://jvgs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz

# Extracted from https://aur.archlinux.org/packages/jv/jvgs/jvgs.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	freetype-devel
BuildRequires:	GL-devel
BuildRequires:	lua-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	swig
BuildRequires:	tinyxml-devel
Requires:	%{name}-data

# Do not bundle tinyxml, use system one
Patch0:		%{name}-tinyxml.patch

%description
This game takes place in a world much like ours, which has started
fading away. At a point where nearly everything has gone, a poet
finds himself, alone in a strange world of danger. He starts a journey
along the broken stream of thoughts that's left.

%package	data
Summary:	The %{name} resource data files
License:	CC-BY-SA
Group:		Games/Arcade
BuildArch:	noarch

%description	data
The %{name} resource data files.

%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p1

# Remove bundled library
rm -fr src/tinyxml

%build
CFLAGS="%{optflags}"
CXXFLAGS="%{optflags}"
FFLAGS="%{optflags}"
LDFLAGS="%{ldflags}"
%{_bindir}/cmake \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \
	-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
	-DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
%if "%{_lib}" == "lib64" 
	-DLIB_SUFFIX=64 \
%endif 
	-DBUILD_SHARED_LIBS:BOOL=ON \
	.
%make

%install
mkdir -p %{buildroot}{%{_gamesdatadir}/%{name}/resources,%{_bindir}}

install -D -p -m644 ./main.lua %{buildroot}%{_gamesdatadir}/%{name}/main.lua
install -D -p -m755 ./src/%{name} %{buildroot}%{_gamesdatadir}/%{name}/%{name}

install -D -p -m644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -p -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

pushd resources
    tar cf - * | (cd %{buildroot}%{_gamesdatadir}/%{name}/resources; tar xfp -)
popd

echo "#!/bin/sh

cd %{_gamesdatadir}/jvgs
./%{name} \"\$@\"" > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

%files
%doc AUTHORS
%doc README.markdown
%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/pixmaps/%{name}.png
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/%{name}
%{_gamesdatadir}/%{name}/main.lua

%files		data
%{_gamesdatadir}/%{name}/resources

%changelog
* Fri Feb 22 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.5-1
- Initial jvgs spec.
