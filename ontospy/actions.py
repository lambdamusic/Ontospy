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

try:
    from ConfigParser import SafeConfigParser
except ImportError:  # python3
    from configparser import SafeConfigParser

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

import time, optparse, os, rdflib, sys, datetime


from colorama import Fore, Style


from . import *  # imports __init__
from ._version import *
from .core.graph import Graph
from .core.util import *






# ===========
# ACTIONS FIRED FROM THE SHELL OR COMMAND LINE
# note: all actions are loaded in ontospy.py and called from other modules as 'ontospy.action_bootstrap' etc...
# ===========




def action_listlocal():
    " select a file from the local repo "

    options = get_localontologies()

    counter = 1
    # printDebug("------------------", 'comment')
    if not options:
        printDebug("Your local library is empty. Use 'ontospy -i <uri>' to add more ontologies to it.")
        return
    else:
        _print_table_ontologies()

        while True:
            printDebug("------------------\nSelect a model by typing its number: (enter=quit)", "important")
            var = input()
            if var == "":
                return None
            else:
                try:
                    _id = int(var)
                    ontouri = options[_id - 1]
                    printDebug("\nYou selected:", "comment")
                    printDebug("---------\n" + ontouri + "\n---------", "red")
                    return ontouri
                except:
                    printDebug("Please enter a valid option.", "comment")
                    continue






def _print_table_ontologies():
    """
    list all local files
    2015-10-18: removed 'cached' from report
    2016-06-17: made a subroutine of action_listlocal()
    """
    ontologies = get_localontologies()
    ONTOSPY_LOCAL_MODELS = get_home_location()

    if ontologies:
        print("")
        temp = []
        from collections import namedtuple
        Row = namedtuple('Row',['N','Added', 'File'])
        # Row = namedtuple('Row',['N','Added','Cached', 'File'])
        counter = 0
        for file in ontologies:
            counter += 1
            # _counter = Fore.BLUE + Style.BRIGHT + str(counter) + Style.RESET_ALL
            _counter = str(counter)
            name = Style.BRIGHT + file + Style.RESET_ALL
            try:
                mtime = os.path.getmtime(ONTOSPY_LOCAL_MODELS + "/" + file)
            except OSError:
                mtime = 0
            last_modified_date = str(datetime.datetime.fromtimestamp(mtime))

            # cached = str(os.path.exists(ONTOSPY_LOCAL_CACHE + "/" + file + ".pickle"))
            temp += [Row(_counter,last_modified_date, name)]
        pprinttable(temp)
        print("")
    return





def action_import(location, verbose=True, lock=None):
    """import files into the local repo
        <lock> was used by the Threaded routine *now removed* 2016-04-24

    """

    location = str(location) # prevent errors from unicode being passed

    # 1) extract file from location and save locally
    ONTOSPY_LOCAL_MODELS = get_home_location()
    fullpath = ""
    try:
        if location.startswith("www."): #support for lazy people
            location = "http://%s" % str(location)
        if location.startswith("http"):
            # print("here")
            headers = {'Accept': "application/rdf+xml"}
            req = urllib2.Request(location, headers=headers)
            res = urllib2.urlopen(req)
            final_location = res.geturl()  # after 303 redirects
            printDebug("Saving data from <%s>" % final_location, "green")
            # filename = final_location.split("/")[-1] or final_location.split("/")[-2]
            filename = location.replace("http://", "").replace("/", "_")
            if not filename.lower().endswith(('.rdf', '.owl', '.rdfs', '.ttl', '.n3')):
                filename = filename + ".rdf"
            fullpath = ONTOSPY_LOCAL_MODELS + "/" + filename # 2016-04-08
            # fullpath = ONTOSPY_LOCAL_MODELS + filename

            # print("==DEBUG", final_location, "**", filename,"**", fullpath)

            file_ = open(fullpath, 'w')
            file_.write(res.read())
            file_.close()
        else:
            if os.path.isfile(location):
                filename = location.split("/")[-1] or location.split("/")[-2]
                fullpath = ONTOSPY_LOCAL_MODELS + "/" + filename
                shutil.copy(location, fullpath)
            else:
                raise ValueError('The location specified is not a file.')
        # print("Saved local copy")
    except:
        printDebug("Error retrieving file. Please make sure <%s> is a valid location." % location, "important")
        if os.path.exists(fullpath):
            os.remove(fullpath)
        return None

    try:
        g = Graph(fullpath, verbose=verbose)
        # printDebug("----------")
    except:
        g = None
        if os.path.exists(fullpath):
            os.remove(fullpath)
        printDebug("Error parsing file. Please make sure %s contains valid RDF." % location, "important")

    if g:
        printDebug("Caching...", "red")
        do_pickle_ontology(filename, g)
        printDebug("----------\n...completed!", "important")

    # finally...
    return g





def action_import_folder(location):
    """Try to import all files from a local folder"""

    if os.path.isdir(location):
        onlyfiles = [ f for f in os.listdir(location) if os.path.isfile(os.path.join(location,f)) ]
        for file in onlyfiles:
            if not file.startswith("."):
                filepath = os.path.join(location,file)
                print(Fore.RED + "\n---------\n" + filepath + "\n---------" + Style.RESET_ALL)
                return action_import(filepath)
    else:
        printDebug("Not a valid directory", "important")
        return None





def action_webimport(hrlinetop=False):
    """ select from the available online directories for import """
    DIR_OPTIONS = {1 : "http://lov.okfn.org", 2 : "http://prefix.cc/popular/"}
    selection = None
    while True:
        if hrlinetop:
            printDebug("----------")
        text = "Please select which online directory to scan: (enter=quit)\n"
        for x in DIR_OPTIONS:
            text += "%d) %s\n" % (x, DIR_OPTIONS[x])
        var = input(text + "> ")
        if var == "q" or var == "":
            return None
        else:
            try:
                selection = int(var)
                test = DIR_OPTIONS[selection]  #throw exception if number wrong
                break
            except:
                printDebug("Invalid selection. Please try again.", "important")
                continue


    printDebug("----------")
    text = "Search for a specific keyword? (enter=show all)\n"
    var = input(text + "> ")
    keyword = var

    try:
        if selection == 1:
            _import_LOV(keyword=keyword)
        elif selection == 2:
            _import_PREFIXCC(keyword=keyword)
    except:
        printDebug("Sorry, the online repository seems to be unreachable.")

    return True



def _import_LOV(baseuri="http://lov.okfn.org/dataset/lov/api/v2/vocabulary/list", keyword=""):
    """
    2016-03-02: import from json list
    """

    printDebug("----------\nReading source... <%s>" % baseuri)
    query = requests.get(baseuri, params={})
    all_options = query.json()
    options = []

    # pre-filter if necessary
    if keyword:
        for x in all_options:
            if keyword in x['uri'].lower() or keyword in x['titles'][0]['value'].lower() or keyword in x['nsp'].lower():
                options.append(x)
    else:
        options = all_options

    printDebug("----------\n%d results found.\n----------" % len(options))

    if options:
        # display:
        counter = 1
        for x in options:
            uri, title, ns = x['uri'], x['titles'][0]['value'], x['nsp']
            # print("%s ==> %s" % (d['titles'][0]['value'], d['uri']))

            print(Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + uri + " ==> ", Fore.RED + title, Style.RESET_ALL)

            counter += 1

        while True:
            var = input(Style.BRIGHT + "=====\nSelect ID to import: (q=quit)\n" + Style.RESET_ALL)
            if var == "q":
                break
            else:
                try:
                    _id = int(var)
                    ontouri = options[_id - 1]['uri']
                    print(Fore.RED + "\n---------\n" + ontouri + "\n---------" + Style.RESET_ALL)
                    action_import(ontouri)
                except:
                    print("Error retrieving file. Import failed.")
                    continue




def _import_PREFIXCC(keyword=""):
    """
    List models from web catalog (prefix.cc) and ask which one to import
    2015-10-10: originally part of main ontospy; now standalone only
    2016-06-19: eliminated dependency on extras.import_web
    """
    SOURCE = "http://prefix.cc/popular/all.file.vann"
    options = []

    printDebug("----------\nReading source...")
    g = Graph(SOURCE, verbose=False)

    for x in g.ontologies:
        if keyword:
            if keyword in unicode(x.prefix).lower() or keyword in unicode(x.uri).lower():
                options += [(unicode(x.prefix), unicode(x.uri))]
        else:
            options += [(unicode(x.prefix), unicode(x.uri))]

    printDebug("----------\n%d results found." % len(options))

    counter = 1
    for x in options:
        print(Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + x[0] + " ==> ", Fore.RED +	 x[1], Style.RESET_ALL)
        # print(Fore.BLUE + x[0], " ==> ", x[1])
        counter += 1

    while True:
        var = input(Style.BRIGHT + "=====\nSelect ID to import: (q=quit)\n" + Style.RESET_ALL)
        if var == "q":
            break
        else:
            try:
                _id = int(var)
                ontouri = options[_id - 1][1]
                print(Fore.RED + "\n---------\n" + ontouri + "\n---------" + Style.RESET_ALL)
                action_import(ontouri)
            except:
                print("Error retrieving file. Import failed.")
                continue








def action_bootstrap():
    """Bootstrap the local REPO with a few cool ontologies"""
    printDebug("The following ontologies will be imported:")
    printDebug("--------------")
    count = 0
    for s in BOOTSTRAP_ONTOLOGIES:
        count += 1
        print(count, "<%s>" % s)

    printDebug("--------------")
    printDebug("Note: this operation may take several minutes.")
    printDebug("Proceed? [Y/N]")
    var = input()
    if var == "y" or var == "Y":
        for uri in BOOTSTRAP_ONTOLOGIES:
            try:
                printDebug("--------------")
                action_import(uri, verbose=False)
            except:
                printDebug("OPS... An Unknown Error Occurred - Aborting Installation")
        printDebug("----------\n" + "Completed (note: you can load an ontology by typing `ontospy -l`)", "comment")
        return True
    else:
        printDebug("--------------")
        printDebug("Goodbye")
        return False








def action_visualize(args, save_gist, fromshell=False):
    """
    export model into another format eg html, d3 etc...
    <fromshell> : the local name is being passed from ontospy shell
    """

    from .viz import ask_visualization, run_viz, saveVizGithub, saveVizLocally

    # get argument
    if not(args):
        ontouri = action_listlocal()
        if ontouri:
            islocal = True
        else:
            raise SystemExit(1)
    elif fromshell:
        ontouri = args
        islocal = True
    else:
        ontouri = args[0]
        islocal = False


    # select a visualization
    viztype = ask_visualization()
    if viztype == "":
        return None
        # raise SystemExit, 1

    # get ontospy graph
    if islocal:
        g = get_pickled_ontology(ontouri)
        if not g:
            g = do_pickle_ontology(ontouri)
    else:
        g = Graph(ontouri)

    # viz DISPATCHER
    contents = run_viz(g, viztype, save_gist)


    # once viz contents are generated, save file locally or on github
    if save_gist:
        urls = saveVizGithub(contents, ontouri)
        printDebug("...documentation saved on GitHub:\n", "comment")
        # printDebug("----------")
        printDebug("Gist (source code)           :  " + urls['gist'], "important")
        printDebug("Gist (interactive)           :  " + urls['blocks'], "important")
        printDebug("Gist (interactive+fullscreen):  " + urls['blocks_fullwin'], "important")
        url = urls['blocks'] # defaults to full win
    else:
        url = saveVizLocally(contents)
        printDebug("...documentation generated!\n[%s]" % url, "comment")

    return url










#
# ACTIONS ASSOCIATED TO MANAGER COMMAND
#






def action_update_library_location(_location):
    """
    Sets the folder that contains models for the local library
    @todo: add options to move things over etc..
    note: this is called from 'manager'
    """

    # if not(os.path.exists(_location)):
    # 	os.mkdir(_location)
    # 	printDebug("Creating new folder..", "comment")


    printDebug("Old location: '%s'" % get_home_location(), "comment")

    if os.path.isdir(_location):

        config = SafeConfigParser()
        config_filename = ONTOSPY_LOCAL + '/config.ini'
        config.read(config_filename)
        if not config.has_section('models'):
            config.add_section('models')

        config.set('models', 'dir', _location)
        with open(config_filename, 'w') as f:
            config.write(f) # note: this does not remove previously saved settings

        return _location
    else:
        return None






def actions_delete():
    """
    delete an ontology from the local repo
    """

    filename = action_listlocal()

    ONTOSPY_LOCAL_MODELS = get_home_location()

    if filename:
        fullpath = ONTOSPY_LOCAL_MODELS + filename

        if os.path.exists(fullpath):
            var = input("Are you sure you want to delete this file? (y/n)")
            if var == "y":
                os.remove(fullpath)
                printDebug("Deleted %s" % fullpath, "important")
                cachepath = ONTOSPY_LOCAL_CACHE + filename + ".pickle"
                # @todo: do this operation in /cache...
                if os.path.exists(cachepath):
                    os.remove(cachepath)
                    printDebug("---------")
                    printDebug("File deleted [%s]" % cachepath, "important")

                return True
            else:
                printDebug("Goodbye")

    return False






def action_erase():
    """just a wrapper.. possibly to be extended in the future"""
    get_or_create_home_repo(reset=True)
    return True




def action_cache():
    """
    generate cached version of all graphs in the local repo
    :return: True
    """
    printDebug("""The existing cache will be erased and recreated.""")
    printDebug("""This operation may take several minutes, depending on how many files exist in your local library.""")
    ONTOSPY_LOCAL_MODELS = get_home_location()

    var = input(Style.BRIGHT + "=====\nProceed? (y/n) " + Style.RESET_ALL)
    if var == "y":
        repo_contents = get_localontologies()
        print(Style.BRIGHT + "\n=====\n%d ontologies available in the local library\n=====" % len(repo_contents) + Style.RESET_ALL)
        for onto in repo_contents:
            fullpath = ONTOSPY_LOCAL_MODELS + "/" + onto
            try:
                print(Fore.RED + "\n=====\n" + onto + Style.RESET_ALL)
                print("Loading graph...")
                g = Graph(fullpath)
                print("Loaded ", fullpath)
            except:
                g = None
                print("Error parsing file. Please make sure %s contains valid RDF." % fullpath)

            if g:
                print("Caching...")
                do_pickle_ontology(onto, g)

        print(Style.BRIGHT + "===Completed===" + Style.RESET_ALL)

    else:
        print("Goodbye")






