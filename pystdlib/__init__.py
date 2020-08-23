import subprocess


def shell_cmd(cmd, oneshot=False, env=None, exc=subprocess.CalledProcessError, split_output=None):
    result = None
    if oneshot:
        os.system(cmd)
        return ""
    task = subprocess.Popen(cmd, env=env, shell=True, stdout=subprocess.PIPE)
    ret = task.wait()
    if ret != 0:
        raise exc()

    contents = task.stdout.read().decode().strip()
    if split_output:
        contents = contents.split(split_output)
    return contents
