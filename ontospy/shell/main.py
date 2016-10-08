# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c) 2013-2016 __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

More info in the README file.

"""

import click
# http://click.pocoo.org/5/arguments/
# http://click.pocoo.org/5/options/

from .. import *  # imports __init__
from .shell import Shell, STARTUP_MESSAGE       



CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--source', '-s',  multiple=True, help='Load the shell with a specific graph (uri or file)')
def cli_run_shell(source):
    """This application launches the OntoSpy interactive shell."""
    Shell()._clear_screen()
    print(STARTUP_MESSAGE)
    if source and len(source) > 1:
        click.secho('Currenlty only first argument can be read', fg='green')
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
