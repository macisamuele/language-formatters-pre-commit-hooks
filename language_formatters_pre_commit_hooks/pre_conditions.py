# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import typing
from functools import wraps
from os import getenv

from language_formatters_pre_commit_hooks.utils import run_command


if getattr(typing, "TYPE_CHECKING", False):
    F = typing.TypeVar("F", bound=typing.Callable[..., int])


def _is_command_success(*command_args):
    # type: (typing.Text) -> bool
    exit_status, _ = run_command(*command_args)
    return exit_status == 0


class ToolNotInstalled(RuntimeError):
    def __init__(self, tool_name, download_install_url):
        # type: (typing.Text, typing.Text) -> None
        self.tool_name = tool_name
        self.download_install_url = download_install_url

    def __str__(self):
        # type: () -> str
        return str(
            "{tool_name} is required to run this pre-commit hook.\n"
            "Make sure that you have it installed and available on your path.\n"
            "Download/Install URL: {download_install_url}".format(
                tool_name=self.tool_name,
                download_install_url=self.download_install_url,
            )
        )


class _ToolRequired(object):
    def __init__(self, tool_name, check_command, download_install_url):
        # type: (typing.Text, typing.Callable[[], bool], typing.Text) -> None
        self.tool_name = tool_name
        self.check_command = check_command
        self.download_install_url = download_install_url

    def is_tool_installed(self):
        # type: () -> bool
        return self.check_command()

    def __call__(self, f):
        # type: (F) -> F
        @wraps(f)
        def wrapper(*args, **kwargs):
            # type: (typing.Any, typing.Any) -> int
            if not self.is_tool_installed():
                raise ToolNotInstalled(
                    tool_name=self.tool_name,
                    download_install_url=self.download_install_url,
                )

            return f(*args, **kwargs)

        return wrapper  # type: ignore


java_required = _ToolRequired(
    tool_name="JRE",
    check_command=lambda: _is_command_success("java", "-version"),
    download_install_url="https://www.java.com/en/download/",
)

golang_required = _ToolRequired(
    tool_name="golang/gofmt",
    check_command=lambda: _is_command_success("go", "version"),
    download_install_url="https://golang.org/doc/install#download",
)


rust_required = _ToolRequired(
    tool_name="rustfmt",
    check_command=(lambda: _is_command_success("cargo", "+{}".format(getenv("RUST_TOOLCHAIN", "stable")), "fmt", "--", "--version")),
    download_install_url="https://github.com/rust-lang-nursery/rustfmt#quick-start",
)
