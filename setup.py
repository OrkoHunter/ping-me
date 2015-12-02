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
        long_description = open('README.md').read(),
        packages = ['ping_me',
                    'ping_me.depends',
                    'ping_me.data',
                    'ping_me.utils'],
        data_files = [('ping_me/data', ['ping_me/data/countrylist.csv'])],
        license = 'Apache License',
        entry_points = {
            'console_scripts': [
            'ping-me = ping_me.ping:main'
            ]
        },
        test_suite = 'nose.collector',
        tests_require = ['nose>=0.10.1']
    )
