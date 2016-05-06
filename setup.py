#!/usr/bin/env python
# This file is part of django-url-sso.
#
# django-url-sso: Generate login URL's for unstandardized SSO systems.
# Copyright (C) 2014 Mathijs de Bruin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import warnings

from setuptools import setup, find_packages

try:
    README = open('README.rst').read() + '\n\n'
    README += open('CHANGES.rst').read()
except:
    warnings.warn('Could not read README.rst and/or CHANGES.rst')
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    warnings.warn('Could not read requirements.txt')
    REQUIREMENTS = None

try:
    TEST_REQUIREMENTS = open('requirements_test.txt').read()
except:
    warnings.warn('Could not read requirements_test.txt')
    TEST_REQUIREMENTS = None


setup(
    name='django-wishlist',
    version='1.0',
    description='Generic user wishlists for use with any Django model.',
    long_description=README,
    install_requires=REQUIREMENTS,
    license='AGPL',
    author='Mathijs de Bruin',
    author_email='mathijs@mathijsfietst.nl',
    url='https://github.com/dokterbob/django-wishlist/',
    packages=find_packages(exclude=("tests", "test_project")),
    include_package_data=True,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ),
    test_suite='runtests.run_tests',
    tests_require=TEST_REQUIREMENTS
)
