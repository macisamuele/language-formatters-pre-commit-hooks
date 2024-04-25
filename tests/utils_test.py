# -*- coding: utf-8 -*-
import os
from os.path import basename
from unittest.mock import patch
from urllib.parse import urljoin
from urllib.request import pathname2url

import pytest

from language_formatters_pre_commit_hooks.utils import does_checksum_match
from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import run_command


@pytest.mark.parametrize(
    "command, expected_status, expected_output, expected_stderr",
    [
        (["echo", "1"], 0, "1\n", ""),
        (["true"], 0, "", ""),
        (["false"], 1, "", ""),
    ],
)
def test_run_command(command, expected_status, expected_output, expected_stderr):
    assert run_command(*command) == (expected_status, expected_output, expected_stderr)


@pytest.mark.parametrize(
    "url, does_file_already_exist",
    [
        [urljoin("file://", pathname2url(__file__)), True],
        [urljoin("file://", pathname2url(__file__)), False],
    ],
)
@patch("language_formatters_pre_commit_hooks.utils.shutil", autospec=True)
@patch("language_formatters_pre_commit_hooks.utils.requests", autospec=True)
def test_download_url(mock_requests, mock_shutil, tmpdir, url, does_file_already_exist):
    if does_file_already_exist:
        with open(os.path.join(tmpdir.strpath, basename(url)), "w") as f:
            f.write(str(""))

    with patch.dict(os.environ, {"PRE_COMMIT_HOME": tmpdir.strpath}):
        assert download_url(url) == os.path.join(tmpdir.strpath, basename(url))

    if does_file_already_exist:
        assert not mock_requests.get.called
    else:
        mock_requests.get.assert_called_once_with(url, stream=True)


@pytest.mark.parametrize(
    ("checksum", "expected"),
    (
        ("486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7", True),
        ("2d32af8ef04ffbf0ae77fc7953e86871b85143b29d51f9794466842f68f5fb48", False),
    ),
)
def test_does_checksum_match(tmpdir, checksum, expected):
    hello = tmpdir.join("hello.txt")
    hello.write("world")
    assert does_checksum_match(str(hello), checksum) is expected
