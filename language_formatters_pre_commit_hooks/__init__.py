# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import typing

import pkg_resources


__version__ = pkg_resources.get_distribution("language_formatters_pre_commit_hooks").version


def _get_default_version(tool_name):  # pragma: no cover
    # type: (typing.Text) -> typing.Text
    """
    Read tool_name default version.
    The method is intended to be used only from language_formatters_pre_commit_hooks modules
    """
    try:
        with open(
            pkg_resources.resource_filename(
                "language_formatters_pre_commit_hooks",
                "{tool_name}.version".format(tool_name=tool_name),
            )
        ) as f:
            return f.readline().split()[0]
    except:  # noqa: E722 (allow usage of bare 'except')
        raise RuntimeError("No default version found for {tool_name}".format(tool_name=tool_name))
