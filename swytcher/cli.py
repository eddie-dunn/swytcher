# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""
import logging
import logging.config

import click

import swytcher.settings as settings
import swytcher.swytcher as swytcher


@click.command()
def main(args=None):
    """Console script for swytcher"""
    # click.echo("See click documentation at http://click.pocoo.org/")
    click.echo(__name__)
    # Setup logging
    log_conf = 'log_conf.ini'
    logfile = settings.get_config(log_conf)

    if not logfile:
        logfile = settings.conf_not_found(
            log_conf, settings.conf_paths(log_conf))

    logging.config.fileConfig(logfile, disable_existing_loggers=False)

    swytcher.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
