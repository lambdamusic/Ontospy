# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTOSPY
Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

"""

from __future__ import print_function

import sys
import os
import time
import optparse
import os.path
import shutil
import requests

try:
    import cPickle
except ImportError:
    import pickle as cPickle

try:
    import urllib2
except ImportError:
    import urllib as urllib2

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

import click
# http://click.pocoo.org/5/python3/
click.disable_unicode_literals_warning = True

from . import *  # imports __init__
from .VERSION import *

from .core.actions import *
from .core.ontospy import Ontospy
from .core.manager import *
from .core.utils import *

SHELL_EXAMPLES = """
Quick Examples:

  > ontospy ~/Desktop/mymodel.rdf          # ==> inspect a local RDF file
  > ontospy -l                             # ==> list ontologies available in the local library
  > ontospy -s http://xmlns.com/foaf/spec/ # ==> download FOAF vocabulary and save it in library

More info: <ontospy.readthedocs.org>
------------
"""

##################
#
#  COMMAND LINE MAIN METHODS
#
##################

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('sources', nargs=-1)
@click.option(
    '--bootstrap',
    '-b',
    is_flag=True,
    help='BOOTSTRAP: bootstrap the local library.')
@click.option(
    '--cache',
    '-c',
    is_flag=True,
    help='CACHE: force caching of the local library (for faster loading).')
@click.option(
    '--delete',
    '-d',
    is_flag=True,
    help='DELETE: remove an ontology from the local library.')
@click.option(
    '--endpoint',
    '-e',
    is_flag=True,
    help='ENDPOINT: query a sparql endpoint.')
@click.option(
    '--library',
    '-l',
    is_flag=True,
    help='LIBRARY: list ontologies saved in the local library.')
@click.option(
    '--save',
    '-s',
    is_flag=True,
    help='SAVE: save a file/folder/url into the local library.')
@click.option(
    '--reset',
    '-r',
    is_flag=True,
    help='RESET: delete all files in the local library.')
@click.option(
    '--update',
    '-u',
    is_flag=True,
    help='UPDATE: enter new path for the local library.')
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='VERBOSE: verbose logs and entities labels.')
@click.option(
    '--web',
    '-w',
    is_flag=True,
    help='WEB: import ontologies from remote repositories.')
@click.option(
    '--shell', '-z', is_flag=True, help='SHELL: launch the interactive shell.')
@click.pass_context
def main_cli(ctx,
             sources=None,
             library=False,
             verbose=False,
             save=False,
             bootstrap=False,
             web=False,
             shell=False,
             cache=False,
             update=False,
             delete=False,
             reset=False,
             endpoint=False):
    """
Ontospy is a command line inspector for RDF/OWL knowledge models.

Examples:

Inspect a local RDF file:

> ontospy /path/to/mymodel.rdf

List ontologies available in the local library:

> ontospy -l

Open FOAF vocabulary and save it to the local library:

> ontospy http://xmlns.com/foaf/spec/ -s

More info: <https://github.com/lambdamusic/ontospy/wiki>


    """

    sTime = time.time()
    if not update:
        get_or_create_home_repo()
    print_opts = {
        'labels': verbose,
    }

    click.secho("OntoSpy " + VERSION, bold=True)
    # click.secho("Local library: '%s'" % get_home_location(), fg='white')
    click.secho("------------", fg='white')

    if bootstrap:
        action_bootstrap()
        printDebug("Tip: you can now load an ontology by typing `ontospy -l`",
                   "important")
        # raise SystemExit(1)

    elif cache:
        action_cache()

    elif delete:
        res = actions_delete()
        # raise SystemExit(1)

    elif library:
        click.secho("Local library: '%s'" % get_home_location(), fg='white')
        filename = action_listlocal(all_details=True)
        if filename:
            g = get_pickled_ontology(filename)
            if not g:
                g = do_pickle_ontology(filename)
            shellPrintOverview(g, print_opts)

    # save?? missing

    elif reset:
        action_erase()
        # raise SystemExit(1)

    elif update:
        if not sources:
            printDebug("Please specify a new location for the local library.",
                       'important')
            printDebug("E.g. 'ontospy -u /Users/john/ontologies'", 'tip')
            sys.exit(0)
        else:
            _location = sources[0]
            if _location.endswith("/"):
                # dont need the final slash
                _location = _location[:-1]
            output = action_update_library_location(_location)
            if output:
                printDebug(
                    "Note: no files have been moved or deleted (this has to be done manually)",
                    "comment")
                printDebug("----------\n" + "New location: '%s'" % _location,
                           "important")

            else:
                printDebug(
                    "----------\n" + "Please specify an existing folder path.",
                    "important")
            raise SystemExit(1)

    elif web:
        action_webimport()
        # raise SystemExit(1)

    elif shell:
        from extras.shell import launch_shell
        launch_shell(sources)

    else:
        if sources or (sources and endpoint):
            for x in sources:
                click.secho("Parsing %s..." % str(x), fg='white')

            if endpoint:
                g = Ontospy(sparql_endpoint=sources[0], verbose=verbose)
                printDebug("Extracting classes info")
                g.build_classes()
                printDebug("..done")
                printDebug("Extracting properties info")
                g.build_properties()
                printDebug("..done")
            else:
                g = Ontospy(uri_or_path=sources, verbose=verbose)

            shellPrintOverview(g, print_opts)

        else:
            click.echo(ctx.get_help())
            return

    # finally: print(some stats.... )
    eTime = time.time()
    tTime = eTime - sTime
    printDebug("\n----------\n" + "Time:	   %0.2fs" % tTime, "comment")


if __name__ == '__main__':
    import sys
    try:
        main_cli(prog_name='ontospy')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
