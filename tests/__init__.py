# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import typing
from contextlib import contextmanager
from posixpath import basename
from shutil import copyfile

import py


F = typing.TypeVar("F", bound=typing.Callable)


@contextmanager
def change_dir_context(directory: str) -> typing.Generator[None, None, None]:
    working_directory = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(working_directory)


@contextmanager
def undecorate_function(func: F) -> typing.Generator[F, None, None]:
    passed_function = func
    func = getattr(passed_function, "__wrapped__", passed_function)
    yield func
    func = passed_function


def run_autofix_test(
    tmpdir: py.path.local,
    method: typing.Callable[[typing.List[str]], int],
    not_pretty_formatted_path: str,
    formatted_path: str,
) -> None:
    tmpdir.mkdir("src")
    not_pretty_formatted_tmp_path = tmpdir.join("src").join(basename(not_pretty_formatted_path))

    # It is a relative paths as KTLint==0.41.0 dropped support for absolute paths
    not_pretty_formatted_tmp_strpath = str(tmpdir.bestrelpath(not_pretty_formatted_tmp_path))

    copyfile(not_pretty_formatted_path, not_pretty_formatted_tmp_path)
    with change_dir_context(tmpdir.strpath):
        assert method(["--autofix", not_pretty_formatted_tmp_strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    with change_dir_context(tmpdir.strpath):
        assert method(["--autofix", not_pretty_formatted_tmp_strpath]) == 0

    assert not_pretty_formatted_tmp_path.read_text("utf-8") == py.path.local(formatted_path).read_text("utf-8")
