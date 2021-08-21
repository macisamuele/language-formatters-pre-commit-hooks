# -*- coding: utf-8 -*-
import typing
from unittest.mock import patch

import pytest

from language_formatters_pre_commit_hooks.pre_conditions import _is_command_success
from language_formatters_pre_commit_hooks.pre_conditions import _ToolRequired
from language_formatters_pre_commit_hooks.pre_conditions import golang_required
from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.pre_conditions import rust_required
from language_formatters_pre_commit_hooks.pre_conditions import ToolNotInstalled


@pytest.fixture(params=[True, False])
def success(request):
    with patch(
        "language_formatters_pre_commit_hooks.pre_conditions.run_command",
        autospec=True,
        return_value=(0 if request.param else 1, ""),
    ):
        yield request.param


@pytest.mark.parametrize(
    "matcher, expected_matcher_result",
    (
        (None, True),
        (lambda output: output == "", True),
        (lambda output: output != "", False),
    ),
)
def test__is_command_success(
    success: bool,
    matcher: typing.Optional[typing.Callable[[str], bool]],
    expected_matcher_result: bool,
) -> None:

    assert (success and expected_matcher_result) == _is_command_success(
        "cmd",
        "with",
        "args",
        output_should_match=matcher,
    )


def test__ToolRequired(success: bool) -> None:
    decorator = _ToolRequired(tool_name="test", check_command=lambda _: success, download_install_url="url")
    assert decorator.is_tool_installed() == success

    def throw_exception():
        raise SyntaxError("This error is thrown by the decorated function")

    try:
        decorator(throw_exception)()
    except Exception as e:
        raised_exception = e

    if success:
        assert isinstance(raised_exception, SyntaxError)
    else:
        assert isinstance(raised_exception, ToolNotInstalled)
        assert raised_exception.tool_name == "test"
        assert raised_exception.download_install_url == "url"


@pytest.mark.parametrize(
    "decorator, assert_content",
    [
        [java_required, "JRE is required"],
        [golang_required, "golang/gofmt is required"],
        [rust_required, "rustfmt is required"],
    ],
)
def test_tool_required(success, decorator, assert_content):
    @decorator
    def func():
        pass

    raised_exception = None
    try:
        func()
    except ToolNotInstalled as e:
        raised_exception = e

    if success:
        assert raised_exception is None
    else:
        assert isinstance(raised_exception, ToolNotInstalled) and assert_content in str(raised_exception)
