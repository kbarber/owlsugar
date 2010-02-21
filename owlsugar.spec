# Copyright 2007 by Adrian Hare and Kenneth Barber. All rights reserved.

#    This file is part of OWLSugar.

#    OWLSugar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    OWLSugar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Version: $Ref$

# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           owlsugar
Version:        0.1
Release:        1%{?dist}
Summary:        Summary of the package

Group:          Development/Libraries
License:        GPL
URL:            http://
Source0:        archive_name-%{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      
BuildRequires:  python-devel

%description


%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
# For noarch packages: sitelib
%{python_sitelib}/*
# For arch-specific packages: sitearch
%{python_sitearch}/*


%changelog
