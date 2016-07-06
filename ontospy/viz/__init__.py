# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# VIZ MODULE : util to visualize an ontology as html or similar
#
#



from .. import ontospy
from ..core.util import *


# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass



# django loading requires different steps based on version
# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django

if django.get_version() > '1.7':
    from django.conf import settings
    from django.template import Context, Template

    settings.configure()
    django.setup()
    settings.TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # insert your TEMPLATE_DIRS here
                ontospy.ONTOSPY_VIZ_TEMPLATES + "shared",
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






# ===========
# MAIN CATALOGUE
# ===========
# @todo modify here in order to add new viz

from .viz_html import run as html
from .viz_d3tree import run as tree
# from .viz_d3packHierarchy import run as packH
# from .viz_d3bubblechart import run as bubble
# from .viz_d3cluster import run as cluster
# from .viz_d3barHierarchy import run as barH
# from .viz_d3partitionTable import run as partitionT
# from .viz_d3treePie import run as treeP


VISUALIZATIONS_LIST =  [("JavaDoc", html)]
VISUALIZATIONS_LIST += [("Dendogram", tree)]
# VISUALIZATIONS_LIST += [("Pack Hierarchy (experimental)", packH)]
# VISUALIZATIONS_LIST += [("Bubble Chart (experimental)", bubble)]
# VISUALIZATIONS_LIST += [("Cluster Tree (experimental)", cluster)]
# VISUALIZATIONS_LIST += [("Bar Hierarchy (experimental)", barH)]
# VISUALIZATIONS_LIST += [("Partition Table (experimental)", partitionT)]
# VISUALIZATIONS_LIST += [("Tree Pie (buggy)", treeP)]

# ============
# =END CATALOGUE
# ============





def ask_visualization():
    """
    ask user which viz output to use
    """
    while True:
        text = "Please select an output format for the ontology visualization: (q=quit)\n"
        for viz in VISUALIZATIONS_LIST:
            text += "%d) %s\n" % (VISUALIZATIONS_LIST.index(viz) + 1, viz[0])
        var = input(text + ">")
        if var == "q":
            return ""
        else:
            try:
                n = int(var) - 1
                test = VISUALIZATIONS_LIST[n]  # throw exception if number wrong
                return n
            except:
                printDebug("Invalid selection. Please try again.", "important")
                continue




# ===========
# DYNAMIC RUNNER FUN
# ===========

def run_viz(g, viz_index, save_gist):
    """
    Main fun calling the visualizations

    Note: dependent on VISUALIZATIONS_LIST

    :param g: graph instance
    :param viztype: a number passed from the user
    :param save_gist: a flag (just to extra info printed on template)
    :return: string contents of html file (the viz)
    """
    contents = VISUALIZATIONS_LIST[viz_index][1](g, save_gist)
    return contents






def saveVizLocally(contents, filename="index.html"):
    filename = ontospy.ONTOSPY_LOCAL_VIZ + "/" + filename

    f = open(filename, 'wb')
    f.write(contents)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

    url = "file://" + filename
    return url


def saveVizGithub(contents, ontouri):
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


def run_test_viz(func):
    """
    2016-06-20: wrapper for command line usage
    # script for testing - must launch as module for each viz eg
    # >python -m ontospy.viz.viz_packh
    """

    import webbrowser, random
    ontouri = ontospy.get_localontologies()[random.randint(0, 10)]  # [0]
    print("Testing with URI: %s" % ontouri)

    g = ontospy.get_pickled_ontology(ontouri)
    if not g:
        g = ontospy.do_pickle_ontology(ontouri)

    # getting main func dynamically
    contents = func(g, False)

    url = saveVizLocally(contents)
    if url:  # open browser
        import webbrowser
        webbrowser.open(url)

    return True
