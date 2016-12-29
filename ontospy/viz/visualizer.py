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


import zipfile
import os
import shutil


try:
    from .CONFIG import VISUALIZATIONS_LIST
    VISUALIZATIONS_LIST = VISUALIZATIONS_LIST['Visualizations']
except:  # Mother of all exceptions
    click.secho("Visualizations configuration file not found.", fg="red")
    raise



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
        home = os.path.expanduser("~")
        self.output_path_DEFAULT = os.path.join(home, "ontospy-viz-test")
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
        contents = self._renderTemplate(self.template_name, extraContext=None)
        # the main url used for opening viz
        f = self.main_file_name
        main_url = self._save2File(contents, f, self.output_path)
        return main_url


    def _renderTemplate(self, template_name, extraContext=None):
        """

        :param template_name: NOTE *relative* to templates folder
        :param extraContext: a dict that can be loaded on demand
        :return: the rendered template as a string
        """

        atemplate = open(self.templates_root + template_name, "r")
        t = Template(atemplate.read())
        context = self.get_basic_context()
        if extraContext and type(extraContext) == dict:
            context.update(extraContext)
        contents = safe_str(t.render(context))
        return contents


    def _buildStaticFiles(self, static_folder="static"):
        """ move over static files so that relative imports work
        Note: if a dir is passed, it is copied with all of its contents
        If the file is a zip, it is copied and extracted too
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
                if x.endswith('.zip'):
                    printDebug("..unzipping")
                    zip_ref = zipfile.ZipFile(os.path.join(dest_f), 'r')
                    zip_ref.extractall(static_path)
                    zip_ref.close()
                    printDebug("..cleaning up")
                    os.remove(dest_f)
                    # http://superuser.com/questions/104500/what-is-macosx-folder
                    shutil.rmtree(os.path.join(static_path, "__MACOSX"))



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
    
    def checkOutputPath(self, output_path):
        """
        Create or clean up output path
        """
        if not output_path:
            output_path = self.output_path_DEFAULT
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.makedirs(output_path)
        return output_path







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






class KompleteViz(VizFactory):
    """

    """

    def __init__(self, ontospy_graph):
        """
        Init
        """
        super(KompleteViz, self).__init__(ontospy_graph)
        self.static_files = ["static"]


    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        # DASHBOARD - MAIN PAGE
        contents = self._renderTemplate("komplete/dashboard.html", extraContext=None)
        FILE_NAME = "dashboard.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        # VIZ LIST
        contents = self._renderTemplate("komplete/viz_list.html", extraContext=None)
        FILE_NAME = "visualizations.html"
        self._save2File(contents, FILE_NAME, self.output_path)

        # BROWSER PAGES
        browser_output_path = self.output_path

        # ENTITIES A-Z
        extra_context = {"ontograph": self.ontospy_graph}
        contents = self._renderTemplate("komplete/browser/browser_entities_az.html", extraContext=extra_context)
        FILE_NAME = "entities-az.html"
        self._save2File(contents, FILE_NAME, browser_output_path)

        # ENTITIES TREE
        extra_context = {"ontograph": self.ontospy_graph}
        contents = self._renderTemplate("komplete/browser/browser_entities_tree.html", extraContext=extra_context)
        FILE_NAME = "entities-tree.html"
        self._save2File(contents, FILE_NAME, browser_output_path)

        for entity in self.ontospy_graph.classes:
            extra_context = {"main_entity": entity,
                            "main_entity_type": "class",
                            "ontograph": self.ontospy_graph
                            }
            contents = self._renderTemplate("komplete/browser/browser_classinfo.html", extraContext=extra_context)
            FILE_NAME = entity.slug + ".html"
            self._save2File(contents, FILE_NAME, browser_output_path)


        for entity in self.ontospy_graph.properties:
            extra_context = {"main_entity": entity,
                            "main_entity_type": "property",
                            "ontograph": self.ontospy_graph
                            }
            contents = self._renderTemplate("komplete/browser/browser_propinfo.html", extraContext=extra_context)
            FILE_NAME = entity.slug + ".html"
            self._save2File(contents, FILE_NAME, browser_output_path)

        for entity in self.ontospy_graph.skosConcepts:
            extra_context = {"main_entity": entity,
                            "main_entity_type": "concept",
                            "ontograph": self.ontospy_graph
                            }
            contents = self._renderTemplate("komplete/browser/browser_conceptinfo.html", extraContext=extra_context)
            FILE_NAME = entity.slug + ".html"
            self._save2File(contents, FILE_NAME, browser_output_path)


        # entities = [g.classes, g.properties, g.skosConcepts]
        # for group in entities:
        #     for c in group:
        #         # getting main func dynamically
        #         contents = func(g, False, c)
        #         _filename = c.slug + ".html"
        #         url = _saveVizLocally(contents, _filename, DEST_FOLDER)

        return main_url



if __name__ == '__main__':
    import sys
    
    try:
    
        uri, g = get_random_ontology()
        
        v = KompleteViz(g)
        v.build()
        v.preview()
        
        sys.exit(0)
    
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

