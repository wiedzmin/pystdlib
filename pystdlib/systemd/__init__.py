import subprocess

from pystdlib import shell_cmd


def sctl_list_units(system=True, user=True):
    units = []
    if user:
        result = shell_cmd("systemctl --user list-unit-files")
        units.extend([f"{unit.split()[0].split('.')[0]} [user]"
                      for unit in result.split("\n")[1:-3]
                      if unit.split()[0].endswith("service")])
    if system:
        result = shell_cmd("systemctl list-unit-files")
        units.extend([f"{unit.split()[0].split('.')[0]} [system]"
                      for unit in result.split("\n")[1:-3]
                      if unit.split()[0].endswith("service")])

    return units
