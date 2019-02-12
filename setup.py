#!/usr/bin/env python

import os
from os.path import abspath, dirname, join
from setuptools import setup

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               'requirements.txt'), session='None')

here = abspath(dirname(__file__))

with open(join(here, 'VERSION')) as f:
    VERSION = f.read()

setup(
    name='connectsdk',
    author='Ingram Micro',
    version=VERSION,
    keywords='sdk connectsdk connect automation',
    packages=['connectsdk'],
    description='Connect Python SDK',
    long_description='Documentation is described on '
                     '`GitHub <https://github.com/ingrammicro/connect-python-sdk>`_',
    url='https://github.com/ingrammicro/connect-python-sdk',
    license='Apache Software License',
    include_package_data=True,
    install_requires=[str(ir.req) for ir in install_reqs],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
)
