"""Settings module"""
import logging
import os
import configparser


LOGLEVEL = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO
NOTIFY = True
PATH_TEMPLATES = (
    '{home}/.config/swytcher/{filename}',
    '{home}/.local/swytcher/config/{filename}',
)


logging.basicConfig(level=LOGLEVEL)
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def setup_layouts(xkb):
    """Setup layout settings"""
    # config = get_configini('config.ini')
    config = configparser.ConfigParser()
    filename = 'config.ini'
    config_file = get_config(filename)
    if not config_file:
        config_file = conf_not_found(filename, conf_paths(filename))

    config.read(config_file)

    global NOTIFY  # pylint: disable=global-statement
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


def conf_paths(filename) -> list:
    """Get config paths"""
    home = os.path.expanduser('~')
    paths = [path.format(home=home, filename=filename) for path in
             PATH_TEMPLATES]
    return paths


def get_config(filename: str) -> str:
    """Try to find user configured logfile"""
    config_file = ''
    for path in conf_paths(filename):
        if os.path.isfile(path):
            config_file = path
            break
    return config_file


def conf_not_found(filename: str, config_paths: list) -> str:
    """Log warning that config file was not found, return path to default
    conf"""
    default_conf = "%s%s%s" % (os.path.dirname(__file__), os.path.sep,
                               filename)
    log.warning("Config file %r not found in %r, using default %r", filename,
                config_paths, default_conf)
    return default_conf
