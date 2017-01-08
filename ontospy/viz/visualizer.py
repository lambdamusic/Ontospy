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

from .utils import *

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

from pygments import highlight
from pygments.lexers.rdf import TurtleLexer
from pygments.formatters import HtmlFormatter


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

    def __init__(self, ontospy_graph, title=""):
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
        self.title = title or self.infer_best_title()
        self.basic_context_data = self._build_basic_context()

    def infer_best_title(self):
        """Selects something usable as a title for an ontospy graph"""
        if self.ontospy_graph.ontologies:
            return self.ontospy_graph.ontologies[0].uri
        elif self.ontospy_graph.sources:
            return self.ontospy_graph.sources[0]
        else:
            return "Untitled"

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
        context = Context(self.basic_context_data)
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


    def _build_basic_context(self):
        """util to return a standard dict used in django as a template context"""
        # printDebug(str(self.ontospy_graph.toplayer))
        topclasses = self.ontospy_graph.toplayer[:]
        if len(topclasses) < 3: # massage the toplayer!
            for topclass in self.ontospy_graph.toplayer:
                for child in topclass.children():
                    if child not in topclasses: topclasses.append(child)

        context_data = {
            "STATIC_URL": "static/",
            "ontospy_version": VERSION,
            "ontospy_graph": self.ontospy_graph,
            "docs_title": self.title,
            "namespaces": self.ontospy_graph.namespaces,
            "stats": self.ontospy_graph.stats(),
            "ontologies": self.ontospy_graph.ontologies,
            "sources": self.ontospy_graph.sources,
            "classes": self.ontospy_graph.classes,
            "topclasses": topclasses,
            "objproperties": self.ontospy_graph.objectProperties,
            "dataproperties": self.ontospy_graph.datatypeProperties,
            "annotationproperties": self.ontospy_graph.annotationProperties,
            "skosConcepts": self.ontospy_graph.skosConcepts,
            "instances": []
        }

        return context_data


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


    def highlight_code(self, ontospy_entity):
        """
        produce an html version of Turtle code with syntax highlighted
        using Pygments CSS
        """
        try:
            pygments_code = highlight(ontospy_entity.serialize(), TurtleLexer(), HtmlFormatter())
            pygments_code_css = HtmlFormatter().get_style_defs('.highlight')
            return {"pygments_code": pygments_code,
                    "pygments_code_css": pygments_code_css
                            }
        except Exception as e:
            printDebug("Error: Pygmentize Failed", "red")
            return {}




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

    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(KompleteViz, self).__init__(ontospy_graph, title)
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


        browser_output_path = self.output_path

        # ENTITIES A-Z
        extra_context = {"ontograph": self.ontospy_graph}
        contents = self._renderTemplate("komplete/browser/browser_entities_az.html", extraContext=extra_context)
        FILE_NAME = "entities-az.html"
        self._save2File(contents, FILE_NAME, browser_output_path)



        if self.ontospy_graph.classes:
            # CLASSES = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "treetype" : "classes",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyClassTree())}
            contents = self._renderTemplate("komplete/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-classes.html"
            self._save2File(contents, FILE_NAME, browser_output_path)
            # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.classes:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "class",
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("komplete/browser/browser_classinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.properties:

            # PROPERTIES = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "treetype" : "properties",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyPropTree())}
            contents = self._renderTemplate("komplete/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-properties.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - PROPERTIES ======

            for entity in self.ontospy_graph.properties:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "property",
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("komplete/browser/browser_propinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.skosConcepts:

            # CONCEPTS = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "treetype" : "concepts",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyConceptTree())}
            contents = self._renderTemplate("komplete/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-concepts.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - CONCEPTS ======

            for entity in self.ontospy_graph.skosConcepts:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "concept",
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("komplete/browser/browser_conceptinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        return main_url



if __name__ == '__main__':
    import sys

    try:

        if True:
            uri, g = get_random_ontology(50, pattern="subjects")

        if False:
            from ..core.ontospy import Ontospy
            # g = Ontospy("http://cohere.open.ac.uk/ontology/cohere.owl#")
            g = Ontospy("/Users/michele.pasin/Dropbox/code/scigraph/knowledge-graph/models/ontologies/core")

        v = KompleteViz(g)
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
