# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""
import logging
import logging.config
import os

import click

import swytcher.swytcher as swytcher


def get_config(filename: str) -> str:
    """Try to find user configured logfile"""
    # NOTE: Move to settings later
    logfile = ''
    home = os.path.expanduser('~')
    paths = [
        '{}/.config/swytcher/{}'.format(home, filename),
        '{}/.local/swytcher/config/{}'.format(home, filename),
    ]
    for path in paths:
        if os.path.isfile(path):
            logfile = path
            break
    return logfile


@click.command()
def main(args=None):
    """Console script for swytcher"""
    # click.echo("See click documentation at http://click.pocoo.org/")
    click.echo(__name__)
    # Setup logging
    logfile = get_config('log_conf.ini')

    if not logfile:
        logfile = '{}/log_conf.ini'.format(os.path.dirname(__file__))
        print("No log conf file found, using default %r" % logfile)

    logging.config.fileConfig(logfile, disable_existing_loggers=False)

    swytcher.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
