# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""
import logging
import logging.config
import os

import click

import swytcher.swytcher as swytcher


@click.command()
def main(args=None):
    """Console script for swytcher"""
    click.echo("Replace this message by putting your code into "
               "swytcher.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    print(args or "NO ARGS GIVEN")
    # Setup logging
    logfile = "{}{}{}".format(
        os.path.dirname(__file__), os.path.sep, 'log_conf.ini')
    logging.config.fileConfig(logfile, disable_existing_loggers=False)

    swytcher.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
