#!/usr/bin/env python3

import os
from setuptools import setup
import unittest

install_requires = [
    'docopt',
    'rosdep',
]

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('src/auto_abi_checker/tests', pattern='*_TEST.py')
    return test_suite

kwargs = {
    'name': 'auto-abi-checker',
    'version': '0.1.0',
    'packages': ['auto-abi-checker'],
    'package_dir': {'': 'src'},
    'author': 'Jose Luis Rivero',
    'author_email': 'jrivero@osrfoundation.org',
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License'
    ],
    'description': 'Tool to facilitate the run of abi-compliance-checker',
    'long_description': 'Tool designed to facilitate the run the great ABI compliance checker by supporting easy inputs and no configuration files',
    'license': 'Apache License 2.0',
    'python_requires': '>=3.0',

    'install_requires': install_requires,
    'url': 'https://github.com/osrf/auto-abi-checker'
}

setup(**kwargs, test_suite='setup.my_test_suite')
