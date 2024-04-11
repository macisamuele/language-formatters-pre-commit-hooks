import json
import subprocess  # nosec B404 B603
import sys
import traceback
from pathlib import Path
from urllib.request import urlopen


def bump_release(github_project, tool_name):
    try:
        with urlopen(f"https://api.github.com/repos/{github_project}/releases/latest") as request:  # nosec: disable=B310
            latest_version = json.load(request)["name"].lstrip("v")
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
        try:
            subprocess.check_call(args=args, stdout=subprocess.PIPE)  # nosec: disable=B603
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {args}\nstdout: {e.stdout}\nstderr: {e.stderr}", file=sys.stderr)
            raise

    call("pre-commit", "run", "--file", str(tool_name_version_path.absolute()))
    call("git", "add", str(tool_name_version_path.absolute()))
    call("git", "commit", "-m", message)

    return True


def bump_ktfmt():
    return bump_release(
        github_project="facebook/ktfmt",
        tool_name="ktfmt",
    )


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
    for bumper in (bump_ktfmt, bump_ktlint, bump_google_java_formatter):
        something_is_bumped |= bumper()

    if not something_is_bumped:
        print("No tool need to be bumped")
