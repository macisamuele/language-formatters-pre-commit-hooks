import pkg_resources


__version__ = pkg_resources.get_distribution("language_formatters_pre_commit_hooks").version


def _get_default_version(tool_name: str) -> str:  # pragma: no cover
    """
    Read tool_name default version.
    The method is intended to be used only from language_formatters_pre_commit_hooks modules
    """
    try:
        with open(
            pkg_resources.resource_filename(
                "language_formatters_pre_commit_hooks",
                f"{tool_name}.version",
            )
        ) as f:
            return f.readline().split()[0]
    except:  # noqa: E722 (allow usage of bare 'except')  # pragma: no cover
        raise RuntimeError(f"No default version found for {tool_name}")
