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
from ..core import actions


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('source', nargs=-1)
@click.option('--outputpath', '-o',  help='Output path (default: home folder)')
def cli_run_viz(source=None, outputpath=""):
    """
This application launches the OntoSpy visualization tool.

Example:
    
> ontospy-viz path/to/mymodel.rdf

Note: if the location of an RDF model is not provided, a selection can be made from the contents of the local ontospy library folder.

"""

    if outputpath:
        if not(os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            click.secho("WARNING: the -o option must include a valid directory path.", fg="red")
            sys.exit(0)        

    if source and len(source) > 1:
        click.secho('Note: currently only one argument can be passed', fg='red')

    url = actions.action_visualize(source, fromshell=False, path=outputpath)

    if url:# open browser
        import webbrowser
        webbrowser.open(url)

        # continue and print(timing at bottom )

    raise SystemExit(1)



if __name__ == '__main__':
    try:
        # http://stackoverflow.com/questions/32553969/modify-usage-string-on-click-command-line-interface-on-windows
        cli_run_viz(prog_name='ontospy-viz')
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e

