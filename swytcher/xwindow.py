#!/usr/bin/env python
"""Get active window name and class.

Inspiration taken from http://unix.stackexchange.com/a/334293/138633
"""
import logging
from typing import Callable

import Xlib
import Xlib.display

from swytcher.util import suppress_err

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Globals
DISP = None
ROOT = None
NET_ACTIVE_WINDOW = None
NET_WM_NAME = None
WM_NAME = None


def _set_globals():  # pragma: no cover
    """Set global X variables that are used in the module"""
    # NOTE: There should be a better way to do this, other than using globals.
    # pylint: disable=global-statement
    global DISP, ROOT, NET_ACTIVE_WINDOW, NET_WM_NAME, WM_NAME
    DISP = Xlib.display.Display()
    ROOT = DISP.screen().root
    NET_ACTIVE_WINDOW = DISP.intern_atom('_NET_ACTIVE_WINDOW')
    NET_WM_NAME = DISP.intern_atom('_NET_WM_NAME')  # UTF-8
    WM_NAME = DISP.intern_atom('WM_NAME')  # Legacy encoding
    log.debug("global vars set")


def get_window_name(window: Xlib.xobject.drawable.Window) -> str:
    """Get window name"""
    def get_name():
        """Closure"""
        log.debug("get_wm_name empty, trying other methods")
        for atom in (NET_WM_NAME, WM_NAME):
            name = window.get_full_text_property(atom)
            if name:
                return name

    name = window.get_wm_name() or get_name() or ''
    log.debug("Got window name %r", name)
    return name


@suppress_err(Exception, log, logging.ERROR, traceback=True)
@suppress_err(Xlib.error.BadWindow)  # ignore BadWindow
def handle_xevent(event: Xlib.X.PropertyNotify,
                  callback: Callable[..., None]) -> bool:
    """Handle xevent; returns true if an event was handled"""
    if event.type != Xlib.X.PropertyNotify:
        return False

    if event.atom != NET_ACTIVE_WINDOW:
        return False

    win_id = ROOT.get_full_property(NET_ACTIVE_WINDOW,
                                    Xlib.X.AnyPropertyType).value[0]

    window = DISP.create_resource_object('window', win_id)
    wmclass = window.get_wm_class() or tuple()
    wmname = get_window_name(window)
    callback(name_list=[*wmclass, wmname])
    return True


def example_handler(name_list: list):  # pragma: no cover
    """Example of a callback handler for when a window change occurs.

    This one just prints the list of strings that were found in handle_xevent.
    """
    print(name_list)


def run(callback):  # pragma: no cover
    """Runner for getting X window events.

    The callback function will be invoked with a list containing the classnames
    and window titles as a `name_list` keyword argument. If you need pass more
    parameters to the callback, use functools.partial to partially construct
    the callback function.
    """
    _set_globals()
    ROOT.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
    while True:  # next_event() sleeps until we get an event
        handle_xevent(DISP.next_event(), callback)


if __name__ == '__main__':  # pragma: no cover
    run(callback=example_handler)
