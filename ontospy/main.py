# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTOSPY
Copyright (c) 2013-2016 __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

"""

from __future__ import print_function

import sys, os, time, optparse, os.path, shutil, requests

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
@click.option('--bootstrap', '-b', is_flag=True, help='BOOTSTRAP: bootstrap the local library.')
@click.option('--library', '-l', is_flag=True, help='LIBRARY: list ontologies saved in the local library.')
@click.option('--save', '-s', is_flag=True, help='SAVE: save a file/folder/url into the local library.')
@click.option('--verbose', '-v', is_flag=True, help='VERBOSE: show entities labels as well as URIs.')
@click.option('--web', '-w', is_flag=True, help='WEB: import a vocabulary from an online directory.')
def main_cli(sources=None, library=False, verbose=False, save=False, bootstrap=False, web=False):
    """
Ontospy is a command line inspector for RDF/OWL knowledge models.

Examples:

Inspect a local RDF file:

> ontospy /path/to/mymodel.rdf

List ontologies available in the local library:

> ontospy -l

Open FOAF vocabulary and save it to the local library:

> ontospy http://xmlns.com/foaf/spec/ -s

More info: <ontospy.readthedocs.org>
    
    
    """

    sTime = time.time()
    get_or_create_home_repo()
    print_opts = {
                    'labels' : verbose,
                }
    if False: #debug
        print(sources, library, verbose, save, bootstrap, web)

    click.secho("OntoSpy " + VERSION,  bold=True)
    # click.secho("Local library: '%s'" % get_home_location(), fg='white')
    click.secho("------------", fg='white')
    
    if bootstrap:
        action_bootstrap()
        # raise SystemExit(1)
    
    elif web:
        action_webimport()
        # raise SystemExit(1)
    
    elif library:
        click.secho("Local library: '%s'" % get_home_location(), fg='white')
        filename = action_listlocal()
        if filename:
            g = get_pickled_ontology(filename)
            if not g:
                g = do_pickle_ontology(filename)
            shellPrintOverview(g, print_opts)
    
    else:
        if not sources:
            click.secho("Note: please specify a data source (-h for more options).", fg='red')
            raise SystemExit(1)
        else:
            t = "You passed the arguments:%s" % "".join([ "\n-> <%s>" % str(x) for x in sources])
            click.secho(str(t), fg='green')
            g = Ontospy(uri_or_path=sources)
            shellPrintOverview(g, print_opts)


    # finally: print(some stats.... )
    eTime = time.time()
    tTime = eTime - sTime
    printDebug("\n----------\n" + "Time:	   %0.2fs" %  tTime, "comment")




if __name__ == '__main__':
    import sys
    try:
        main_cli(prog_name='ontospy')
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
