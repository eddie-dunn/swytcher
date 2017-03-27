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
    'Click>=6.0',
    'python-xlib',
    'xkbgroup',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='swytcher',
    version='0.1.0',
    description="Automatic",
    long_description=readme + '\n\n' + history,
    author="Eddie Dunn",
    author_email='eddie.dunn@gmail.com',
    url='https://github.com/eddie-dunn/swytcher',
    packages=[
        'swytcher',
    ],
    package_dir={'swytcher':
                 'swytcher'},
    data_files = [
        ('', ['swytcher/log_conf.ini', 'swytcher/config.ini']),
    ],
    entry_points={
        'console_scripts': [
            'swytcher=swytcher.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='swytcher',
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
