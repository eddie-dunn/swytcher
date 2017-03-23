# -*- coding: utf-8 -*-
"""CLI frontend for Swytcher"""

import click

import swytcher.swytcher as swytcher


@click.command()
def main(args=None):
    """Console script for swytcher"""
    click.echo("Replace this message by putting your code into "
               "swytcher.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    print(args or "NO ARGS GIVEN")
    swytcher.main()


if __name__ == "__main__":
    main()
