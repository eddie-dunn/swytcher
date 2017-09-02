# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""
import logging

import click

import swytcher.settings as settings
import swytcher.swytcher as swytcher
from swytcher import __version__

log = logging.getLogger(__name__)  # pylint: disable=invalid-name
logging.basicConfig(level=logging.INFO)


@click.command()
@click.version_option(__version__)
def main(args=None):
    """Console script for swytcher"""
    # click.echo("See click documentation at http://click.pocoo.org/")
    click.echo(__name__)
    settings.load_configs()  # pylint: disable=protected-access

    swytcher.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
