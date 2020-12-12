import argparse
import glob
import os
import time

from pystdlib.uishim import get_selection
from pystdlib import shell_cmd


def collect_sessions(path):
    return [f"{os.path.basename(session)}" for session in glob.glob(f"{path}/*.org")]


def collect_sessions_with_size(path):
    return [f"{os.path.basename(session)} ({collect_session_urls(path, os.path.basename(session))[1]})"
            for session in glob.glob(f"{path}/*.org")]


def collect_session_urls(path, name):
    urls = None
    with open(f"{path}/{name}", "r") as session:
        urls = [url.strip()[2:] for url in session.readlines() if url.startswith("* http")]
    return urls, len(urls)


def init_argparser():
    parser = argparse.ArgumentParser(description="Manage stored browser sessions.")
    parser.add_argument("--path", "-p", dest="sessions_path",
                        help="Base path to operate under")
    parser.add_argument("--size-threshold", "-s", dest="session_size_threshold",
                        default=10, help="Maximum session size to be opened in browser")
    parser.add_argument("--history-length", "-l", dest="sessions_history_length",
                        default=10, help="Last saved sessions count to keep")
    parser.add_argument("--name-template", "-n", dest="sessions_name_template",
                        default="firefox-session-auto", help="Filename template for auto-saved sessions")
    parser.add_argument("--save", dest="save_session", action="store_true",
                        default=False, help="Save current session")
    parser.add_argument("--open", dest="open_session", action="store_true",
                        default=False, help="Open stored session")
    parser.add_argument("--edit", dest="edit_session", action="store_true",
                        default=False, help="Edit stored session")
    parser.add_argument("--delete", dest="delete_session", action="store_true",
                        default=False, help="Delete stored session")
    parser.add_argument("--rotate", dest="rotate_sessions", action="store_true",
                        default=False, help="Rotate auto-saved sessions")
    return parser


def open_urls_firefox(urls):
    if not urls or len(urls) == 0:
        raise ValueError("invalid urls provided")
    shell_cmd(f"firefox --new-window {urls[0]}")
    time.sleep(0.5)
    urls_remainder = " --new-tab ".join(urls[1:])
    if len(urls_remainder):
        shell_cmd(f"firefox --new-tab {urls_remainder}")


def rotate_sessions(path, name_template, keep_count):
    garbage_sessions = sorted([session for session in glob.glob(f"{path}/*{name_template}*")])[keep_count:]
    for s in garbage_sessions:
        os.remove(s)
