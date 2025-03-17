#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests

Summary:	Python 2 tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona 2
Name:		python-fonttools
Version:	3.44.0
Release:	9
# basic license is BSD
# FontTools includes Adobe AGL & AGLFN, which is under 3-clauses BSD license
License:	MIT, BSD
Group:		Development/Tools
#Source0Download: https://github.com/fonttools/fonttools/releases
Source0:	https://github.com/fonttools/fonttools/archive/%{version}/fonttools-%{version}.tar.gz
# Source0-md5:	3f9ff311081a0f591a09552902671d29
Patch0:		%{name}-singledispatch.patch
URL:		https://github.com/fonttools/fonttools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-brotli
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-fs >= 2.2.0
BuildRequires:	python-pytest >= 3.0
BuildRequires:	python-unicodedata2 >= 12.0.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.750
%if %{with doc}
BuildRequires:	sphinx-pdg-2 >= 1.5.5
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-unicodedata2 >= 12.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 tools to manipulate font files.

%description -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona 2.

%package apidocs
Summary:	Documentation for Python fonttools module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona fonttools
Group:		Documentation

%description apidocs
Documentation for Python fonttools module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu Pythona fonttools.

%prep
%setup -q -n fonttools-%{version}
%patch -P 0 -p1

%build
export LC_ALL=C.UTF-8
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=Lib \
%{__python} -m pytest Tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-2/lib \
%{__make} -C Doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

# packaged from fonttools.spec
%{__rm} -r $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/fontTools
%{py_sitescriptdir}/fonttools-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/build/html/{_static,designspaceLib,misc,pens,ttLib,varLib,*.html,*.js}
%endif
