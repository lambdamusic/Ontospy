# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# TEST TEST TEST TEST TES
#
#



# from .. import *
from ..core.utils import *
from ..core.manager import *

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

else:
    from django.conf import settings
    from django.template import Context, Template


import os
from shutil import copyfile

try:
    from .CONFIG import VISUALIZATIONS_LIST
    
    VISUALIZATIONS_LIST = VISUALIZATIONS_LIST['Visualizations']
except:  # Mother of all exceptions
    click.secho("Visualizations configuration file not found.", fg="red")
    raise



# @TODO

"""
- Visualizer class may return the basic scaffolding for all other visualizations
    - eg header, footer, top level index.html
    - page containing high level stats about the ontology
    - maybe pages with common serializations too?
- then other viz eg d3 would reuse Visualizer
    - eg even if you have 1 only viz, you'd have all of the above each time
    - with exceptions eg Markdown
    
    
Visualizer() = reusable methods etc
    Scaffolding() = basic boostrap page, header, footer and stats
        ++ icons for subpages, which must be known
        .. this ideally goes at top level, but user decides that
    HTMLVisualizer() = eg the single page view
        .. goes at first level or second level, but user decides that by passing path
        .. if second level, normally you'd instantiate Scaffolding first
    D3TreeVisualizer() = eg the d3 view

.. running visualizer could be a way to run Scaffolding, plus all the others?

IDEA: each Visualizer should be self-contained (can be run by itself) but also easily pluggable under a scaffolding eg by passing output path etc..

MAYBE call them all 'RENDERER' or 'TRANSFORMER' 
"""


class VizFactory(object):
    """
    2016-12-01: attempt to rationalize the dataviz functions

    """
    
    def __init__(self, ontospy_graph):
        self.title = 'Base Visualizer'
        self.ontospy_graph = ontospy_graph
        self.static_files = []
        self.final_url = None
        self.output_path = None
        self.template_name = ""
        self.main_file_name = ""
    
    def build(self, output_path=None):
        """method that should be inherited by all vis classes"""
        
        self.output_path = self.checkOutputPath(output_path)
        self._buildStaticFiles(self.output_path)
        self.final_url = self._buildTemplates()
        return self.final_url

    def _buildTemplates(self):
        """
        do all the things necessary to build the viz
        should be adapted to work for single-file viz, or multi-files etc.

        :param output_path:
        :return:
        """
        #  in this case we only have one
        ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + self.template_name, "r")
    
        t = Template(ontotemplate.read())
    
        c = Context({
            "STATIC_URL": "static/",
            "ontology": self.ontospy_graph.sources,
            "classes": self.ontospy_graph.classes,
            "objproperties": self.ontospy_graph.objectProperties,
            "dataproperties": self.ontospy_graph.datatypeProperties,
            "annotationproperties": self.ontospy_graph.annotationProperties,
            "skosConcepts": self.ontospy_graph.skosConcepts,
            "instances": []
        })
    
        rnd = t.render(c)
        contents = safe_str(rnd)
        # the main url used for opening viz
        f = self.main_file_name
        main_url = self._save2File(contents, f, self.output_path)
        return main_url

    def _buildStaticFiles(self, static_folder="static"):
        """ move over static files so that relative imports work """
        static_path = os.path.join(self.output_path, static_folder)
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        for x in self.static_files:
            source_f = os.path.join(ONTOSPY_VIZ_STATIC, x)
            dest_f = os.path.join(static_path, x)
            copyfile(source_f, dest_f)
    
    def preview(self):
        if self.final_url:
            import webbrowser
            webbrowser.open(self.final_url)
        else:
            printDebug("Nothing to preview")
    
    def _save2File(self, contents, filename, path):
        filename = os.path.join(path, filename)
        f = open(filename, 'wb')
        f.write(contents)  # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it
        url = "file://" + filename
        return url
    
    def checkOutputPath(self, outputPath):
        if not outputPath:
            from os.path import expanduser
            home = expanduser("~")
            res = os.path.join(home, "ontospy-viz-test")
        if not os.path.exists(res):
            os.makedirs(res)
        return res





class HTMLVisualizer(VizFactory):
    """
    

    """


    def __init__(self, ontospy_graph):
        """
        Init
        """
        super(HTMLVisualizer, self).__init__(ontospy_graph)
        self.template_name = "javadoc.html"
        self.main_file_name = "index.html"






import zipfile
import os
import shutil

class TopLevelScaffolding(VizFactory):
    """

    """

    def __init__(self, ontospy_graph):
        """
        Init
        """
        super(TopLevelScaffolding, self).__init__(ontospy_graph)
        self.template_name = "komplete/index.html"
        self.main_file_name = "index.html"
        self.static_files = ["static_komplete.zip" ]

    # OVERRIDING THIS METHOD
    def _buildStaticFiles(self, static_folder=""):
        """ move over static files so that relative imports work """
        static_path = os.path.join(self.output_path, static_folder)
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        for x in self.static_files:
            source_f = os.path.join(ONTOSPY_VIZ_STATIC, x)
            dest_f = os.path.join(static_path, x)
            copyfile(source_f, dest_f)

 
        print("..unzipping")
        zip_ref = zipfile.ZipFile(os.path.join(static_path, "static_komplete.zip"), 'r')
        zip_ref.extractall(static_path)
        zip_ref.close()


        print("..cleaning up")
        os.remove(os.path.join(static_path, "static_komplete.zip"))
        # http://superuser.com/questions/104500/what-is-macosx-folder
        shutil.rmtree(os.path.join(static_path, "__MACOSX"))
        # shutil.rmtree(static_path + "__MACOSX")















if __name__ == '__main__':
    import sys
    
    try:
    
        uri, g = get_random_ontology()
        
        v = TopLevelScaffolding(g)
        v.build()
        v.preview()
        
        sys.exit(0)
    
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

