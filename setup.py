#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'requests>=2.12.0'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='rt_factory',
    version='0.2.2',
    description="Pythonic wrapper for the artifactory API",
    long_description=readme + '\n\n' + history,
    author="Peter Tillemans",
    author_email='pti@melexis.com',
    url='https://github.com/melexis/rt_factory',
    packages=[
        'rt_factory',
    ],
    package_dir={'rt_factory': 'rt_factory'},
    entry_points={
        'console_scripts': [
            'rt_factory=rt_factory.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='rt_factory',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Software Distribution',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
