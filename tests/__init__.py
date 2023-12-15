# -*- coding: utf-8 -*-
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
    yield getattr(passed_function, "__wrapped__", passed_function)


class UnexpectedStatusCode(Exception):
    def __init__(self, parameters: typing.List[str], expected_status_code: int, actual_status_code: int) -> None:
        super().__init__()
        self.parameters = parameters
        self.expected_status_code = expected_status_code
        self.actual_status_code = actual_status_code

    def __str__(self) -> str:
        return (
            f"Execution of {self.parameters} is expected to terminate"
            f" with status code={self.expected_status_code}."
            f" Actual status code={self.actual_status_code}"
        )


def run_autofix_test(
    tmpdir: py.path.local,
    method: typing.Callable[[typing.List[str]], int],
    not_pretty_formatted_path: str,
    formatted_path: str,
    extra_parameters: typing.Optional[typing.List[str]] = None,
) -> None:
    extra_parameters = [] if extra_parameters is None else extra_parameters
    tmpdir.mkdir("src")
    not_pretty_formatted_tmp_path = tmpdir.join("src").join(basename(not_pretty_formatted_path))

    # It is a relative paths as KTLint==0.41.0 dropped support for absolute paths
    not_pretty_formatted_tmp_strpath = str(tmpdir.bestrelpath(not_pretty_formatted_tmp_path))

    copyfile(not_pretty_formatted_path, not_pretty_formatted_tmp_path)
    with change_dir_context(tmpdir.strpath):
        parameters = extra_parameters + ["--autofix"] + [not_pretty_formatted_tmp_strpath]
        status_code = method(parameters)
        if status_code != 1:
            raise UnexpectedStatusCode(parameters=parameters, expected_status_code=1, actual_status_code=status_code)

    # file was formatted (shouldn't trigger linter again)
    with change_dir_context(tmpdir.strpath):
        parameters = extra_parameters + ["--autofix", not_pretty_formatted_tmp_strpath]
        status_code = method(parameters)
        if status_code != 0:
            raise UnexpectedStatusCode(parameters=parameters, expected_status_code=0, actual_status_code=status_code)

    assert not_pretty_formatted_tmp_path.read_text("utf-8") == py.path.local(formatted_path).read_text("utf-8")
