# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c) 2013-2017 __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

More info in the README file.

"""

import click
# http://click.pocoo.org/5/arguments/
# http://click.pocoo.org/5/options/
from . import *
from .. import *  # imports __init__
from ..core import actions
from ..core.manager import get_home_location




CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('source', nargs=-1)
@click.option('--library', '-l', is_flag=True, help='List ontologies saved in the local library.')
@click.option('--outputpath', '-o',  help='Output path (default: home folder).')
@click.option('--title',  help='Title for the visualization (default=graph uri).')
@click.option('--theme',  help='CSS Theme for the html-complex visualization (random=use a random theme).')
@click.option('--showthemes', is_flag=True, help='Show the available CSS theme choices.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode.')
def cli_run_viz(source=None, library=False, outputpath="", title="", theme="", showthemes=False, verbose=False):
    """
This application allows to create html or markdown documentation for an RDF model.
Example:

> ontospy-viz http://www.w3.org/2008/05/skos# --theme random -o ~/Desktop/skos

"""
    if showthemes:
        from .builder import show_themes
        show_themes()
        sys.exit(0)

    if theme and theme=="random":
        from .builder import random_theme
        theme = random_theme()

    if outputpath:
        if not(os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            click.secho("WARNING: the -o option must include a valid directory path.", fg="red")
            sys.exit(0)

    if not library and not source:
        # ctx.get_help()
        # ctx.invoke(get_help) how to???
        click.secho("WARNING: not enough options. Use -h for help.", fg="red")
        sys.exit(0)

    if library:
        click.secho("Showing the local library: '%s'" % get_home_location(), fg='red')

    if source and len(source) > 1:
        click.secho('Note: currently only one argument can be passed', fg='red')


    url = action_visualize(source, fromshell=False, path=outputpath, title=title, theme=theme, verbose=verbose)


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
