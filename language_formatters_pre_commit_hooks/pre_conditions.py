# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from decorator import decorator

from language_formatters_pre_commit_hooks.utils import run_command

_DEFAULT_MESSAGE_TEMPLATE = '{required_tool} is required to run this pre-commit hook. ' \
                            'Make sure that you have it installed and available on your path.\n' \
                            'Download/Install URL: {install_url}'


def _assert_command_succeed(command, assertion_error_message):
    status, _ = run_command(command)
    assert status == 0, assertion_error_message


@decorator
def java_required(f, *args, **kwargs):
    _assert_command_succeed(
        command='java -version',
        assertion_error_message=_DEFAULT_MESSAGE_TEMPLATE.format(
            required_tool='JRE',
            install_url='https://www.java.com/en/download/',
        ),
    )
    return f(*args, **kwargs)


@decorator
def golang_required(f, *args, **kwargs):
    _assert_command_succeed(
        command='go version',
        assertion_error_message=_DEFAULT_MESSAGE_TEMPLATE.format(
            required_tool='golang/gofmt',
            install_url='https://golang.org/doc/install#download',
        ),
    )

    return f(*args, **kwargs)


@decorator
def rust_required(f, *args, **kwargs):
    _assert_command_succeed(
        command='cargo +nightly fmt  -- --version',
        assertion_error_message=_DEFAULT_MESSAGE_TEMPLATE.format(
            required_tool='rustfmt',
            install_url='https://github.com/rust-lang-nursery/rustfmt#quick-start',
        ),
    )

    return f(*args, **kwargs)
