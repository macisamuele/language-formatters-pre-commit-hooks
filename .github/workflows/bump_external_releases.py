# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import sys
import traceback
from pathlib import Path
from subprocess import check_call
from subprocess import PIPE
from urllib.request import urlopen


if sys.version_info < (3, ):
    raise RuntimeError("Script build to support Python3 only. Sorry ;(")


def bump_release(github_project, file_name, constant_name):
    try:
        with urlopen(f"https://api.github.com/repos/{github_project}/releases/latest") as request:
            latest_version = json.load(request)["name"]
    except:  # noqa: E722 (allow usage of bare 'except')
        traceback.print_exc()
        return None

    with (Path("language_formatters_pre_commit_hooks") / file_name).open(mode="r+") as f:
        should_update_file = False
        lines = []
        for line in f.readlines():
            if line.startswith(f"{constant_name} ="):
                loaded_line = {}
                exec(line, None, loaded_line)  # noqa: E211
                if loaded_line[constant_name].split(".") < latest_version.split("."):
                    should_update_file = True
                    lines.append(f'{constant_name} = "{latest_version}"\n')
                else:
                    break
            else:
                lines.append(line)

        if should_update_file:
            f.seek(0)
            f.writelines(lines)
            return latest_version

        return None


def add_and_commit(file_name, message):
    check_call(args=["git", "add", (Path("language_formatters_pre_commit_hooks") / file_name).absolute()], stdout=PIPE)
    check_call(args=["git", "commit", "-m", message], stdout=PIPE)


def bump_ktlint():
    bumped_released_version = bump_release(
        github_project="pinterest/ktlint",
        file_name="pretty_format_kotlin.py",
        constant_name="__KTLINT_VERSION",
    )
    if bumped_released_version:
        message = f"Bump KTLint to version {bumped_released_version}"
        print(message)
        add_and_commit(file_name="pretty_format_kotlin.py", message=message)
    return bool(bumped_released_version)


def bump_google_java_formatter():
    bumped_released_version = bump_release(
        github_project="google/google-java-format",
        file_name="pretty_format_java.py",
        constant_name="__GOOGLE_JAVA_FORMATTER_VERSION",
    )
    if bumped_released_version:
        message = f"Bump Google Java Formatter to version {bumped_released_version}"
        print(message)
        add_and_commit(file_name="pretty_format_java.py", message=message)
    return bool(bumped_released_version)


if __name__ == "__main__":
    exit(
        0 if bump_ktlint() | bump_google_java_formatter() else 1,
    )
