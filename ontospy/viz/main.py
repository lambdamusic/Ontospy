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
@click.option('--source', '-s',  multiple=True, help='Load the visualizer with a specific graph (uri or file)')
@click.option('--outputpath', '-o',  help='Output path')
@click.option('--savegist', '-g',  help='Save as anonymous gist')
def cli_run_viz(source=None, outputpath="", savegist=False):
    """This application ........."""

    # @todo: savegist should be a boolean
    #revise anyways

    print source ,outputpath, savegist

    if outputpath:
        if not(os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            printDebug("WARNING: the -o option must include a valid directory path.")
            sys.exit(0)        


    url = actions.action_visualize(source, savegist, False, outputpath)

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

