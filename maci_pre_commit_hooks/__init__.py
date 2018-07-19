import os
import shutil
import subprocess

import requests
from six.moves.urllib.parse import urlparse


def run_command(command):
    try:
        return 0, subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode('utf-8')


def _base_directory():
    # Extracted from pre-commit code:
    # https://github.com/pre-commit/pre-commit/blob/master/pre_commit/store.py
    return os.environ.get('PRE_COMMIT_HOME') or os.path.join(
        os.environ.get('XDG_CACHE_HOME') or os.path.expanduser('~/.cache'),
        'pre-commit',
    )


def download_url(url, file_name=None):
    final_file = os.path.join(
        _base_directory(),
        file_name or os.path.basename(urlparse(url).path),
    )

    if os.path.exists(final_file):
        return final_file

    r = requests.get(url, stream=True)
    tmp_file = '{}_tmp'.format(final_file)
    with open(tmp_file, mode='wb') as f:
        # Copy on a temporary file in case of issues while downloading the file
        shutil.copyfileobj(r.raw, f)

    os.rename(tmp_file, final_file)
    return final_file
