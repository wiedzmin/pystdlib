import subprocess

from pystdlib import shell_cmd
from pystdlib.shell import tmux_create_window, term_create_window


def list_units(system=True, user=True):
    units = []
    if user:
        result = shell_cmd("systemctl --user list-unit-files")
        units.extend([f"{unit.split()[0]} [user]"
                      for unit in result.split("\n")[1:-3]
                      if unit.split()[0].endswith(("service", "timer"))])
    if system:
        result = shell_cmd("systemctl list-unit-files")
        units.extend([f"{unit.split()[0]} [system]"
                      for unit in result.split("\n")[1:-3]
                      if unit.split()[0].endswith(("service", "timer"))])

    return units


def unit_perform(unit, op, user=False):
    cmd = f"systemctl {'--user ' if user else ''}{op} {unit.split()[0]}"
    return shell_cmd(cmd)


def unit_show(unit, op, user=False,
              shell=None, # virtual terminal command in form like `alacritty -e`
              tmux_session=None # tmux session name, will not be created it does not exist
              ):
    if op not in ["status", "journal", "show"]:
        raise ValueError("[unit_show] invalid operation: {op}")

    cmd = None
    if op in ["status", "show"]:
        cmd = f"systemctl {'--user ' if user else ''}{op} {unit.split()[0]}; read"
    elif op == "journal":
        cmd = f"journalctl {'--user ' if user else ''}-u {unit.split()[0]}; read"

    title = f"{op} :: {unit}"
    if shell:
        if tmux_session:
            tmux_create_window(f"sh -c '{cmd}'",
                               session_name=tmux_session,
                               window_title=title,
                               create_if_not=False,
                               attach=True)
        else:
            term_create_window(f"sh -c '{cmd}'", term_cmd=shell)
    else:
        show_text_dialog(cmd=cmd, title=title)


def is_systemd_service_active(name, user=False):
    status_task = subprocess.Popen(f"systemctl {'--user ' if user else ''}status --no-page {name}.service", shell=True,
                                   stdout=subprocess.PIPE)
    result = status_task.wait()
    print(result)
    if result in [0, 3]:
        lines = status_task.stdout.read().decode().split("\n")
        print(lines)
        if "running" in lines[2]:
            return True
        return False
    else:
        return False
