#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit vantage6-algorithms/__version__.py
version = {}
with open(os.path.join(here, 'vantage6_algorithms', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='vantage6_algorithms',
    version=version['__version__'],
    description="Algorithms developed for running on Vantage6",
    long_description=readme + '\n\n',
    author="Djura Smits",
    author_email='dsmits@esciencecenter.nl',
    url='https://github.com/NLeSC/vantage6-algorithms',
    packages=[
        'vantage6_algorithms',
    ],
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='vantage6-algorithms',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    install_requires=[],  # FIXME: add your package's dependencies to this list
    setup_requires=[
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'],
    }
)
