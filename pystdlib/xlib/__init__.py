import os

import Xlib.protocol.event
from Xlib import X, display, error, Xatom, Xutil

from pystdlib import shell_cmd


d = display.Display()
root = d.screen().root
_NET_ACTIVE_WINDOW = d.intern_atom("_NET_ACTIVE_WINDOW")
_NET_WM_NAME = d.intern_atom("_NET_WM_NAME")


def prepare_desktops_map():
    desktops = shell_cmd("wmctrl -d", split_output="\n")
    return { desktop[-1]: desktop[0] for desktop in [desktop.split() for desktop in desktops]}


def sendEvent(win, ctype, data, mask=None):
    data = (data+[0]*(5-len(data)))[:5]
    ev = Xlib.protocol.event.ClientMessage(window=win, client_type=ctype, data=(32,(data)))

    if not mask:
        mask = (X.SubstructureRedirectMask|X.SubstructureNotifyMask)
    win.send_event(ev, event_mask=mask)


def switch_desktop(index):
    display = Xlib.display.Display()
    sendEvent(display.screen().root, display.intern_atom("_NET_CURRENT_DESKTOP"),
              [index, X.CurrentTime])
    display.flush()


def switch_named_desktop(name):
    index = prepare_desktops_map()[name] # TODO: add more safety harness
    switch_desktop(int(index))


def is_idle_enough(xprintidle_binary, idle_time_treshold=3600):
    idle_time = shell_cmd(xprintidle_binary, env={"DISPLAY": os.getenv("DISPLAY"),
                                                  "XAUTHORITY": os.getenv("XAUTHORITY")})
    return int(idle_time) >= idle_time_treshold * 1000


def get_active_window_traits():
    active_window = root.get_full_property(_NET_ACTIVE_WINDOW, X.AnyPropertyType).value.pop()
    active_window_name = None
    active_window_class = None
    try:
        active_window_obj = d.create_resource_object("window", active_window)
        active_window_name = active_window_obj.get_full_property(_NET_WM_NAME, X.AnyPropertyType).value.decode("ascii")
        active_window_class = active_window_obj.get_wm_class()[0] or ""
    except XError:
        pass
    return active_window_name, active_window_class
