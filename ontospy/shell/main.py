# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c) 2013-2017 __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

More info in the README file.

"""

import sys
import click
# http://click.pocoo.org/5/arguments/
# http://click.pocoo.org/5/options/

try:
    import readline
except:
    click.secho("WARNING: ontospy shell can't without the readline library.", fg='red')
    click.secho("Tip: install it with `pip install readline` (you can try pyreadline on Windows)", fg='green')
    sys.exit(0)

from .. import *  # imports __init__
from .shell import Shell, STARTUP_MESSAGE



CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# @click.option('--source', '-s',  multiple=True, help='Load the shell with a specific graph (uri or file)')

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('source', nargs=-1)
def cli_run_shell(source=None):
    """
This application launches the OntoSpy interactive shell.

Note: if a local path or URI of an RDF model is provided, that gets loaded into the shell by default. E.g.:

> ontospy-shell path/to/mymodel.rdf

"""
    Shell()._clear_screen()
    print(STARTUP_MESSAGE)
    if source and len(source) > 1:
        click.secho('Note: currently only one argument can be passed', fg='red')
    uri = source[0] if source else None
    Shell(uri).cmdloop()
    raise SystemExit(1)



if __name__ == '__main__':
    try:
        # http://stackoverflow.com/questions/32553969/modify-usage-string-on-click-command-line-interface-on-windows
        cli_run_shell(prog_name='ontospy-shell')
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
