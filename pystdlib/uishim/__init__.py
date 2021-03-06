import os
import sys

import dmenu
import notify2
from notify2 import URGENCY_NORMAL, URGENCY_CRITICAL
from pyfzf.pyfzf import FzfPrompt
from rofi import Rofi

from pystdlib import shell_cmd


URGENCY_NORMAL = notify2.URGENCY_NORMAL
URGENCY_CRITICAL = notify2.URGENCY_CRITICAL


notify2.init(os.path.basename(__file__))
is_interactive = sys.stdin.isatty()
in_xsession = os.environ.get("DISPLAY")

ro = Rofi()


def notify(header, msg, urgency=URGENCY_NORMAL, timeout=3000):
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


def get_selection_rofi(seq, prompt):
    seq = list(seq)
    index, _ = ro.select(prompt, seq)
    if index:
        return seq[index[0]]
    return None


def show_text_dialog(text=None, cmd=None, title=None, path=None, keep=False):
    if not text and not cmd:
        raise ValueError("[show_text_dialog] nothing to display")

    output = None
    if cmd:
        output = shell_cmd(cmd)
        if not output:
            raise ValueError("[show_text_dialog] '{cmd}' returned nothing")
    elif text:
        output = text

    dump_path = path if path else "/tmp/dialog_text"
    if not os.path.exists(dump_path):
        with open(dump_path, "w") as f:
            if type(output) is list:
                f.write("\n".join(output))
            else:
                f.write(output)
    shell_cmd(f"yad --filename {dump_path} {'--title {title} ' if title else ''}--text-info",
              ignore_error_codes=[252])
    if not keep:
        os.remove(dump_path)
