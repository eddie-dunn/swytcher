#!/usr/bin/env python
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
from contextlib import contextmanager
import logging
import Xlib
import Xlib.display

disp = Xlib.display.Display()
root = disp.screen().root

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')  # UTF-8
WM_NAME = disp.intern_atom('WM_NAME')           # Legacy encoding
WM_CLASS = disp.intern_atom('_NET_WM_CLASS')

last_seen = {'xid': None, 'title': None}

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@contextmanager
def window_obj(win_id):
    """Simplify dealing with BadWindow (make it either valid or None)"""
    window_obj_ = None
    if win_id:
        try:
            window_obj_ = disp.create_resource_object('window', win_id)
        except Xlib.error.XError:
            pass
    yield window_obj_


def get_active_window():
    win_id = root.get_full_property(NET_ACTIVE_WINDOW,
                                    Xlib.X.AnyPropertyType).value[0]

    focus_changed = (win_id != last_seen['xid'])
    if focus_changed:
        with window_obj(last_seen['xid']) as old_win:
            if old_win:
                log.debug("old_win")
                old_win.change_attributes(event_mask=Xlib.X.NoEventMask)

        last_seen['xid'] = win_id
        with window_obj(win_id) as new_win:
            if new_win:
                log.debug("new_win")
                new_win.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

    return win_id, focus_changed


def _get_window_name_inner(win_obj):
    """Simplify dealing with _NET_WM_NAME (UTF-8) vs. WM_NAME (legacy)"""
    for atom in (NET_WM_NAME, WM_NAME, WM_CLASS):
        print(win_obj.get_wm_class())
        print(win_obj.get_wm_name())
        try:
            window_name = win_obj.get_full_property(atom, 0)
            print(window_name.value)
        except UnicodeDecodeError:  # Apparently a Debian distro package bug
            title = "<could not decode characters>"
        else:
            if window_name:
                win_name = window_name.value
                if isinstance(win_name, bytes):
                    # Apparently COMPOUND_TEXT is so arcane that this is how
                    # tools like xprop deal with receiving it these days
                    win_name = win_name.decode('latin1', 'replace')
                return win_name
            else:
                title = "<unnamed window>"

    return "{} (XID: {})".format(title, win_obj.id)


def get_window_name(win_id):
    if not win_id:
        last_seen['title'] = "<no window id>"
        return last_seen['title']

    title_changed = False
    with window_obj(win_id) as wobj:
        if wobj:
            win_title = _get_window_name_inner(wobj)
            title_changed = (win_title != last_seen['title'])
            last_seen['title'] = win_title

    return last_seen['title'], title_changed


def handle_xevent(event):
    if event.type != Xlib.X.PropertyNotify:
        return

    changed = False
    if event.atom == NET_ACTIVE_WINDOW:
        log.debug("NET_ACTIVE_WINDOW")
        if get_active_window()[1]:
            changed = changed or get_window_name(last_seen['xid'])[1]
    elif event.atom in (NET_WM_NAME, WM_NAME, WM_CLASS):
        log.debug("event.atom in ...")
        changed = changed or get_window_name(last_seen['xid'])[1]

    if changed:
        handle_change(last_seen)


def handle_change(new_state):
    """Replace this with whatever you want to actually do"""
    print(new_state)


if __name__ == '__main__':
    root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

    get_window_name(get_active_window()[0])
    handle_change(last_seen)

    while True:  # next_event() sleeps until we get an event
        handle_xevent(disp.next_event())
