#!/usr/bin/env python
"""
:Copyright: |copy| 2007 by Adrian Hare and Kenneth Barber. All rights reserved.

.. |copy| unicode:: 0xA9 .. copyright sign

:license: 
    This file is part of OWLSugar.

    OWLSugar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OWLSugar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

:Version: $Rev: 173 $

Setup tools.
"""
__docformat__ = 'restructuredtext en' 

from setuptools import setup

setup(
    name = "owlsugar",
    version = '0.1',
    author="Organic dev team",
    author_email="dev@organictechnology.net",
    maintainer="Organic dev team",
    maintainer_email="dev@organictechnology.net",
    url="http://organictechnology.net/somewhere",
    description="OO based library interface to OWL/RDF",
    package_dir = {'': 'src'},
    packages = ['owlsugar'],
)