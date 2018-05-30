# -*- coding: utf-8 -*-
"""Setup script for linecook terminal tool for .

See:
    https://packaging.python.org/en/latest/distributing.html
    https://github.com/pypa/sampleproject
"""
from __future__ import unicode_literals

from codecs import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='sample',
    version='0.1.0',
    description='',
    long_description=long_description,
    url='https://github.com/tonysyu/linecook',
    author='Tony S. Yu',
    author_email='tsyu80@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='console terminal logging parsing color sed termcolor',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'termcolor',
        'toolz',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'coverage',
        'flake8',
        'pytest',
        'pytest-cov',
        'pytest-flake8',
        'pytest-sugar',
    ],
    package_data={},
    entry_points={
        'console_scripts': [
            'linecook = linecook.cli:main',
        ],
    },
)
