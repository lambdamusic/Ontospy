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




class Visualizer(object):
    """
    2016-12-01: attempt to rationalize the dataviz functions

    """

    def __repr__(self):
        return "<OntoSpy: Visualizer object>"

    def __init__(self, ontospy_graph):
        self.title = 'title'
        self.ontospy_graph = ontospy_graph
        self.static_files = []
        self.final_url = None
        self.template_name = "javadoc.html"

        from os.path import expanduser
        home = expanduser("~")
        self.path_default = os.path.join(home, "ontospy-viz-test")
        if not os.path.exists(self.path_default):
            os.makedirs(self.path_default)

    def build(self, templates=[], filename="index.html", output_path=None):
        if not output_path:
            output_path = self.path_default
        self._copyStaticFiles(output_path)
        contents = self._render()
        self.final_url = self._saveVizLocally(contents, filename, output_path)
      
    def preview(self):
        if self.final_url:
            import webbrowser
            webbrowser.open(self.final_url)


    def _render(self):
        ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + self.template_name, "r")
    
        t = Template(ontotemplate.read())
    
        c = Context({
            "ontology": self.ontospy_graph.sources,
            "classes": self.ontospy_graph.classes,
            "objproperties": self.ontospy_graph.objectProperties,
            "dataproperties": self.ontospy_graph.datatypeProperties,
            "annotationproperties": self.ontospy_graph.annotationProperties,
            "skosConcepts": self.ontospy_graph.skosConcepts,
            "instances": []
        })
    
        rnd = t.render(c)
        return safe_str(rnd)


    def _saveVizLocally(self, contents, filename, path):
        filename = os.path.join(path, filename)
        f = open(filename, 'wb')
        f.write(contents)  # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it
        url = "file://" + filename
        return url
    
    def _copyStaticFiles(self, output_path, static_folder="static"):
        """ move over static files so that relative imports work """
        static_path = os.path.join(output_path, static_folder)
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        for x in self.static_files:
            source_f = os.path.join(ONTOSPY_VIZ_STATIC, x)
            dest_f = os.path.join(static_path, x)
            copyfile(source_f, dest_f)





# eg subclassing [UNUSED]
class VisualizerBasicRdf(Visualizer):
    
    def __init__(self, title, ontospy_graph, static_files=[]):
        """
        Init
        """
        super(Visualizer, self).__init__(title, ontospy_graph, static_files)






if __name__ == '__main__':
    import sys
    
    try:
    
        uri, g = get_random_ontology()
        v = Visualizer(g)
        v.build()
        v.preview()
        
        sys.exit(0)
    
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

