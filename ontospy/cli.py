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

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

##################
#
#  COMMAND LINE MAIN METHODS
#
##################
#
# 2018-08-23: trying to restructure the cli using command groups
# http://click.pocoo.org/6/commands/
# test with python -m ontospy.cli library

##
## TOP LEVEL COMMAND
##


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Print out version info and debug messages.')
@click.pass_context
def main_cli(ctx, verbose=False):
    """
Ontospy is a command line inspector for RDF/OWL models. Use --help option with one of the commands listed below to find out more. Or visit <https://github.com/lambdamusic/ontospy/wiki>.
    """
    sTime = time.time()
    if ctx.obj is None:  # Fix for bug (as of 3.0)
        # https://github.com/pallets/click/issues/888
        ctx.obj = {}
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['STIME'] = sTime
    if verbose:
        click.secho("Ontospy " + VERSION, bold=True)
        click.secho("------------", fg='white')
    if not verbose and ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    # else:
    #     click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


##
## CHECK / ANALYZE / SCAN COMMAND
##


@main_cli.command()
@click.argument('sources', nargs=-1)
@click.option(
    '--endpoint',
    '-e',
    is_flag=True,
    help='Use to specify that the source url passed is a sparql endpoint')
@click.pass_context
def scan(ctx, sources=None, endpoint=False):
    """Search an RDF source for ontology entities and print out a report.
    """
    verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }
    if sources or (sources and endpoint):
        action_analyze(sources, endpoint)
        eTime = time.time()
        tTime = eTime - sTime
        printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")

    else:
        click.echo(ctx.get_help())


##
## LIBRARY COMMAND
##


@main_cli.command()
@click.option(
    '--bootstrap',
    '-b',
    is_flag=True,
    help='BOOTSTRAP: bootstrap the local library with a few sample models.')
@click.option(
    '--cache',
    '-c',
    is_flag=True,
    help=
    'CACHE: force reset the cache folder for the local library (used to clean up old files and speed up loading of ontologies).'
)
@click.option(
    '--reveal',
    '-r',
    is_flag=True,
    help=
    'REVEAL: open the local library folder using default app. Note: from v1.9.4 all file management operations should be done via the OS.'
)
@click.option(
    '--directory',
    '-d',
    is_flag=True,
    help=
    'DIRECTORY: set a (new) home directory for the local library. A valid path must be passed as argument.'
)
@click.option(
    '--save',
    '-s',
    is_flag=True,
    help=
    'SAVE: import a local or remote RDF file to the local library. If a local folder path is passed, all valid RDF files found in it get imported. If no argument is provided and there is an internet connection, it allows to scan online ontology repositories to find items of interests.'
)
@click.argument('filepath', nargs=-1)
@click.pass_context
def library(ctx,
            filepath=None,
            bootstrap=False,
            cache=False,
            reveal=False,
            save=False,
            directory=False):
    """
    Work with a local library of RDF models. If no option or argument is passed, by default the library contents are listed.
    """
    verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }

    if bootstrap:
        action_bootstrap()
        printDebug("Tip: you can now load an ontology by typing `ontospy -l`",
                   "important")
        # raise SystemExit(1)

    elif cache:
        action_cache_reset()

    elif directory:
        if not filepath:
            printDebug("Please specify a new directory for the local library.",
                       'important')
            printDebug(
                "E.g. 'ontospy library --update /Users/john/ontologies'",
                'tip')
            sys.exit(0)
        else:
            _location = filepath[0]
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

    elif reveal:
        action_reveal_library()
        raise SystemExit(1)

    elif save:
        if filepath:
            action_import(filepath[0])
        else:
            click.secho(
                "You provided no arguments - starting web import wizard..",
                fg='white')
            action_webimport()
        raise SystemExit(1)

    else:
        # by default, show the local library
        click.secho(
            "Tip: view all options for the library command with `ontospy library -h`\n-------------",
            fg='white')
        click.secho("Local library => '%s'" % get_home_location(), fg='white')
        filename = action_listlocal(all_details=True)

        if filename:
            g = get_pickled_ontology(filename)
            if not g:
                g = do_pickle_ontology(filename)
            shellPrintOverview(g, print_opts)

    eTime = time.time()
    tTime = eTime - sTime
    printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")


##
## SHELL COMMAND
##


@main_cli.command()
@click.argument('sources', nargs=-1)
def shell(sources=None):
    """Launch the ontospy repl - an interactive shell for querying ontologies. If an rdf source path is provided the repl is preloaded with it."
    """
    from extras.shell import launch_shell
    launch_shell(sources)


##
## TRANSFORM COMMAND
##


@main_cli.command()
@click.argument('source', nargs=1)
@click.argument('output_format', nargs=1)
@click.pass_context
def transform(ctx, source, output_format):
    """Output a different RDF serialization for a given source.
    """
    verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }
    VALID_FORMATS = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'json-ld']
    if not source:
        if serialize:
            click.secho(
                "What do you want to serialize? Please specify a valid RDF source.",
                fg='red')
        click.echo(ctx.get_help())
    else:
        if output_format not in VALID_FORMATS:
            click.secho(
                "Not a valid format - must be one of: 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'json-ld'.",
                fg='red')
            return
        else:
            action_transform(source, output_format, verbose)
            eTime = time.time()
            tTime = eTime - sTime
            printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime,
                       "comment")


if __name__ == '__main__':
    import sys
    try:
        main_cli(prog_name='ontospy')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
