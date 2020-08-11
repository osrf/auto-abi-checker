#!/usr/bin/env python3

import os
from setuptools import setup
import unittest

install_requires = [
    'docopt',
    'rosdistro',
]

def discover_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('src/auto_abi_checker/tests', pattern='*_TEST.py')
    return test_suite

kwargs = {
    'name': 'auto_abi_checker',
    'version': '0.1.13',
    'packages': ['auto_abi_checker'],
    'package_dir': {'': 'src'},
    'author': 'Jose Luis Rivero',
    'author_email': 'jrivero@osrfoundation.org',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License'
    ],
    'description': 'Tool to facilitate the run of abi-compliance-checker',
    'long_description': 'Tool designed to facilitate the run the great ABI compliance checker by supporting easy inputs and no configuration files',
    'license': 'Apache License 2.0',
    'python_requires': '>=3.0',
    'scripts': ['src/auto_abi_checker/auto-abi.py'],
    'install_requires': install_requires,
    'url': 'https://github.com/osrf/auto-abi-checker',
    'test_suite': 'src/auto_abi_checker/test/auto-abi_TEST.py',
    'download_url': 'https://github.com/osrf/auto-abi-checker/archive/0.1.10.tar.gz',
}

setup(**kwargs)
