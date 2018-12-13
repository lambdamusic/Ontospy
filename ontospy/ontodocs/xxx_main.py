# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTODOCS
Copyright (c) 2013-2017 __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

More info in the README file.

"""

import time
import click
# http://click.pocoo.org/5/arguments/
# http://click.pocoo.org/5/options/

from ontospy.core import manager as ontospy_manager
from ontospy import VERSION as ontospy_VERSION

from . import *
from .core.builder import *

# http://stackoverflow.com/questions/1714027/version-number-comparison
from distutils.version import LooseVersion

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('source', nargs=-1)
@click.option('--outputpath', '-o', help='Output path (default: home folder).')
@click.option(
    '--title', '-t', help='Title for the visualization (default=graph uri).')
@click.option(
    '--theme',
    help=
    'CSS Theme for the html-complex visualization (random=use a random theme).'
)
@click.option(
    '--showthemes', is_flag=True, help='Show the available CSS theme choices.')
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode.')
def main_cli(source=None,
             outputpath="",
             title="",
             theme="",
             showthemes=False,
             verbose=False):
    """
Ontodocs allows to create  documentation for ontologies encoded in RDF/OWL.

IMPORTANT: in future versions this CLI will be integrated within ontospy 

E.g.:

> ontodocs http://www.w3.org/2008/05/skos# --theme random -o ~/Desktop/skos

==> generates html docs for the SKOS ontology and save it to your desktop
"""

    if LooseVersion(ontospy_VERSION.replace("v", "")) < LooseVersion('1.8'):
        click.secho(
            "WARNING: OntoDocs requires OntoSpy >= v1.8 but it looks like you have installed %s."
            % ontospy_VERSION,
            fg="red")
        sys.exit(0)

    sTime = time.time()
    ontospy_manager.get_or_create_home_repo()
    click.echo(
        click.style("OntoDocs " + VERSION, bold=True) +
        click.style(" (OntoSpy " + ontospy_VERSION + ")", fg='white'))

    # click.secho("OntoDocs " + VERSION,  bold=True)
    # click.secho("OntoSpy " + ontospy_VERSION)
    # click.echo(click.style('Hello World!', fg='green') + click.style('Hello World!', fg='red'))
    # click.secho("Local library: '%s'" % get_home_location(), fg='white')
    click.secho("------------", fg='white')

    if showthemes:
        # from .core.builder import show_themes
        show_themes()
        sys.exit(0)

    if theme and theme == "random":
        # from .core.builder import random_theme
        theme = random_theme()

    if outputpath:
        if not (os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            click.secho(
                "WARNING: the -o option must include a valid directory path.",
                fg="red")
            sys.exit(0)

    if not source:
        # ask to show local library
        click.secho("You haven't specified any argument.", fg='red')
        click.secho(
            "Please select an ontology from the local OntoSpy library.")

    if source and len(source) > 1:
        click.secho(
            'Note: currently only one argument can be passed', fg='red')

    # note: the local ontospy library gets displayed via this method too
    url = action_visualize(
        source,
        fromshell=False,
        path=outputpath,
        title=title,
        theme=theme,
        verbose=verbose)

    if url:  # open browser
        import webbrowser
        webbrowser.open(url)

    # finally: print(some stats.... )
    eTime = time.time()
    tTime = eTime - sTime
    printDebug("\n----------\n" + "Time:	   %0.2fs" % tTime, "comment")


if __name__ == '__main__':
    try:
        # http://stackoverflow.com/questions/32553969/modify-usage-string-on-click-command-line-interface-on-windows
        main_cli(prog_name='ontodocs')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
