#!/usr/bin/env python3

"""Setup.py for dxdt package."""

import os
from setuptools import setup, find_packages


def read(fname):
    """Utility function to insert the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='dxdt',
    version='0.6',
    packages=find_packages(exclude=['tests']),

    # py_modules=[
    #     'dxdt',
    #     'dxdtcli',
    #     'dxdtconf',
    # ],

    description=('Notational Velocity for every file.'),
    long_description=read('README.md'),

    author='Daniel Theriault',
    author_email='dannymt97@gmail.com',
    license='MIT',

    install_requires=[
        'argcomplete',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: MIT License',
        'Environment :: Console'
    ],

    entry_points={
        'console_scripts': [
            'dxdt = dxdt.cli:main',
        ]
    }
)
