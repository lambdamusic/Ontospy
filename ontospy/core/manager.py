# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *
import random

from colorama import Fore, Style

# ===========
#
# Ontospy management utils
#
# ===========


def get_or_create_home_repo(reset=False):
    """
    Check to make sure we never operate with a non-existing local repo
    """
    dosetup = True
    if os.path.exists(ONTOSPY_LOCAL):
        dosetup = False

        if reset:
            import shutil
            var = input(
                "Delete the local library and all of its contents? (y/n) ")
            if var == "y":
                shutil.rmtree(ONTOSPY_LOCAL)
                dosetup = True
            else:
                pass

    if dosetup or not (os.path.exists(ONTOSPY_LOCAL)):
        os.mkdir(ONTOSPY_LOCAL)
    if dosetup or not (os.path.exists(ONTOSPY_LOCAL_CACHE)):
        # print "HERE"
        os.makedirs(ONTOSPY_LOCAL_CACHE)
    if dosetup or not (os.path.exists(ONTOSPY_LIBRARY_DEFAULT)):
        os.mkdir(ONTOSPY_LIBRARY_DEFAULT)

    LIBRARY_HOME = get_home_location()  # from init file, or default

    # check that the local library folder exists, otherwise prompt user to create it
    if not (os.path.exists(LIBRARY_HOME)):
        printDebug(
            "Warning: the local library at '%s' has been deleted or is not accessible anymore."
            % LIBRARY_HOME, "important")
        printDebug(
            "Please reset the local library by running 'ontospy-manager -u <a-valid-path>'",
            "comment")
        raise SystemExit(1)

    if dosetup:
        print(Fore.GREEN + "Setup successfull: local library created at <%s>" %
              LIBRARY_HOME + Style.RESET_ALL)
    # else:
    # print(Style.DIM + "Local library: <%s>" % LIBRARY_HOME + Style.RESET_ALL)

    return True


def get_home_location():
    """Gets the path of the local library folder
    :return - a string e.g. "/users/mac/ontospy"
    """
    config = SafeConfigParser()
    config_filename = ONTOSPY_LOCAL + '/config.ini'

    if not os.path.exists(config_filename):
        config_filename = 'config.ini'

    config.read(config_filename)
    try:
        _location = config.get('models', 'dir')
        if _location.endswith("/"):
            return _location
        else:
            return _location + "/"
    except:
        # FIRST TIME, create it
        config.add_section('models')
        config.set('models', 'dir', ONTOSPY_LIBRARY_DEFAULT)
        with open(config_filename, 'w') as f:
            # note: this does not remove previously saved settings
            config.write(f)

        return ONTOSPY_LIBRARY_DEFAULT


def get_localontologies(pattern=""):
    "returns a list of file names in the ontologies folder (not the full path)"
    res = []
    ONTOSPY_LOCAL_MODELS = get_home_location()
    if os.path.exists(ONTOSPY_LOCAL_MODELS):
        for f in os.listdir(ONTOSPY_LOCAL_MODELS):
            if os.path.isfile(os.path.join(ONTOSPY_LOCAL_MODELS, f)):
                if not f.startswith(".") and not f.endswith(".pickle"):
                    if not pattern:
                        res += [f]
                    else:
                        if pattern in f:
                            res += [f]
    return res


def get_random_ontology(TOP_RANGE=10, pattern=""):
    """for testing purposes. Returns a random ontology/graph"""
    choices = get_localontologies(pattern=pattern)
    try:
        ontouri = choices[random.randint(0, TOP_RANGE)]  # [0]
    except:
        ontouri = choices[0]
    print("Testing with URI: %s" % ontouri)
    g = get_pickled_ontology(ontouri)
    if not g:
        g = do_pickle_ontology(ontouri)
    return ontouri, g


def get_pickled_ontology(filename):
    """ try to retrieve a cached ontology """
    pickledfile = os.path.join(ONTOSPY_LOCAL_CACHE, filename + ".pickle")
    # pickledfile = ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
    if GLOBAL_DISABLE_CACHE:
        printDebug(
            "WARNING: DEMO MODE cache has been disabled in __init__.py ==============",
            "red")
    if os.path.isfile(pickledfile) and not GLOBAL_DISABLE_CACHE:
        try:
            return cPickle.load(open(pickledfile, "rb"))
        except:
            print(Style.DIM +
                  "** WARNING: Cache is out of date ** ...recreating it... " +
                  Style.RESET_ALL)
            return None
    else:
        return None


def del_pickled_ontology(filename):
    """ 
    Remove a cached ontology based on related filename
    """
    pickledfile = os.path.join(ONTOSPY_LOCAL_CACHE, filename + ".pickle")
    # pickledfile = ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
    if os.path.isfile(pickledfile) and not GLOBAL_DISABLE_CACHE:
        os.remove(pickledfile)
        return True
    else:
        return None


def rename_pickled_ontology(filename, newname):
    """ try to rename a cached ontology """
    pickledfile = os.path.join(ONTOSPY_LOCAL_CACHE, filename + ".pickle")
    # pickledfile = ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
    newpickledfile = os.path.join(ONTOSPY_LOCAL_CACHE, newname + ".pickle")
    # newpickledfile = ONTOSPY_LOCAL_CACHE + "/" + newname + ".pickle"
    if os.path.isfile(pickledfile) and not GLOBAL_DISABLE_CACHE:
        os.rename(pickledfile, newpickledfile)
        return True
    else:
        return None


def do_pickle_ontology(filename, g=None):
    """
    from a valid filename, generate the graph instance and pickle it too
    note: option to pass a pre-generated graph instance too
    2015-09-17: added code to increase recursion limit if cPickle fails
        see http://stackoverflow.com/questions/2134706/hitting-maximum-recursion-depth-using-pythons-pickle-cpickle
    """
    ONTOSPY_LOCAL_MODELS = get_home_location()
    get_or_create_home_repo()  # ensure all the right folders are there
    pickledpath = os.path.join(ONTOSPY_LOCAL_CACHE, filename + ".pickle")
    # pickledpath = ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
    if not g:
        g = Ontospy(os.path.join(ONTOSPY_LOCAL_MODELS, filename))
        # g = Ontospy(ONTOSPY_LOCAL_MODELS + "/" + filename)

    if not GLOBAL_DISABLE_CACHE:
        try:
            cPickle.dump(g, open(pickledpath, "wb"))
            printDebug(".. cached <%s>" % filename, "green")
        except Exception as e:
            print(Style.DIM + "\n.. Failed caching <%s>" % filename +
                  Style.RESET_ALL)
            print(str(e) + "\n")
            print(
                Style.DIM +
                "... attempting to increase the recursion limit from %d to %d" %
                (sys.getrecursionlimit(), sys.getrecursionlimit() * 10) +
                Style.RESET_ALL)

            try:
                sys.setrecursionlimit(sys.getrecursionlimit() * 10)
                cPickle.dump(g, open(pickledpath, "wb"))
                printDebug(".. cached <%s>" % filename, "green")
            except Exception as e:
                printDebug(
                    "\n... Failed caching <%s>... Aborting caching operation..."
                    % filename, "error")
                print(str(e) + "\n")
            sys.setrecursionlimit(int(sys.getrecursionlimit() / 10))
    return g
