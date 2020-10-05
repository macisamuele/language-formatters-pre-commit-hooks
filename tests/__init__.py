# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import typing
from contextlib import contextmanager
from posixpath import basename
from shutil import copyfile

if getattr(typing, "TYPE_CHECKING", False):
    import py

    F = typing.TypeVar("F", bound=typing.Callable)


@contextmanager
def change_dir_context(directory):
    # type: (typing.Text) -> typing.Generator[None, None, None]
    working_directory = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(working_directory)


@contextmanager
def undecorate_function(func):
    # type: (F) -> typing.Generator[F, None, None]
    passed_function = func
    func = getattr(passed_function, "__wrapped__", passed_function)
    yield func
    func = passed_function


def __read_file(path):
    # type: (typing.Text) -> typing.Text
    with open(path) as f:
        return "".join(f.readlines())


def run_autofix_test(
    tmpdir,  # type: py.path.local
    method,  # type: typing.Callable[[typing.List[typing.Text]], int]
    not_pretty_formatted_path,  # type: typing.Text
    formatted_path,  # type: typing.Text
):
    # type: (...) -> None
    tmpdir.mkdir("src")
    not_pretty_formatted_tmp_path = tmpdir.join("src").join(basename(not_pretty_formatted_path)).strpath

    copyfile(not_pretty_formatted_path, not_pretty_formatted_tmp_path)
    with change_dir_context(tmpdir.strpath):
        assert method(["--autofix", not_pretty_formatted_tmp_path]) == 1

    # file was formatted (shouldn't trigger linter again)
    with change_dir_context(tmpdir.strpath):
        assert method(["--autofix", not_pretty_formatted_tmp_path]) == 0

    assert __read_file(not_pretty_formatted_tmp_path) == __read_file(formatted_path)
