# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


#
# BEGINNING TO USE CLICK TO DO A LAUNCHER FOR ONTOSPY-VIZ
#

"""
ONTOSPY
Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

Run it from the command line by passing it an ontology URI,
or check out the help:

>>> ontospy-viz -h

More info in the README file.

"""

import sys, os, time, os.path, webbrowser

from . import *  # imports __init__
from ._version import *
# from .actions import *
from .viz.builder import action_visualize
from .core.ontospy import Ontospy

from .core.utils import *

import click


@click.command()
def hello():
    """"http://click.pocoo.org/5/
    http://click.pocoo.org/5/api/
    """
    click.clear()
    click.secho('Hello World!', fg='green')
    click.secho('Some more text', bg='blue', fg='white')
    click.secho('ATTENTION', blink=True, bold=True)

    click.echo('Continue? [yn] ', nl=False)
    c = click.getchar()
    click.echo()
    if c == 'y':
        click.echo('We will go on')
    elif c == 'n':
        click.echo('Abort!')
    else:
        click.echo('Invalid input :(')
    click.echo_via_pager('\n'.join('Line %d' % idx
                               for idx in range(200)))


@click.command()
@click.option('--uri', help='URI of ontology graph.')
@click.option('--outputpath', default="", prompt='The output path', help='The output path.')
@click.option('--gist', default=False, help='Save as gist.')
def main(uri, outputpath, gist):

    # select a model from the local ontologies

    # if opts._gist and not opts._export:
    #   printDebug("WARNING: the -g option must be used in combination with -e (=export)")
    #   sys.exit(0)

    if outputpath:
        if not(os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            click.secho("WARNING: not a valid directory path.", bg='blue', fg='white')
            sys.exit(0)

    url = action_visualize([uri], gist, False, outputpath)
    if url:# open browser
        webbrowser.open(url)

        # continue and print(timing at bottom )
        # ...



if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
