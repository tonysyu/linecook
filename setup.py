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

install_requires = [
    'future',
    'termcolor',
    'toolz',
]

docs_require = [
    'sphinx',
    'sphinx-autobuild',
    'sphinx_rtd_theme',
    'sphinxcontrib-napoleon',
]

tests_require = [
    'coverage',
    'flake8',
    'mock',
    'pytest',
    'pytest-cov',
    'pytest-flake8',
    'pytest-sugar',
]

dev_requires = tests_require + docs_require + [
    'bumpversion',
    'ipdb',
    'ipython',
    'twine',
    'wheel',
]


setup(
    name='linecook',
    version='0.2.0',
    description='Prepare lines of text for easy consumption',
    long_description=long_description,
    url='https://github.com/tonysyu/linecook',
    author='Tony S. Yu',
    author_email='tsyu80@gmail.com',
    license='Modified BSD',
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
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'dev': dev_requires,
    },
    package_data={},
    entry_points={
        'console_scripts': [
            'linecook = linecook.cli:main',
        ],
    },
)
