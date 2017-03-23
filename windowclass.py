#!/usr/bin/env python
"""Get active window name and class.

Inspiration taken from http://unix.stackexchange.com/a/334293/138633
"""
import logging

import Xlib
import Xlib.display

from util import exception_handler

DISP = Xlib.display.Display()
ROOT = DISP.screen().root

NET_ACTIVE_WINDOW = DISP.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = DISP.intern_atom('_NET_WM_NAME')  # UTF-8
WM_NAME = DISP.intern_atom('WM_NAME')  # Legacy encoding

log = logging.getLogger(__name__)  # pylint: disable=invalid-name
log.level = logging.INFO


def get_window_name(window: Xlib.xobject.drawable.Window) -> str:
    """Get window name"""
    name = window.get_wm_name()
    if not name:
        for atom in (NET_WM_NAME, WM_NAME):
            name = window.get_full_property(atom, 0).value.decode('utf8')

    log.debug("Found window name %r", name)
    return name


@exception_handler(Exception, log, logging.ERROR, traceback=True)
@exception_handler(Xlib.error.BadWindow)  # ignore BadWindow
def handle_xevent(event, callback):
    """Handle xevent"""
    if event.type != Xlib.X.PropertyNotify:
        return

    if event.atom != NET_ACTIVE_WINDOW:
        return

    win_id = ROOT.get_full_property(NET_ACTIVE_WINDOW,
                                    Xlib.X.AnyPropertyType).value[0]

    window = DISP.create_resource_object('window', win_id)
    wmclass = window.get_wm_class()
    wmname = get_window_name(window)
    callback(name_list=[*wmclass, wmname])


def example_handler(name_list: list):
    """Example of a callback handler for when a window change occurs.

    This one just prints the list of strings that were found in handle_xevent.
    """
    print(name_list)


def run(callback):
    """Runner for getting X window events.

    The callback function will be invoked with a list containing the classnames
    and window titles as a `name_list` keyword argument. If you need pass more
    parameters to the callback, use functools.partial to partially construct
    the callback function.
    """
    ROOT.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
    while True:  # next_event() sleeps until we get an event
        handle_xevent(DISP.next_event(), callback)


if __name__ == '__main__':
    # main()
    run(callback=example_handler)
