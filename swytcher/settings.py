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
    # '/tmp/{home}/.config/swytcher/{filename}',
    '{home}/.config/swytcher/{filename}',
    # '{home}/.local/swytcher/config/{filename}',
)


log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _setup_logging(config: configparser.ConfigParser) -> None:
    # Setup logging
    log_conf = 'log_conf.ini'
    logfile = get_config(log_conf)

    if not logfile:  # pragma: no cover; how to mock a configparser object?
        logfile = default_conf_name(log_conf)

    logging.config.fileConfig(logfile, disable_existing_loggers=False)

    # Optionally override logging from config.ini
    loglevel = config['logging'].get('loglevel')
    if loglevel:
        logger = logging.getLogger()
        logger.setLevel(logging.getLevelName(loglevel))  # type: ignore
        log.info("Loglevel %r set!", loglevel)


def copy_config(conf_name: str) -> str:
    """Copies default config to user's config dir. Returns copied filename"""
    config_file = default_conf_name(conf_name)
    cp_conf_path = conf_paths(conf_name)[0]
    log.info("Copying default conf from %r to %r", config_file, cp_conf_path)
    os.makedirs(os.path.dirname(cp_conf_path), exist_ok=True)
    if os.path.isfile(cp_conf_path):
        # TODO: return a Result object instead of raising errors
        raise FileExistsError(cp_conf_path)
    config_file = shutil.copy(config_file, cp_conf_path)
    return config_file


def _get_configparser() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config_ini = 'config.ini'
    config_file = get_config(config_ini)
    log.info("Using config found in %r", config_file)
    config.read(config_file)
    if not config:
        raise FileNotFoundError("{} not found".format(config_ini))
    return config


def _setup_config(config: configparser.ConfigParser) -> None:
    # Setup globals from config.ini
    global CONFIG_INI  # pylint: disable=global-statement
    CONFIG_INI = config

    global NOTIFY  # pylint: disable=global-statement
    NOTIFY = config['logging'].getboolean('notify')  # type: ignore


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


def default_conf_name(
        filename: str, log_msg: bool = False,
        config_paths: list = None) -> str:
    """Log warning that config file was not found, return path to default
    conf"""
    default_conf_path = "%s%s%s" % (os.path.dirname(__file__), os.path.sep,
                                    filename)

    if log_msg:
        log.warning(
            "Config file %r not found%s; using default %r",
            filename,
            " in %s" % ' or '.join(config_paths) if config_paths else "",
            default_conf_path)
    return default_conf_path
