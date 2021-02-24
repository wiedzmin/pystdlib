import os
import subprocess

from libtmux import Server
from libtmux.exc import LibTmuxException

from pystdlib import shell_cmd


tmux_server = Server()


def term_create_window(cmd, term_cmd=None):
    if type(term_cmd) not in [list, str]:
        raise ValueError(f"invalid `term_cmd` type: {type(term_cmd)}")
    if type(term_cmd) is str:
        term_cmd = term_cmd.split()
    if len(cmd) > 0:
        term_cmd.extend(cmd.split(" "))
        shell_cmd(" ".join(term_cmd))


def tmux_create_window(cmd, session_name, window_title, create_if_not=True, attach=True, attach_window=True,
                       start_directory=None):
    window = None
    try:
        session = tmux_server.find_where({ "session_name": session_name })
        if not session and create_if_not:
            tmuxp_load_session(session_name, attach=attach)
            session = tmux_server.find_where({ "session_name": session_name })
        if attach:
            session.switch_client()
        window = session.new_window(attach=attach_window, window_name=window_title,
                                    window_shell=cmd, start_directory=start_directory)
    except LibTmuxException:
        return None
    return window


def tmuxp_load_session(name, attach=True, sessions_root=f'{os.getenv("HOME")}/.tmuxp'):
    load_session_task = subprocess.Popen(f"tmuxp load -y {'-d ' if not attach else ''}{sessions_root}/{name}.yml",
                                         # TODO: decouple from file format
                                         shell=True, stdout=subprocess.PIPE)
    result = load_session_task.wait()
    if result != 0:
        raise LibTmuxException


def tmuxp_collect_sessions(sessions_root=f'{os.getenv("HOME")}/.tmuxp'):
    configs = []
    for root, dirs, files in os.walk(sessions_root):
        for file in files:
            if file.endswith(".yml"): # TODO: decouple from file format
                configs.append(os.path.splitext(file)[0])

    return configs
