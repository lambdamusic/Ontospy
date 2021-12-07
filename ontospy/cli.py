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


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

VALID_FORMATS = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml', "json-ld"]

def validate_format_string(s):
    if s not in VALID_FORMATS:
        printDebug(
            "Not a valid format - must be one of: 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'json-ld'.",
            fg='red')
        return False
    return True


##################
#
#  COMMAND LINE MAIN METHODS
# http://click.pocoo.org/6/commands/
# test with python -m ontospy.cli library
#
##################

##
## WRAPPER
# so that commands are listed in order of appearance
# https://github.com/pallets/click/issues/513
##
##

from collections import OrderedDict


class NaturalOrderGroup(click.Group):
    """Command group trying to list subcommands in the order they were added.

    Make sure you initialize the `self.commands` with OrderedDict instance.

    With decorator, use::

        @click.group(cls=NaturalOrderGroup, commands=OrderedDict())
    """

    def list_commands(self, ctx):
        """List command names as they are in commands dict.

        If the dict is OrderedDict, it will preserve the order commands
        were added.
        """
        return self.commands.keys()


##
## TOP LEVEL COMMAND
##


@click.group(
    cls=NaturalOrderGroup,
    commands=OrderedDict(),
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS)
@click.option(
    '--verbose', '-v', is_flag=True, help='VERBOSE: print out debug messages.')
@click.pass_context
def main_cli(ctx, verbose=False):
    """
Ontospy allows to extract and visualise ontology information included in RDF data. Use one of the commands listed below to find out more, or visit http://lambdamusic.github.io/ontospy 
    """
    sTime = time.time()
    if ctx.obj is None:  # Fix for bug (as of 3.0)
        # https://github.com/pallets/click/issues/888
        ctx.obj = {}
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['STIME'] = sTime

    printDebug("Ontospy " + VERSION, "comment")
    if not verbose and ctx.invoked_subcommand is None:
        printDebug(ctx.get_help())
    # else:
    #     printDebug('I am about to invoke %s' % ctx.invoked_subcommand)


##
## SCAN COMMAND
##


@main_cli.command()
@click.argument('sources', nargs=-1)
@click.option(
    '--extra',
    '-x',
    is_flag=True,
    help=
    'EXTRA-DATA: extract implicit types and predicates using basic inference rules. Note: by default ontospy extracts only classes/properties which are explictly declared.'
)
@click.option(
    '--individuals',
    '-i',
    is_flag=True,
    help=
    'INDIVIDUALS: extract class instances as well. Note: by default ontospy extracts direct instances of explicitly declared classes. Use with -x option to get all possible instances.'
)
@click.option(
    '--raw',
    '-r',
    is_flag=True,
    help='RAW-DATA: print out the raw RDF data received.')
@click.option(
    '--endpoint',
    '-e',
    is_flag=True,
    help='ENDPOINT: the url passed is a sparql endpoint (beta).')
@click.option(
    '-f',
    '--format',
    default='',
    help='RDF-FORMAT: the serialization format of the input file (default=inferred)')
@click.option(
    '--verbose', '-v', is_flag=True, help='VERBOSE: print out debug messages.')
@click.pass_context
def scan(ctx, sources=None, endpoint=False, raw=False, extra=False, individuals=False, verbose=False, format=False):
    """SCAN: get ontology data from RDF source and print out a report.
    """
    # verbose = ctx.obj['VERBOSE']  # TODO 2021-11-14 VERBOSE INHERITANCE BROKEN ?
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
        'extra': extra,
        'individuals': individuals,
    }

    if format and not validate_format_string(format):
        return
    if sources or (sources and endpoint):
        action_analyze(sources, endpoint, print_opts, verbose, extra, raw, individuals, format)
        eTime = time.time()
        tTime = eTime - sTime
        printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")

    else:
        printDebug(ctx.get_help())


##
## GENDOCS COMMAND (wrapper around ontodocs)
##


@main_cli.command()
@click.argument('source', nargs=-1)
@click.option(
    '-l',
    '--lib',
    is_flag=True,
    help='LIBRARY: choose an ontology from your local library.')
@click.option(
    '--outputpath',
    '-o',
    help=
    'OUTPUT-PATH: where to save the visualization files (default: home folder).'
)
@click.option(
    '--extra',
    '-x',
    is_flag=True,
    help=
    'EXTRA-DATA: extract implicit types and predicates using basic inference rules. Note: by default ontospy extracts only classes/properties which are explictly declared.'
)
@click.option(
    '--individuals',
    '-i',
    is_flag=True,
    help=
    'INDIVIDUALS: extract class instances as well. Note: by default ontospy extracts only instances of explicitly declared classes. Use with -x option to get all possible instances.'
)
@click.option(
    '--type',
    help=
    'VIZ-TYPE: specify which viz type to use as an integer (eg 1=single-page html, 2=multi-page etc..).'
)
@click.option(
    '--title',
    help='TITLE: custom title for the visualization (default=graph uri).')
@click.option(
    '--theme',
    help=
    'THEME: select bootstrap style (only for the html-multi-page visualization). Default: simplex (random=use a random theme).'
)
@click.option(
    '--preflabel',
    help='PREF-LABEL: default value to use for entity titles (qname|label - default=qname).')
@click.option(
    '--preflang',
    help=
    'PREF-LANGUAGE: default language for multilingual strings (default=en).'
)
@click.option(
    '--nobrowser',
    is_flag=True,
    help="NO-BROWSER: prevents opening the html output in the browser by default.")
@click.option(
    '--showtypes',
    is_flag=True,
    help='SHOW-TYPES: show the available visualization types.')
@click.option(
    '--showthemes',
    is_flag=True,
    help='SHOW-THEMES: show the available css theme choices.')
@click.option(
    '--verbose', '-v', is_flag=True, help='VERBOSE: print out debug messages.')
@click.pass_context
def gendocs(ctx,
            lib=False,
            source=None,
            outputpath="",
            extra=False,
            individuals=False,
            type="",
            title="",
            theme="",
            preflabel="",
            preflang="",
            nobrowser=False,
            showthemes=False,
            showtypes=False,
            verbose=False):
    """GENDOCS: generate documentation in html or markdown format.
    """
    # verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']

    from .ontodocs.builder import show_themes, random_theme, show_types

    try:
        # check that we have the required dependencies
        import django
    except:
        printDebug(
            "WARNING: this functionality requires the Django package and other extra dependecies.",
            fg="red")
        printDebug("Install with `pip install ontospy[HTML] -U`")
        sys.exit(0)

    if not source and not showthemes and not showtypes and not lib:
        printDebug(ctx.get_help())
        return

    if showthemes:
        show_themes()
        sys.exit(0)

    if showtypes:
        show_types()
        sys.exit(0)

    if theme and theme == "random":
        theme = random_theme()

    if preflabel and preflabel not in ["label", "qname"]:
        printDebug(
            "WARNING: the valid preflabel options are either 'qname' or 'label' (= rdfs:label) only. Using defaults.",
            fg="red")
        preflabel = "qname"

    if outputpath:
        if not (os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            printDebug(
                "WARNING: the -o option must include a valid directory path.",
                fg="red")
            sys.exit(0)

    if source and len(source) > 1:
        printDebug(
            'Note: currently only one argument can be passed', fg='red')

    if lib:
        printDebug("Local library => '%s'" % get_home_location(), fg='white')
        ontouri = action_listlocal(all_details=False)
        if ontouri:
            source = [os.path.join(get_home_location(), ontouri)]
        else:
            raise SystemExit(1)

    # note: the local ontospy library gets displayed via this method too
    url = action_visualize(
        source,
        fromshell=False,
        path=outputpath,
        title=title,
        viztype=type,
        theme=theme,
        preflabel=preflabel,
        preflang=preflang,
        extra= extra,
        individuals= individuals,
        verbose=verbose)


    if url and (not nobrowser):  # open browser
        import webbrowser
        webbrowser.open(url)

    eTime = time.time()
    tTime = eTime - sTime
    printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")


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
    '--extra',
    '-x',
    is_flag=True,
    help=
    'EXTRA-DATA: extract implicit types and predicates using basic inference rules. Note: by default ontospy extracts only classes/properties which are explictly declared.'
)
@click.option(
    '--individuals',
    '-i',
    is_flag=True,
    help=
    'INDIVIDUALS: extract class instances as well. Note: by default ontospy extracts only instances of explicitly declared classes. Use with -x option to get all possible instances.'
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
@click.option(
    '--verbose', '-v', is_flag=True, help='VERBOSE: print out debug messages.')
@click.argument('filepath', nargs=-1)
@click.pass_context
def lib(ctx,
        filepath=None,
        extra=False,
        individuals=False,
        bootstrap=False,
        cache=False,
        reveal=False,
        show=False,
        save=False,
        directory=False,
        verbose=False):
    """
    LIBRARY: work with a local library of RDF models.
    """
    # verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
        'extra': extra,
        'individuals': individuals,
    }
    DONE_ACTION = False

    if bootstrap:
        DONE_ACTION = True
        action_bootstrap(verbose)
        printDebug("Tip: you can now load an ontology by typing `ontospy lib -s`",
                   "important")
        # raise SystemExit(1)

    elif cache:
        DONE_ACTION = True
        action_cache_reset()

    elif directory:
        if not filepath:
            printDebug("Please specify a new directory for the local library.",
                       'important')
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
            printDebug(
                "You provided no arguments - please specify what to save..",
                fg='white')
        raise SystemExit(1)

    elif show:
        printDebug("Local library => '%s'" % get_home_location(), fg='white')
        filename = action_listlocal(all_details=False)

        if filename:
            DONE_ACTION = True
            g = get_pickled_ontology(filename)
            if not g:
                g = do_pickle_ontology(filename)
            shellPrintOverview(g, print_opts)

    else:
        printDebug(ctx.get_help())
        return

    if DONE_ACTION:
        eTime = time.time()
        tTime = eTime - sTime
        printDebug("\n-----------\n" + "Time:	   %0.2fs" % tTime, "comment")
    else:
        printDebug("Goodbye", "comment")


##
## SHELL COMMAND'
##


@main_cli.command()
@click.argument('sources', nargs=-1)
def shell(sources=None):
    """SHELL: launch ontospy's interactive mode. If an rdf source path is provided the shell is preloaded with it."
    """
    from .extras.shell import launch_shell
    launch_shell(sources)


##
## SERIALIZE COMMAND
##


@main_cli.command()
@click.argument('source', nargs=-1)
@click.option(
    '-f',
    '--output_format',
    default='turtle',
    help='OUTPUT-FORMAT: the serialization format (default=turtle)')
@click.option(
    '--verbose', '-v', is_flag=True, help='VERBOSE: print out debug messages.')
@click.pass_context
def ser(ctx, source, output_format, verbose=False):
    """SERIALIZE: tranform an RDF graph to a format of choice.
    """
    # verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }
    if not source:
        printDebug(ctx.get_help())
    else:
        if not validate_format_string(output_format):
            return
        else:
            action_serialize(source, output_format, verbose)
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
    help='JSONLD: test a json-ld file using the online playground tool.')
@click.option(
    '--discover',
    '-d',
    is_flag=True,
    help='DISCOVER: find ontologies in online repositories like LOV or Prefix.cc'
)
@click.option(
    '--verbose', '-v', is_flag=True, help='VERBOSE: print out debug messages.')
@click.argument('filepath', nargs=-1)
@click.pass_context
def utils(
        ctx,
        filepath=None,
        jsonld=False,
        discover=False,
        verbose=False,
):
    """UTILS: miscellaneous bits and pieces.
    """
    # verbose = ctx.obj['VERBOSE']
    sTime = ctx.obj['STIME']
    print_opts = {
        'labels': verbose,
    }
    DONE_ACTION = False

    if jsonld:
        if not filepath:
            printDebug(
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
        printDebug("You haven't specified any utils command.")
        printDebug(ctx.get_help())

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

if __name__ == '__main__':
    import sys
    try:
        main_cli(prog_name='ontospy')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
