# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# VIZ MODULE : util to visualize an ontology as html or similar
#
#

import os
from ..core.utils import *
from .. import *

_dirname, _filename = os.path.split(os.path.abspath(__file__))
ONTODOCS_VIZ_TEMPLATES = _dirname + "/media/templates/"
ONTODOCS_VIZ_STATIC = _dirname + "/media/static/"


try:
    from .CONFIG import VISUALIZATIONS_LIST, BOOTSWATCH_THEMES, BOOTSWATCH_THEME_DEFAULT
    VISUALIZATIONS_LIST = VISUALIZATIONS_LIST['Visualizations']
except:  # Mother of all exceptions
    printDebug("Visualizations configuration file not found.", fg="red")
    raise


def show_types():
    for n, t in enumerate(VISUALIZATIONS_LIST):
        printInfo("%d. %s" % (n + 1, t['Title']), "green")
    printInfo("Note: select a viz type by using its numerical index.",
               "comment")

def show_themes():
    for t in BOOTSWATCH_THEMES:
        printInfo(t, "green")


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
    printDebug(
        "Please choose an output format for the ontology visualization: (q=quit)\n",
        "important")
    while True:
        text = ""
        for viz in VISUALIZATIONS_LIST:
            text += "%d) %s\n" % (VISUALIZATIONS_LIST.index(viz) + 1,
                                  viz['Title'])
        var = input(text + ">")
        if var == "q":
            return ""
        else:
            try:
                n = int(var) - 1
                test = VISUALIZATIONS_LIST[
                    n]  # throw exception if number wrong
                return n
            except:
                printDebug("Invalid selection. Please try again.", "red")
                continue


def select_visualization(n):
    """
    get viz choice based on numerical index
    """
    try:
        n = int(n) - 1
        test = VISUALIZATIONS_LIST[n]  # throw exception if number wrong
        return n
    except:
        printDebug("Invalid viz-type option. Valid options are:", "red")
        show_types()
        raise SystemExit(1)


# ===========
# VIZ SELECTION FUNCTION
# ===========


def build_visualization(g, viz_index, path=None, title="", theme=""):
    """
    2017-01-20: new verion, less clever but also simpler
    """

    this_viz = VISUALIZATIONS_LIST[viz_index]

    if this_viz['ID'] == "html-simple":
        from .viz.viz_html_single import HTMLVisualizer
        v = HTMLVisualizer(g, title)

    elif this_viz['ID'] == "html-complex":
        from .viz.viz_html_multi import KompleteViz
        v = KompleteViz(g, title, theme)

    elif this_viz['ID'] == "markdown":
        from .viz.viz_markdown import MarkdownViz
        v = MarkdownViz(g, title)

    elif this_viz['ID'] == "d3-dendogram":
        from .viz.viz_d3dendogram import Dataviz
        v = Dataviz(g, title)

    elif this_viz['ID'] == "d3-bubble-chart":
        from .viz.viz_d3bubble_chart import Dataviz
        v = Dataviz(g, title)

    elif this_viz['ID'] == "d3-pack-hierarchy":
        from .viz.viz_d3pack_hierarchy import Dataviz
        v = Dataviz(g, title)

    elif this_viz['ID'] == "d3-bar-hierarchy":
        from .viz.viz_d3bar_hierarchy import Dataviz
        v = Dataviz(g, title)

    elif this_viz['ID'] == "d3-partition-table":
        from .viz.viz_d3partition_table import Dataviz
        v = Dataviz(g, title)

    elif this_viz['ID'] == "d3-rotating-cluster":
        from .viz.viz_d3rotating_cluster import Dataviz
        v = Dataviz(g, title)

    elif this_viz['ID'] == "sigma-force-directed":
        from .viz.viz_sigmajs import Dataviz
        v = Dataviz(g, title)

    else:
        return False

    url = v.build(path)

    return url


# ?LEGACY


def saveVizGithub(contents, ontouri):
    """
    DEPRECATED on 2016-11-16
    Was working but had a dependecies on package 'uritemplate.py' which caused problems at installation time
    """
    title = "Ontospy: ontology export"
    readme = """This ontology documentation was automatically generated with Ontospy (https://github.com/lambdamusic/Ontospy).
	The graph URI is: %s""" % str(ontouri)
    files = {
        'index.html': {
            'content': contents
        },
        'README.txt': {
            'content': readme
        },
        'LICENSE.txt': {
            'content':
            """The MIT License (MIT)

Copyright (c) 2016 Ontospy project [http://lambdamusic.github.io/Ontospy/]

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
