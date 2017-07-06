"""Settings module"""
import configparser
import logging
import logging.config
import os
import shutil


CONFIG_INI = None
NOTIFY = None

NOTIFY = True
PATH_TEMPLATES = (
    '{home}/.config/swytcher/{filename}',
    # '{home}/.local/swytcher/config/{filename}',
)


log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _setup_logging(config) -> None:
    # Setup logging
    log_conf = 'log_conf.ini'
    logfile = get_config(log_conf)

    if not logfile:
        logfile = conf_not_found(log_conf)

    logging.config.fileConfig(logfile, disable_existing_loggers=False)

    # Optionally override logging from config.ini
    loglevel = config['logging'].get('loglevel')
    if loglevel:
        logging.getLogger().setLevel(logging.getLevelName(loglevel))
        print("Loglevel %r set!" % loglevel)


def _get_configparser() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config_ini = 'config.ini'
    config_file = get_config(config_ini)
    if not config_file:
        config_file = conf_not_found(
            config_ini, log_msg=True, config_paths=conf_paths(config_ini))
        config_file = shutil.copy(config_file, conf_paths(config_ini)[0])

    config.read(config_file)
    if not config:
        raise FileNotFoundError("{} not found".format(config_ini))
    return config


def _setup_config(config: configparser.ConfigParser) -> None:
    # Setup globals from config.ini
    global CONFIG_INI  # pylint: disable=global-statement
    CONFIG_INI = config

    global NOTIFY  # pylint: disable=global-statement
    NOTIFY = config['logging'].getboolean('notify')


def load_configs() -> None:
    """Load configs"""
    config = _get_configparser()
    _setup_config(config)
    _setup_logging(config)


def setup_layouts(xkb, config):
    """Setup layout settings"""
    if not config:
        raise AssertionError("Config file must be loaded first")

    layout_sections = [
        (name, section) for name, section in config.items()
        if name.startswith('layout')
    ]

    layouts = []
    for i, (name, section) in enumerate(layout_sections):
        log.info("Config section %r used for %r", name, xkb.groups_names[i])
        layouts.append({
            'name': xkb.groups_names[i],
            'strings': section['strings'].strip().splitlines(),
            'substrings': section['substrings'].strip().splitlines(),
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


def conf_not_found(
        filename: str, log_msg: bool=False, config_paths: list=None) -> str:
    """Log warning that config file was not found, return path to default
    conf"""
    default_conf = "%s%s%s" % (os.path.dirname(__file__), os.path.sep,
                               filename)

    if log_msg:
        log.warning(
            "Config file %r not found%s; using default %r",
            filename,
            " in %s" % ' or '.join(config_paths) if config_paths else "",
            default_conf)
    return default_conf
