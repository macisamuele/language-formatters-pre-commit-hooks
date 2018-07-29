# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import find_packages
from setuptools import setup

from language_formatters_pre_commit_hooks import __version__


setup(
    name=str('language_formatters_pre_commit_hooks'),
    description='List of pre-commit hooks meant to format your source code.',
    url='https://github.com/macisamuele/language-formatters-pre-commit-hooks',
    version=__version__,

    author='Samuele Maci',
    author_email='macisamuele@gmail.com',

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=[
        'decorator',
        'requests',
        'ruamel.yaml',
        'six',
        'toml',
    ],
    entry_points={
        'console_scripts': [
            'pretty-format-golang = language_formatters_pre_commit_hooks.pretty_format_golang:pretty_format_golang',
            'pretty-format-java = language_formatters_pre_commit_hooks.pretty_format_java:pretty_format_java',
            'pretty-format-kotlin = language_formatters_pre_commit_hooks.pretty_format_kotlin:pretty_format_kotlin',
            'pretty-format-ini = language_formatters_pre_commit_hooks.pretty_format_ini:pretty_format_ini',
            'pretty-format-rust = language_formatters_pre_commit_hooks.pretty_format_rust:pretty_format_rust',
            'pretty-format-toml = language_formatters_pre_commit_hooks.pretty_format_toml:pretty_format_toml',
            'pretty-format-yaml = language_formatters_pre_commit_hooks.pretty_format_yaml:pretty_format_yaml',
        ],
    },
)
