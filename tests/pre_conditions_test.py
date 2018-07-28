# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import mock
import pytest

from language_formatters_pre_commit_hooks.pre_conditions import _assert_command_succeed
from language_formatters_pre_commit_hooks.pre_conditions import golang_required
from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.pre_conditions import rust_required


@pytest.fixture(params=[True, False])
def success(request):
    with mock.patch(
        'language_formatters_pre_commit_hooks.pre_conditions.run_command',
        autospec=True,
        return_value=(0 if request.param else 1, None),
    ):
        yield request.param


def test___assert_command_succeed(success):
    raised_exception = None
    try:
        _assert_command_succeed('command', 'assert_message')
    except AssertionError as e:
        raised_exception = e

    if success:
        assert raised_exception is None
    else:
        assert isinstance(raised_exception, AssertionError) and 'assert_message' == str(raised_exception)


@pytest.mark.parametrize(
    'decorator, assert_content',
    [
        [java_required, 'JRE is required'],
        [golang_required, 'golang/gofmt is required'],
        [rust_required, 'rustfmt is required'],
    ],
)
def test_tool_required(success, decorator, assert_content):
    @decorator
    def func():
        pass

    raised_exception = None
    try:
        func()
    except AssertionError as e:
        raised_exception = e

    if success:
        assert raised_exception is None
    else:
        assert isinstance(raised_exception, AssertionError) and assert_content in str(raised_exception)
