# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil
import subprocess
import sys

import requests
from six.moves.urllib.parse import urlparse


def run_command(command):
    print('[cwd={cwd}] Run command: {command}'.format(command=command, cwd=os.getcwd()), file=sys.stderr)
    return_code, output = None, None
    try:
        return_code, output = 0, subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return_code, output = e.returncode, e.output.decode('utf-8')
    print('[return_code={return_code}] | {output}'.format(return_code=return_code, output=output), file=sys.stderr)
    return return_code, output


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


def get_modified_files_in_repo():
    _, command_output = run_command(
        'git diff-index --name-status --binary --exit-code --no-ext-diff $(git write-tree) --',
    )
    return {
        line.split()[-1]
        for line in command_output.splitlines()
        if line
    }
