# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# TEST TEST TEST TEST TES
#
#



from .. import *
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
import shutil

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
    Object encapsulating common methods for building HTML visualizations

    Subclass and override as needed.
    """
    
    def __init__(self, ontospy_graph):
        self.title = 'Base Visualizer'
        self.ontospy_graph = ontospy_graph
        self.static_files = []
        self.final_url = None
        self.output_path = None
        self.template_name = ""
        self.main_file_name = ""
        self.templates_root = ONTOSPY_VIZ_TEMPLATES
        self.static_root = ONTOSPY_VIZ_STATIC

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
        ontotemplate = open(self.templates_root + self.template_name, "r")
    
        t = Template(ontotemplate.read())
    
        c = self.get_basic_context()
    
        rnd = t.render(c)
        contents = safe_str(rnd)
        # the main url used for opening viz
        f = self.main_file_name
        main_url = self._save2File(contents, f, self.output_path)
        return main_url

    def _buildStaticFiles(self, static_folder="static"):
        """ move over static files so that relative imports work
        Note: if a dir is passed, it is copied with all of its contents
        """
        static_path = os.path.join(self.output_path, static_folder)
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        for x in self.static_files:
            source_f = os.path.join(self.static_root, x)
            dest_f = os.path.join(static_path, x)
            if os.path.isdir(source_f):
                if os.path.exists(dest_f):
                    # delete first if exists, as copytree will throw an error otherwise
                    shutil.rmtree(dest_f)
                shutil.copytree(source_f, dest_f)
            else:
                shutil.copyfile(source_f, dest_f)
    
    def preview(self):
        if self.final_url:
            import webbrowser
            webbrowser.open(self.final_url)
        else:
            printDebug("Nothing to preview")


    def get_basic_context(self):
        """util to return a standard context for a django template to render"""
        c = Context({
            "STATIC_URL": "static/",
            "ontospy_version": VERSION,
            "ontospy_graph": self.ontospy_graph,
            "namespaces": self.ontospy_graph.namespaces,
            "stats": self.ontospy_graph.stats(),
            "ontologies": self.ontospy_graph.ontologies,
            "sources": self.ontospy_graph.sources,
            "classes": self.ontospy_graph.classes,
            "objproperties": self.ontospy_graph.objectProperties,
            "dataproperties": self.ontospy_graph.datatypeProperties,
            "annotationproperties": self.ontospy_graph.annotationProperties,
            "skosConcepts": self.ontospy_graph.skosConcepts,
            "instances": []
        })
        return c


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




class BasicDashboard(VizFactory):
    """

    """

    def __init__(self, ontospy_graph):
        """
        Init
        """
        super(BasicDashboard, self).__init__(ontospy_graph)
        self.static_files = ["static"]

    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """


        ontotemplate_dashboard = open(self.templates_root + "komplete/dashboard.html", "r")
        FILE_NAME = "dashboard.html"
        t = Template(ontotemplate_dashboard.read())
        c = self.get_basic_context()
        rnd = t.render(c)
        contents = safe_str(rnd)
        main_url = self._save2File(contents, FILE_NAME, self.output_path)


        ontotemplate_vizlist = open(self.templates_root + "komplete/viz_list.html", "r")
        FILE_NAME = "visualizations.html"
        t = Template(ontotemplate_vizlist.read())
        c = self.get_basic_context()
        rnd = t.render(c)
        contents = safe_str(rnd)
        self._save2File(contents, FILE_NAME, self.output_path)

        return main_url


    #@todo add zip file logic to factory method (for dist release)
    # def NOT_buildStaticFiles(self, static_folder=""):
    #     """
    #     OVERRIDING THIS METHOD
    #     so that the zip file is extracted too
    #     """
    #     static_path = os.path.join(self.output_path, static_folder)
    #     if not os.path.exists(static_path):
    #         os.makedirs(static_path)
    #     for x in self.static_files:
    #         source_f = os.path.join(self.static_root, x)
    #         dest_f = os.path.join(static_path, x)
    #         shutil.copyfile(source_f, dest_f)
    #
    #     print("..unzipping")
    #     zip_ref = zipfile.ZipFile(os.path.join(static_path, "static_komplete.zip"), 'r')
    #     zip_ref.extractall(static_path)
    #     zip_ref.close()
    #
    #     print("..cleaning up")
    #     os.remove(os.path.join(static_path, "static_komplete.zip"))
    #     # http://superuser.com/questions/104500/what-is-macosx-folder
    #     shutil.rmtree(os.path.join(static_path, "__MACOSX"))
    #     # shutil.rmtree(static_path + "__MACOSX")
    #



if __name__ == '__main__':
    import sys
    
    try:
    
        uri, g = get_random_ontology()
        
        v = BasicDashboard(g)
        v.build()
        v.preview()
        
        sys.exit(0)
    
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

