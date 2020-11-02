#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from os.path import exists
from setuptools import find_packages, setup

import pathlib
import pkg_resources

# noinspection PyTypeChecker
with pathlib.Path('requirements/sdk.txt').open() as requirements_txt:
    install_reqs = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

PACKAGES = find_packages(exclude=['tests*'])

DOC = ''
if exists('README.md'):
    DOC = open('README.md', 'r').read()

setup(
    name='connect-sdk',
    author='CloudBlue Connect',
    keywords='sdk connect connect automation',
    packages=PACKAGES,
    description='Connect Python SDK',
    long_description=DOC,
    long_description_content_type='text/markdown',
    url='https://github.com/ingrammicro/connect-python-sdk',
    license='Apache Software License',
    include_package_data=True,
    install_requires=install_reqs,
    setup_requires=['setuptools_scm', 'pytest-runner', 'wheel'],
    use_scm_version=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',

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
