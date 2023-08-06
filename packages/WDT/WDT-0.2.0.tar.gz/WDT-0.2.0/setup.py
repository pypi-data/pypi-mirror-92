#!/usr/bin/env python
# -*- coding: utf-8 -*-

# convert README.md to README.rst
# pandoc --from markdown --to rst README.md -o README.rst



# uninstall
# % python setup.py install --record installed_files
# % cat installed_files | xargs rm -rf
# % rm installed_files

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name= 'WDT', # Application name:
    version= '0.2.0', # Version number

    author= 'Masayuki Tanaka', # Author name
    author_email= 'mastnk@gmail.com', # Author mail

    url='https://github.com/mastnk/WDT', # Details
    description='Watch Dog Timer for python.', # short description
    long_description=read('README.rst'), # long description
    install_requires=[ # Dependent packages (distributions)
    ],

    include_package_data=False, # Include additional files into the package
    packages=find_packages(exclude=('tests')),

    test_suite = 'tests',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)

