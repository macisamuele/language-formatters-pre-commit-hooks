# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import subprocess  # nosec: disable=B603
import sys
import traceback
from pathlib import Path
from urllib.request import urlopen


if sys.version_info < (3, 6):
    raise RuntimeError("Script build to support Python3.6+ only. Sorry ;(")


def bump_release(github_project, tool_name):
    try:
        with urlopen(f"https://api.github.com/repos/{github_project}/releases/latest") as request:  # nosec: disable=B310
            latest_version = json.load(request)["name"]
    except:  # noqa: E722 (allow usage of bare 'except')
        traceback.print_exc()
        return False

    tool_name_version_path = Path("language_formatters_pre_commit_hooks") / f"{tool_name}.version"
    with tool_name_version_path.open(mode="r") as f:
        default_version = f.readline().split()[0]

    if default_version == latest_version:
        return False

    with tool_name_version_path.open(mode="w") as f:
        f.write(f"{latest_version}\n")

    message = f"Bump {tool_name} to version {latest_version}"
    print(message)

    def call(*args):
        print(f"Executing: {args}")
        subprocess.check_call(args=args, stdout=subprocess.PIPE)  # nosec: disable=B603

    call("pre-commit", "run", str(tool_name_version_path.absolute()))
    call("git", "add", str(tool_name_version_path.absolute()))
    call("git", "commit", "-m", message)

    return True


def bump_ktlint():
    return bump_release(
        github_project="pinterest/ktlint",
        tool_name="ktlint",
    )


def bump_google_java_formatter():
    return bump_release(
        github_project="google/google-java-format",
        tool_name="google_java_formatter",
    )


if __name__ == "__main__":
    something_is_bumped = False
    for bumper in (bump_ktlint, bump_google_java_formatter):
        something_is_bumped |= bumper()

    if not something_is_bumped:
        print("No tool need to be bumped")
