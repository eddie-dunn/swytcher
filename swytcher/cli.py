# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""
import click

import swytcher.settings as settings
import swytcher.swytcher as swytcher


@click.command()
def main(args=None):
    """Console script for swytcher"""
    # click.echo("See click documentation at http://click.pocoo.org/")
    click.echo(__name__)
    settings.load_configs()  # pylint: disable=protected-access

    swytcher.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
