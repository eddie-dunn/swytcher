"""Settings module"""
import os
import logging


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
    return [
        {
            # Primary
            'name': xkb.groups_names[0],
            'strings': PRIMARY_FILTER,
            'substrings': PRIMARY_SUBSTRINGS,
        },
        {
            # Secondary
            'name': xkb.groups_names[1],
            'strings': SECONDARY_FILTER,
            'substrings': SECONDARY_SUBSTRINGS,
        },
    ]
