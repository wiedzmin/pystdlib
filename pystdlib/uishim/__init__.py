import os
import sys

import dmenu
import notify2
from notify2 import URGENCY_NORMAL, URGENCY_CRITICAL
from pyfzf.pyfzf import FzfPrompt

from pystdlib import shell_cmd

notify2.init(os.path.basename(__file__))
is_interactive = sys.stdin.isatty()
in_xsession = os.environ.get("DISPLAY")


def notify(msg, header, urgency=URGENCY_NORMAL, timeout=3000):
    n = notify2.Notification(header, msg)
    n.set_urgency(urgency)
    n.set_timeout(timeout)
    n.show()


def do_log(msg, header, urgency, timeout):
    if in_xsession:
        notify(msg, header, urgency, timeout)
    else:
        print(f"{header} {msg}")


def log_info(msg, header="[INFO]", urgency=URGENCY_NORMAL, timeout=3000):
    do_log(msg, header, urgency, timeout)


def log_error(msg, header="[ERROR]", urgency=URGENCY_CRITICAL, timeout=3000):
    do_log(msg, header, urgency, timeout)


def get_selection(seq, prompt, lines=5, case_insensitive=True, font=None):
    if in_xsession:
        return dmenu.show(seq, prompt=prompt, lines=lines,
                          case_insensitive=case_insensitive, font=font)
    else:
        fzf = FzfPrompt()
        return fzf.prompt(seq, '--cycle')[0]


def show_text_dialog(text=None, cmd=None, title=None):
    if not text and not cmd:
        raise ValueError("[show_text_dialog] nothing to display")

    output = None
    if cmd:
        output = shell_cmd(cmd)
        if not output:
            raise ValueError("[show_text_dialog] '{cmd}' returned nothin")
    elif text:
        output = text

    with open("/tmp/dialog_text", "w") as f:
        f.write(output)
    shell_cmd("yad --filename /tmp/iface_traits {'--title {title} ' if title else ''}--text-info")
    os.remove("/tmp/dialog_text")
