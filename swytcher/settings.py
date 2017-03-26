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
    print(os.path.dirname(__file__))
    filenames = [os.path.expanduser('~/.config/swytcher/config.ini')]
    if not config.read(filenames):
        default_conf = "%s%s%s" % (os.path.dirname(__file__), os.path.sep,
                                   'config.ini')
        print("No config file found in %r, using default config %r" %
              (filenames, default_conf))
        config.read(default_conf)

    return config
