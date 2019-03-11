#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from os.path import abspath, dirname, exists, join
from os import environ
from setuptools import find_packages, setup

try:  # for pip >= 10
    # noinspection PyProtectedMember,PyPackageRequirements
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from pip.req import parse_requirements

# noinspection PyTypeChecker
install_reqs = parse_requirements(
    join(
        dirname(abspath(__file__)),
        'requirements',
        'sdk.txt',
    ), session='None')

VERSION = environ.get('TRAVIS_TAG')
PACKAGES = find_packages(exclude=['tests*'])

DOC = ''
if exists('README.md'):
    DOC = open('README.md', 'r').read()

setup(
    name='connect-sdk',
    author='Ingram Micro',
    version=VERSION,
    keywords='sdk connect connect automation',
    packages=PACKAGES,
    description='Connect Python SDK',
    long_description=DOC,
    long_description_content_type='text/markdown',
    url='https://github.com/ingrammicro/connect-python-sdk',
    license='Apache Software License',
    include_package_data=True,
    install_requires=[str(ir.req) for ir in install_reqs],

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
)
