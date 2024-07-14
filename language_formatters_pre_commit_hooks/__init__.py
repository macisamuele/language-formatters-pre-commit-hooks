# -*- coding: utf-8 -*-
from importlib import metadata


__version__ = metadata.version("language_formatters_pre_commit_hooks")


def _get_default_version(tool_name: str) -> str:  # pragma: no cover
    """
    Read tool_name default version.
    The method is intended to be used only from language_formatters_pre_commit_hooks modules
    """
    version_file = "{tool_name}.version".format(tool_name=tool_name)
    try:
        for file in metadata.files("language_formatters_pre_commit_hooks") or ():
            if file.name == version_file:
                return file.read_text().strip()

        raise RuntimeError("Default version for {tool_name} is not found".format(tool_name=tool_name))
    except:  # noqa: E722 (allow usage of bare 'except')  # pragma: no cover
        raise RuntimeError("No default version found for {tool_name}".format(tool_name=tool_name))
