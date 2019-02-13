#!/usr/bin/env python

from os.path import abspath, dirname, exists, join

from setuptools import find_packages, setup

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements(
    join(
        dirname(abspath(__file__)),
        'requirements',
        'sdk.txt',
    ), session='None')

here = dirname(abspath(__file__))
with open(join(here, 'VERSION')) as f:
    VERSION = f.read()

packages = find_packages(exclude=['tests*'])

doc = ''
if exists('README.md'):
    doc = open('README.md', 'r').read()

setup(
    name='connect-sdk',
    author='Ingram Micro',
    version=VERSION,
    keywords='sdk connect connect automation',
    packages=packages,
    description='Connect Python SDK',
    long_description=doc,
    long_description_content_type='text/markdown',
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

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
)
