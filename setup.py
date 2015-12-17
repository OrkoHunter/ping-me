#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print('To install, run \'python setup.py install\'')
    print()

sys.path.insert(0, 'ping_me')
import release

if __name__ == "__main__":
    setup(
        name = release.name,
        version = release.__version__,
        author = release.__author__,
        author_email = release.__email__,
        description = release.__description__,
        url='https://github.com/OrkoHunter/ping-me',
        keywords='ping me reminder cross platform',
        packages = ['ping_me',
                    'ping_me.data',
                    'ping_me.utils'],
        license = 'Apache License',
        entry_points = {
            'console_scripts': [
            'ping-me = ping_me.ping:main',
            'get-ping = ping_me.GET:main'
            ]
        },
        install_requires = ['phonenumbers', 'requests', 'pycrypto',
                            'python-dateutil', 'parsedatetime'],
        test_suite = 'nose.collector',
        tests_require = ['nose>=0.10.1']
    )
