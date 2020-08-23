import subprocess


def shell_cmd(cmd, oneshot=False, exc=subprocess.CalledProcessError):
    result = None
    if oneshot:
        os.system(cmd)
        return ""
    task = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ret = task.wait()
    if ret != 0:
        raise exc()

    return task.stdout.read().decode().strip()
