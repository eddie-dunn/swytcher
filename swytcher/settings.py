"""Settings module"""
import configparser
import logging
import os


# Move these to config.ini
SECONDARY_FILTER = (
    "Msgcompose",  # Icedove window class when writing email
    "Pidgin",
)
SECONDARY_SUBSTRINGS = (
    "Outlook Web App",
    "Google Hangouts",
    "Chromium",
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


def setup_layouts(xkb):
    """Setup layout settings"""
    config = get_config()

    global NOTIFY
    NOTIFY = config['logging'].getboolean('notify')
    # NOTE: implement support for setting loglevel from config someday

    layout_sections = [
        (name, section) for name, section in config.items()
        if name.startswith('layout')
    ]

    layouts = []
    for i, (name, section) in enumerate(layout_sections):
        log.info("Config section %r used for %r", name, xkb.groups_names[i])
        layouts.append({
            'name': xkb.groups_names[i],
            'strings': section['strings'].split(),
            'substrings': section['substrings'].split(),
        })

    return layouts


def get_config():
    config = configparser.ConfigParser()
    filenames = [os.path.expanduser('~/.config/swytcher/config.ini')]
    if not config.read(filenames):
        raise FileNotFoundError("No config file found in %r" % filenames)
    return config
