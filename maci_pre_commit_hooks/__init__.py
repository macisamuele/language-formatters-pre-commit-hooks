import subprocess


def run_command(command):
    try:
        return 0, subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        ).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output.decode('utf-8')
