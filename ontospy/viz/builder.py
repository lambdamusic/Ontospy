# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# VIZ MODULE : util to visualize an ontology as html or similar
#
#



from .. import *
from ..core.utils import *
from ..core.manager import *
from ..core.actions import *

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

# django loading requires different steps based on version
# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django
import click

# http://stackoverflow.com/questions/1714027/version-number-comparison
from distutils.version import StrictVersion

if StrictVersion(django.get_version()) > StrictVersion('1.7'):
    from django.conf import settings
    from django.template import Context, Template

    settings.configure()
    django.setup()
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # insert your TEMPLATE_DIRS here
                ONTOSPY_VIZ_TEMPLATES + "html-simple",
                ONTOSPY_VIZ_TEMPLATES + "markdown",
                ONTOSPY_VIZ_TEMPLATES + "html-multi",
                ONTOSPY_VIZ_TEMPLATES + "misc",
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                    # list if you haven't customized them:
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

else:
    from django.conf import settings
    from django.template import Context, Template

    settings.configure()

import os
from shutil import copyfile

try:
    from .CONFIG import VISUALIZATIONS_LIST, BOOTSWATCH_THEMES, BOOTSWATCH_THEME_DEFAULT

    VISUALIZATIONS_LIST = VISUALIZATIONS_LIST['Visualizations']
except:  # Mother of all exceptions
    click.secho("Visualizations configuration file not found.", fg="red")
    raise



def show_themes():
    for t in BOOTSWATCH_THEMES:
        printDebug(t, "green")

def random_theme():
    return random.choice(BOOTSWATCH_THEMES)

def validate_theme(theme_try, default=BOOTSWATCH_THEME_DEFAULT):
    # print theme_try
    if not theme_try:
        return default
    if theme_try in BOOTSWATCH_THEMES:
        return theme_try
    else:
        printDebug("Warning: theme not found", "red")
        return default




def ask_visualization():
    """
    ask user which viz output to use
    """
    printDebug("Please choose an output format for the ontology visualization: (q=quit)\n", "important")
    while True:
        text = ""
        for viz in VISUALIZATIONS_LIST:
            text += "%d) %s\n" % (VISUALIZATIONS_LIST.index(viz) + 1, viz['Title'])
        var = input(text + ">")
        if var == "q":
            return ""
        else:
            try:
                n = int(var) - 1
                test = VISUALIZATIONS_LIST[n]  # throw exception if number wrong
                return n
            except:
                printDebug("Invalid selection. Please try again.", "red")
                continue




def action_visualize(args, fromshell=False, path=None, title="", theme="", verbose=False):
    """
    export model into another format eg html, d3 etc...
    <fromshell> : the local name is being passed from ontospy shell
    """

    # from ..viz import ask_visualization, build_viz, VISUALIZATIONS_LIST

    # get argument
    if not(args):
        ontouri = action_listlocal(all_details=False)
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

    # 2017-01-23: bypass pickled stuff as it has wrong counts etc..
    USE_CACHE = False
    # get ontospy graph
    if islocal and USE_CACHE:
        g = get_pickled_ontology(ontouri)
        if not g:
            g = do_pickle_ontology(ontouri)
    else:
        printDebug("Loading graph...", dim=True)
        if islocal:
            g = Ontospy(os.path.join(get_home_location(), ontouri), verbose=verbose)
        else:
            g = Ontospy(ontouri, verbose=verbose)

    # put in home folder by default: <ontouri>/<viztype>/files..
    if not path:
        from os.path import expanduser
        home = expanduser("~")
        onto_path = slugify(unicode(ontouri))
        viz_path = slugify(unicode(VISUALIZATIONS_LIST[viztype]['Title']))
        path = os.path.join(home, "ontospy-viz/" + onto_path + "/" + viz_path )
        if not os.path.exists(path):
            os.makedirs(path)

    # url  = build_viz(ontouri, g, viztype, path)
    printDebug("Building visualization...", dim=True)
    url  = build_visualization(ontouri, g, viztype, path, title, theme)

    return url



# ===========
# DYNAMIC RUNNER FUNCTION
# ===========


def build_visualization(ontouri, g, viz_index, path=None, title="", theme=""):
    """
    2017-01-20: new verion, less clever but also simpler

    :param g:
    :param viz_index:
    :param main_entity:
    :return:
    """

    this_viz = VISUALIZATIONS_LIST[viz_index]

    if this_viz['ID'] == "html-simple":
        from .viz_html_single import HTMLVisualizer
        v = HTMLVisualizer(g, title)

    elif this_viz['ID'] == "html-complex":
        from .viz_html_multi import KompleteViz
        v = KompleteViz(g, title, theme)

    elif this_viz['ID'] == "markdown":
        from .viz_markdown import MarkdownViz
        v = MarkdownViz(g, title)

    else:
        return False

    url = v.build(path)

    return url





# LEGACY LEGACY LEGACY

def build_viz(ontouri, g, viz_index, path=None):
    """

    :param g:
    :param viz_index:
    :param main_entity:
    :return:
    """

    this_viz = VISUALIZATIONS_LIST[viz_index]

    extension = "." + this_viz["File-extension"]

    import importlib
    module_name = this_viz['ID']
    viz_module = importlib.import_module(".viz_" + module_name, "ontospy.viz")
    VIZ_WORKER = viz_module.run  # dynamically referenced

    if this_viz['Type'] == "single-file":
        url = _buildSingleFile(ontouri, g, VIZ_WORKER, extension, path)

    elif this_viz['Type'] == "multi-file":
        url = _buildMultiFile(ontouri, g, VIZ_WORKER, extension, path)

    # save static files too
    if this_viz['Static-files']:
        _copyStaticFiles(this_viz['Static-files'], path)

    return url


def _buildSingleFile(ontouri, g, VIZ_WORKER, extension, path):
    # simple  viz DISPATCHER
    contents = VIZ_WORKER(g, False)
    # once viz contents are generated, save file locally or on github
    url = saveVizLocally(contents, slugify(unicode(ontouri)) + extension, path)
    printDebug("Documentation generated: <%s>" % url, "green")
    return url


def _buildMultiFile(ontouri, g, VIZ_WORKER, extension, path):
    """
    one file per entity in ontology
    """
    contents = VIZ_WORKER(g, False, None)
    index_url = saveVizLocally(contents, "index" + extension, path)

    entities = [g.classes, g.properties, g.skosConcepts]
    for group in entities:
        for c in group:
            # getting main func dynamically
            contents = VIZ_WORKER(g, False, c)
            _filename = c.slug + extension
            url = saveVizLocally(contents, _filename, path)

    url = index_url
    printDebug("Documentation generated: <%s>" % url, "green")
    return url


def _copyStaticFiles(files_list, path, folder="static"):
    """ move over static files so that relative imports work """
    static_path = os.path.join(path, folder)
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    for x in files_list:
        source_f = os.path.join(ONTOSPY_VIZ_STATIC, x)
        dest_f = os.path.join(static_path, x)
        copyfile(source_f, dest_f)



def saveVizLocally(contents, filename="index.html", path=None):
    if not path:
        filename = ONTOSPY_LOCAL_VIZ + "/" + filename
    else:
        filename = os.path.join(path, filename)

    f = open(filename, 'wb')
    f.write(contents)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

    url = "file://" + filename
    return url


def saveVizGithub(contents, ontouri):
    """
    DEPRECATED on 2016-11-16
    Was working but had a dependecies on package 'uritemplate.py' which caused problems at installation time
    """
    title = "OntoSpy: ontology export"
    readme = """This ontology documentation was automatically generated with OntoSpy (https://github.com/lambdamusic/OntoSpy).
	The graph URI is: %s""" % str(ontouri)
    files = {
        'index.html': {
            'content': contents
        },
        'README.txt': {
            'content': readme
        },
        'LICENSE.txt': {
            'content': """The MIT License (MIT)

Copyright (c) 2016 OntoSpy project [http://ontospy.readthedocs.org/]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
        }
    }
    urls = save_anonymous_gist(title, files)
    return urls


def run_test_viz(func, filename="index.html", path=None):
    """
    2016-06-20: wrapper for command line usage
    # script for testing - must launch as module for each viz eg
    # >python -m ontospy.viz.viz_packh
    """

    import webbrowser, random
    ontouri = get_localontologies()[random.randint(0, 10)]  # [0]
    print("Testing with URI: %s" % ontouri)

    g = get_pickled_ontology(ontouri)
    if not g:
        g = do_pickle_ontology(ontouri)

    # getting main func dynamically
    contents = func(g, False)

    url = saveVizLocally(contents, filename, path)
    if url:  # open browser
        import webbrowser
        webbrowser.open(url)

    return True
