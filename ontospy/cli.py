# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTOSPY
Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

"""

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
  > ontospy lib -s                             # ==> list ontologies available in the local library
  > ontospy lib --save http://xmlns.com/foaf/spec/ # ==> download FOAF vocabulary and save it in library

More info: <http://lambdamusic.github.io/Ontospy/>
------------
"""

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

##################
#
#  COMMAND LINE MAIN METHODS
#
##################
#
# 2018-08-23: restructuring the cli using command groups
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
Ontospy is a command line inspector for RDF/OWL models. Use the --help option with one of the commands listed below to find out more, or visit http://lambdamusic.github.io/Ontospy 
    """
    sTime = time.time()
    if ctx.obj is None:  # Fix for bug (as of 3.0)
        # https://github.com/pallets/click/issues/888
        ctx.obj = {}
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['STIME'] = sTime

    click.secho("Ontospy " + VERSION, fg='white')
    # click.secho("------------", fg='white')
    if not verbose and ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    # else:
    #     click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


##
## LIBRARY COMMAND
##


@main_cli.command()
@click.option(
    '--show',
    '-s',
    is_flag=True,
    help=
    'SHOW: list all ontologies stored in the local library and prompt which one to open.'
)
@click.option(
    '--bootstrap',
    is_flag=True,
    help='BOOTSTRAP: bootstrap the local library with popular ontologies.')
@click.option(
    '--cache',
    is_flag=True,
    help=
    'CACHE: force reset the cache folder for the local library (used to clean up old files and speed up loading of ontologies).'
)
@click.option(
    '--directory',
    is_flag=True,
    help=
    'DIRECTORY: set a (new) home directory for the local library. A valid path must be passed as argument.'
)
@click.option(
    '--reveal',
    is_flag=True,
    help=
    'REVEAL: open the local library folder using the OS. Note: from v1.9.4 all file management operations should be done via the OS.'
)
@click.option(
    '--save',
    is_flag=True,
    help=
    'SAVE: import a local or remote RDF file to the local library. If a local folder path is passed, all valid RDF files found in it get imported. If no argument is provided and there is an internet connection, it allows to scan online ontology repositories to find items of interests.'
)
@click.argument('filepath', nargs=-1)
@click.pass_context
def lib(ctx,
        filepath=None,
        bootstrap=False,
        cache=False,
        reveal=False,
        show=False,
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
    DONE_ACTION = False

    if bootstrap:
        DONE_ACTION = True
        action_bootstrap(verbose)
        printDebug("Tip: you can now load an ontology by typing `ontospy -l`",
                   "important")
        # raise SystemExit(1)

    elif cache:
        DONE_ACTION = True
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
            DONE_ACTION = True
            action_import(filepath[0], verbose)
        else:
            click.secho(
                "You provided no arguments - please specify what to save..",
                fg='white')
        raise SystemExit(1)

    elif show:
        click.secho("Local library => '%s'" % get_home_location(), fg='white')
        filename = action_listlocal(all_details=True)

        if filename:
            DONE_ACTION = True
            g = get_pickled_ontology(filename)
            if not g:
                g = do_pickle_ontology(filename)
            shellPrintOverview(g, print_opts)

    else:
        click.echo(ctx.get_help())
        return

    if DONE_ACTION:
        eTime = time.time()
        tTime = eTime - sTime
        printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")
    else:
        printDebug("Goodbye", "comment")


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
        action_analyze(sources, endpoint, print_opts, verbose)
        eTime = time.time()
        tTime = eTime - sTime
        printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")

    else:
        click.echo(ctx.get_help())


##
## SHELL COMMAND
##


@main_cli.command()
@click.argument('sources', nargs=-1)
def shell(sources=None):
    """Launch the ontospy repl - an interactive shell for querying ontologies. If an rdf source path is provided the repl is preloaded with it."
    """
    from .extras.shell import launch_shell
    launch_shell(sources)


##
## SERIALIZE COMMAND
##


@main_cli.command()
@click.argument('source', nargs=-1)
@click.option('-f', '--output_format', default='turtle')
# @click.argument('output_format', nargs=1)
@click.pass_context
def serial(ctx, source, output_format):
    """Serialize an RDF graph to a format of choice.
    """
    verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }
    output_format = output_format
    VALID_FORMATS = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml', "json-ld"]
    if not source:
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
            printDebug(
                "\n-----------\n" + "Serialized <%s> to '%s'" %
                (" ".join([x for x in source]), output_format), "comment")
            printDebug("Time:	   %0.2fs" % tTime, "comment")


##
## UTILS COMMAND
##


@main_cli.command()
@click.option(
    '--jsonld',
    '-j',
    is_flag=True,
    help=
    'JSONLD: util for testing a json-ld file using the online playground tool.'
)
@click.option(
    '--discover',
    '-d',
    is_flag=True,
    help='DISCOVER: find ontologies in online repositories like LOV or Prefix.cc'
)
@click.argument('filepath', nargs=-1)
@click.pass_context
def utils(
        ctx,
        filepath=None,
        jsonld=False,
        discover=False,
):
    """Miscellaneous utilities.
    """
    verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }
    DONE_ACTION = False

    if jsonld:
        if not filepath:
            click.secho(
                "What do you want to test? Please specify a valid JSONLD source.",
                fg='red')
        else:
            filepath = filepath[0]
            action_jsonld_playground(filepath, verbose)
            DONE_ACTION = True
    elif discover:
        DONE_ACTION = True
        action_webimport()
    else:
        click.secho("You haven't specified any utils command.")
        click.echo(ctx.get_help())

    if DONE_ACTION:
        eTime = time.time()
        tTime = eTime - sTime
        printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")


if __name__ == '__main__':
    import sys
    try:
        main_cli(prog_name='ontospy')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

##
## GENDOCS COMMAND (wrapper around ontodocs)
##


@main_cli.command()
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
@click.pass_context
def gendocs(ctx,
            source=None,
            outputpath="",
            title="",
            theme="",
            showthemes=False):
    """Generate documentation for an ontology in html or markdown format
    """
    verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }

    from .ontodocs.builder import action_visualize, show_themes, random_theme

    try:
        # check that we have the required dependencies
        import django
    except:
        click.secho(
            "WARNING: this functionality requires the Django package and other extra dependecies.",
            fg="red")
        click.secho("Install with `pip install ontospy[HTML] -U`")
        sys.exit(0)

    if not source and not showthemes:
        click.echo(ctx.get_help())
        return

    if showthemes:
        show_themes()
        sys.exit(0)

    if theme and theme == "random":
        theme = ontodocs.random_theme()

    if outputpath:
        if not (os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            click.secho(
                "WARNING: the -o option must include a valid directory path.",
                fg="red")
            sys.exit(0)

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

    eTime = time.time()
    tTime = eTime - sTime
    printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")


if __name__ == '__main__':
    import sys
    try:
        main_cli(prog_name='ontospy')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
