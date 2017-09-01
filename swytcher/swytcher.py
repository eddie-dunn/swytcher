"""Automatic keyboard layout switcher"""
import functools
import logging
import subprocess
from typing import Iterable
from typing import Set

import xkbgroup

import swytcher.settings as settings
import swytcher.xwindow as xwindow
from swytcher.util import suppress_err

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


# Move this to swytcher.system
@suppress_err(FileNotFoundError, log)
def notify(title: str, msg: str = '') -> None:  # pragma: no cover
    """Use notify-send (if available) to inform user of layout switch."""
    if not settings.NOTIFY:
        return
    cmd = [
        'notify-send',
        '--urgency=low',
        '--expire-time=2000',
        title,
        msg
    ]
    subprocess.call(cmd)


def change_layout(xkb: xkbgroup.XKeyboard, layout: str) -> bool:
    """Set layout; returns True if layout was changed, False otherwise"""
    if xkb.group_name == layout:  # check against current layout
        log.debug("%r is already the active layout", layout)
        return False  # don't change layout if it's already correct
    log.info("setting layout %r", layout)
    xkb.group_name = layout
    notify("Changed layout", layout)
    return True


def _match_substrings(name_list: Iterable[str],
                      substrings: Iterable[str]) -> set:
    """Substring filter match"""
    found_matches = set()
    for name in name_list:
        for substring in substrings:
            if substring in name:
                log.debug("Substring filter match: %r in %r", substring, name)
                found_matches.update([name])

    return found_matches


def matches(name_list: Iterable[str], strings: Iterable[str],
            substrings: Iterable[str]) -> Set[str]:
    """Returns True if any of the strings in the two filters `strings` and
    `substrings` occur in `name_list`."""
    matched = (set(strings) & set(name_list) or
               _match_substrings(name_list, substrings or {}))
    if matched:
        log.debug('%r matched %r from %r or %r',
                  name_list, matched, strings, substrings)
    return matched


def change_callback(name_list, xkb, layouts: list) -> None:  # pragma: no cover
    """Event handler when active window is changed"""
    # NOTE: These extracted variables should be removed later
    primary_filter = layouts[0]['strings']
    primary_substrings = layouts[0]['substrings']
    primary = layouts[0]['name']
    secondary_filter = layouts[1]['strings']
    secondary_substrings = layouts[1]['substrings']
    secondary = layouts[1]['name']

    # matched_layout = match_layout(name_list, layouts)
    # if matched_layout:
    #   change_layout(xkb, matched_layout)
    # else:
    #   change_layout(xkb, last_remembered_layout_for_window)

    if matches(name_list, secondary_filter, secondary_substrings):
        change_layout(xkb, secondary)
    elif matches(name_list, primary_filter, primary_substrings):
        change_layout(xkb, primary)
    else:
        log.debug("%r: No match, using default layout", name_list)
        change_layout(xkb, xkb.groups_names[0])


def main(args=None):  # pragma: no cover
    """Main"""
    if not args:
        pass
    xkb = xkbgroup.XKeyboard()
    layouts = settings.setup_layouts(xkb, settings.CONFIG_INI)
    log.info("Layouts configured by setxkbmap: %s", layouts)
    partial_cb = functools.partial(change_callback, xkb=xkb, layouts=layouts)
    xwindow.run(partial_cb)
