#!/usr/bin/env python
"""Automatic keyboard layout switcher"""
from typing import Iterable
import functools
import logging
import os
import subprocess

import xkbgroup

import windowclass
from util import exception_handler

PRIMARY = "English"  # default primary layout
SECONDARY = "Swedish"  # default secondary layout
LAYOUTS = (PRIMARY, SECONDARY)

SECONDARY_FILTER = (
    "Msgcompose",  # Icedove window class when writing email
    "Pidgin",
)
SECONDARY_SUBSTRINGS = (
    "Outlook Web App",
    "Google Hangouts",
)
PRIMARY_FILTER = (
    "Gnome-terminal",
)
PRIMARY_SUBSTRINGS = (
    "VIM",
    "NVIM",
)
LOGLEVEL = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO
NOTIFY = True

logging.basicConfig(level=LOGLEVEL)
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _setup_layouts(xkb):
    global PRIMARY, SECONDARY, LAYOUTS  # pylint: disable=global-statement
    PRIMARY = xkb.groups_names[0]
    SECONDARY = xkb.groups_names[1]
    LAYOUTS = (PRIMARY, SECONDARY)


@exception_handler(FileNotFoundError, log)
def notify(title: str, msg: str='') -> None:
    """notify-send msg"""
    if not NOTIFY:
        return
    cmd = [
        'notify-send',
        '--urgency=low',
        '--expire-time=2000',
        title,
        msg
    ]
    subprocess.call(cmd)


def set_layout(xkb: xkbgroup.XKeyboard, layout: str) -> bool:
    """Set layout"""
    if xkb.group_name == layout:  # check against current layout
        return False  # don't change layout if it's already correct
    log.info("setting layout %r", layout)
    xkb.group_name = layout
    notify("Changed layout", layout)
    return True


def _match_substrings(name_list: list, substrings: list) -> set:
    """Substring filter match"""
    found_matches = set()
    for name in name_list:
        for substring in substrings:
            if substring in name:
                log.debug("Substring filter match: %r in %r", substring, name)
                found_matches.update([name])

    return found_matches


def matches(name_list: Iterable[str], strings: Iterable[str],
            substrings: Iterable[str]) -> bool:
    """Returns True if any of the strings in the two filters `strings` and
    `substrings` occur in `name_list`."""
    matched = (set(strings) & set(name_list) or
               _match_substrings(name_list, substrings or {}))
    return bool(matched)


def change_callback(name_list, xkb) -> None:
    """Event handler when active window is changed"""
    if matches(name_list, SECONDARY_FILTER, SECONDARY_SUBSTRINGS):
        log.debug("%r matched secondary filters", name_list)
        set_layout(xkb, SECONDARY)
    elif matches(name_list, PRIMARY_FILTER, PRIMARY_SUBSTRINGS):
        log.debug("%r matched primary filters", name_list)
        set_layout(xkb, PRIMARY)
    else:
        log.debug("No match, using default layout")
        set_layout(xkb, xkb.groups_names[0])


def main():
    """Main"""
    xkb = xkbgroup.XKeyboard()
    _setup_layouts(xkb)
    log.info("Layouts configured by setxkbmap: %s", LAYOUTS)
    print("[Primary]\n\tlayout {!r}".format(LAYOUTS[0]))
    print("[Secondary]\n\tlayout: {!r}".format(LAYOUTS[1]))
    partial_cb = functools.partial(change_callback, xkb=xkb)
    windowclass.run(partial_cb)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...\n")
