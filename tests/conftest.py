import os
import typing
from unittest.mock import patch

import py
import pytest


def _is_running_in_ci() -> bool:
    return bool(os.environ.get("CI"))


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=True if _is_running_in_ci() else False,
        help="Run integration tests (aka. download external resources)",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as integration test (aka. download external resources)")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-integration"):
        return

    skip_integration = pytest.mark.skip(reason="need --run-integration option to run or CI env variable defined")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@pytest.fixture
def ensure_download_possible(tmpdir: py.path.local) -> typing.Generator[None, None, None]:
    with patch.dict(
        os.environ,
        {
            # Patch PRE_COMMIT_HOME using a temporary directory to ensure that
            # we do actually download the pointed JAR
            "PRE_COMMIT_HOME": tmpdir.realpath().strpath,
        },
    ), patch(
        # Mock copyfileobj such that we don't really download all the content
        # after all we do care only about being able to start receiving the file
        # because it would be sufficient to prove that the path is correct
        "language_formatters_pre_commit_hooks.utils.shutil.copyfileobj",
        autospec=True,
    ):
        yield
