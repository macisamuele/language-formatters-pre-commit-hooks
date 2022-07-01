# -*- coding: utf-8 -*-
import os
import shutil
import subprocess  # nosec B404 B603
import sys
import tempfile
import typing
from urllib.parse import urlparse

import requests


def run_command(*command: str) -> typing.Tuple[int, str]:
    print("[cwd={cwd}] Run command: {command}".format(command=command, cwd=os.getcwd()), file=sys.stderr)
    return_code, output = 1, ""
    try:
        return_code, output = (
            0,
            subprocess.check_output(  # nosec: disable=B603
                command,
                stderr=subprocess.STDOUT,
            ).decode("utf-8"),
        )
    except subprocess.CalledProcessError as e:
        return_code, output = e.returncode, e.output.decode("utf-8")
    print("[return_code={return_code}] | {output}".format(return_code=return_code, output=output), file=sys.stderr)
    return return_code, output


def _base_directory() -> str:
    # Extracted from pre-commit code:
    # https://github.com/pre-commit/pre-commit/blob/master/pre_commit/store.py
    return os.path.realpath(
        os.environ.get(str("PRE_COMMIT_HOME"))
        or os.path.join(
            os.environ.get(str("XDG_CACHE_HOME")) or os.path.expanduser("~/.cache"),
            "pre-commit",
        ),
    )


def download_url(url: str, file_name: typing.Optional[str] = None) -> str:
    base_directory = _base_directory()

    final_file = os.path.join(
        base_directory,
        file_name or os.path.basename(urlparse(url).path),
    )

    if os.path.exists(final_file):
        return final_file

    if not os.path.exists(base_directory):  # pragma: no cover
        # If the base directory is not present we should create it.
        # This is needed to allow the tool to run if invoked via
        # command line, but it should never be possible if invoked
        # via `pre-commit` as it would ensure that the directories
        # are present
        print("Unexisting base directory ({base_directory}). Creating it".format(base_directory=base_directory), file=sys.stderr)
        os.makedirs(base_directory)

    print("Downloading {url}".format(url=url), file=sys.stderr)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(dir=base_directory, delete=False) as tmp_file:  # Not delete because we're renaming it
        tmp_file_name = tmp_file.name
        shutil.copyfileobj(r.raw, tmp_file)
        tmp_file.flush()
        os.fsync(tmp_file.fileno())

    os.rename(tmp_file_name, final_file)

    return final_file


def remove_trailing_whitespaces_and_set_new_line_ending(string: str) -> str:
    return "{content}\n".format(
        content="\n".join(line.rstrip() for line in string.splitlines()).rstrip(),
    )
