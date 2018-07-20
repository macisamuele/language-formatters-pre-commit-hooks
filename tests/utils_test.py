# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from language_formatters_pre_commit_hooks.utils import run_command


@pytest.mark.parametrize(
    'command, expected_status, expected_output',
    [
        ['echo "1"', 0, '1\n'],
        ['echo "1" | grep 0', 1, ''],
        ['true', 0, ''],
        ['false', 1, ''],
    ],
)
def test_run_command(command, expected_status, expected_output):
    assert run_command(command) == (expected_status, expected_output)
