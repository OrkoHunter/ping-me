#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print('To install, run \'python setup.py install\'')
    print()

NAME = 'ping-me'
VERSION = '0.1'

if __name__ == "__main__":
    setup(
        name = NAME,
        version = VERSION,
        author = 'Himanshu Mishra',
        author_email = 'himanshumishra@iitkgp.ac.in',
        description = 'Cross platform personalized ping',
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
                            'python-dateutil'],
        test_suite = 'nose.collector',
        tests_require = ['nose>=0.10.1']
    )
