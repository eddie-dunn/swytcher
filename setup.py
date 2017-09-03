#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=fixme


from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click>=6.0',
    'python-xlib',
    'xkbgroup',
]

test_requirements = [
    'tox',
]

setup(
    name='swytcher',
    version='0.3.1',
    description="Automatically switch layout based on your active window",
    long_description=readme + '\n\n' + history,
    author="Eddie Dunn",
    author_email='eddie.dunn@gmail.com',
    url='https://github.com/eddie-dunn/swytcher',
    packages=[
        'swytcher',
    ],
    package_dir={'swytcher': 'swytcher'},
    entry_points={
        'console_scripts': [
            'swytcher=swytcher.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='keyboard layout switcher',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
