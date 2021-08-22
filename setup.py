# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    extras_require={
        ":python_version<'3.5'": ["typing"],
    },
    entry_points={
        "console_scripts": [
            "pretty-format-golang = language_formatters_pre_commit_hooks.pretty_format_golang:pretty_format_golang",
            "pretty-format-java = language_formatters_pre_commit_hooks.pretty_format_java:pretty_format_java",
            "pretty-format-kotlin = language_formatters_pre_commit_hooks.pretty_format_kotlin:pretty_format_kotlin",
            "pretty-format-ini = language_formatters_pre_commit_hooks.pretty_format_ini:pretty_format_ini",
            "pretty-format-rust = language_formatters_pre_commit_hooks.pretty_format_rust:pretty_format_rust",
            "pretty-format-toml = language_formatters_pre_commit_hooks.pretty_format_toml:pretty_format_toml",
            "pretty-format-yaml = language_formatters_pre_commit_hooks.pretty_format_yaml:pretty_format_yaml",
        ],
    },
)
