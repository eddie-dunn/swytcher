# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""
import logging

import click

import swytcher.settings as settings
import swytcher.swytcher as swytcher
from swytcher import __version__

log = logging.getLogger(__name__)  # pylint: disable=invalid-name
logging.basicConfig(level=logging.INFO)


def cpcfg(ctx, _param, value):
    """Copy config, then exit"""
    if not value or ctx.resilient_parsing:
        return
    # TODO: Add functionality to copy config here
    click.echo("Sample config copied to {!r}".format('destination'))
    ctx.exit()


@click.command()
@click.option('--cpcfg', is_flag=True, help='copy sample config to ~/.config',
              expose_value=False, is_eager=True, callback=cpcfg)
@click.version_option(__version__)
def main(args=None):
    """Console script for swytcher"""
    # click.echo("See click documentation at http://click.pocoo.org/")
    click.echo(__name__)
    settings.load_configs()  # pylint: disable=protected-access

    swytcher.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
