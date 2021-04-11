import os
import subprocess
import sys


def shell_cmd(cmd, oneshot=False, env=None, shell=True,
              split_output=None, universal_newlines=None, input=None,
              executable=None, stdin=None, stdout=subprocess.PIPE,
              stderr=subprocess.PIPE, exit_error_codes=None, ignore_error_codes=None):
    result = None
    if oneshot:
        os.system(cmd)
        return ""
    completed = subprocess.run(cmd, env=env, shell=shell,
                               stdin=stdin, stdout=stdout, stderr=stderr,
                               executable=executable,
                               universal_newlines=universal_newlines, input=input)

    if completed.returncode != 0:
        if exit_error_codes and completed.returncode in exit_error_codes:
            sys.exit(1)
        elif ignore_error_codes and completed.returncode in ignore_error_codes:
            pass
        else:
            raise ValueError(f"'{cmd}' returned {completed.returncode}")

    if not completed.stdout:
        return ""
    contents = None
    if isinstance(completed.stdout, bytes):
        contents = completed.stdout.decode().strip()
    else:
        contents = completed.stdout.strip()
    if split_output:
        contents = contents.split(split_output)
    return contents
