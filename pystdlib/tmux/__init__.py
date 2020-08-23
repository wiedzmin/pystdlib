import os
import subprocess

from libtmux import Server
from libtmux.exc import LibTmuxException

from pystdlib import shell_cmd


tmux_server = Server()


def create_window(cmd, session_name, window_title, create_if_not=True, attach=True):
    window = None
    try:
        session = tmux_server.find_where({ "session_name": session_name })
        if not session and create_if_not:
            tmuxp_load_session(session_name, attach=attach)
            session = tmux_server.find_where({ "session_name": session_name })
        else:
            return None

        if attach:
            session.switch_client()
        window = session.new_window(attach=attach, window_name=window_title,
                                    window_shell=cmd)
    except LibTmuxException:
        return None

    return window


def tmuxp_load_session(name, attach=True, sessions_root=f'{os.getenv("HOME")}/tmuxp'):
    load_session_task = subprocess.Popen(f"tmuxp load -y {'-d ' if not attach else ''}{sessions_root}/{name}.yml",
                                         # TODO: decouple from file format
                                         shell=True, stdout=subprocess.PIPE)
    result = load_session_task.wait()
    if result != 0:
        raise LibTmuxException


def tmuxp_collect_sessions(sessions_root=f'{os.getenv("HOME")}/tmuxp'):
    configs = []
    for root, dirs, files in os.walk(TMUXP_SESSIONS_PATH):
        for file in files:
            if file.endswith(".yml"): # TODO: decouple from file format
                configs.append(os.path.splitext(file)[0])

    return configs


def tmux_cmd(cmd, oneshot=False):
    shell_cmd(cmd, oneshot=oneshot, exc=LibTmuxException)
