import Xlib.protocol.event
from Xlib import X, display, error, Xatom, Xutil

from pystdlib import shell_cmd


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
