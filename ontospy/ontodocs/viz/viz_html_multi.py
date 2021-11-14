# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# ==================
# VIZ HTML MULTI - html visualization with multiple files, one per entity
# ==================

import os, sys
import json

from ..utils import *
from ..builder import *  # loads and sets up Django
from ..viz_factory import VizFactory





class KompleteViz(VizFactory):
    """

    """


    def __init__(self, ontospy_graph, title="", theme=""):
        """
        Init
        """
        super(KompleteViz, self).__init__(ontospy_graph, title)
        self.static_files = [
                "custom",
                "libs/bootswatch3_2",
                "libs/bootstrap-3_3_7-dist",
                "libs/jquery/1_12_4/",
                "libs/chartjs-2_4_0"
                ]
        self.theme = validate_theme(theme)

    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """
        # INDEX - MAIN PAGE
        contents = self._renderTemplate("html-multi/index.html", extraContext={"theme": self.theme, "index_page_flag" : True})
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        # DASHBOARD
        contents = self._renderTemplate("html-multi/statistics.html", extraContext={"theme": self.theme})
        FILE_NAME = "statistics.html"
        self._save2File(contents, FILE_NAME, self.output_path)

        browser_output_path = self.output_path

        # ENTITIES A-Z
        extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme}
        contents = self._renderTemplate("html-multi/browser/browser_entities_az.html", extraContext=extra_context)
        FILE_NAME = "entities-az.html"
        self._save2File(contents, FILE_NAME, browser_output_path)



        if self.ontospy_graph.all_classes:
            # CLASSES = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "classes",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyClassTree())}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-classes.html"
            self._save2File(contents, FILE_NAME, browser_output_path)
            # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.all_classes:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "class",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_classinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.all_properties:

            # PROPERTIES = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "properties",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyPropTree())}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-properties.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - PROPERTIES ======

            for entity in self.ontospy_graph.all_properties:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "property",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_propinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.all_skos_concepts:

            # CONCEPTS = ENTITIES TREE

            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "concepts",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyConceptTree())}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-concepts.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - CONCEPTS ======

            for entity in self.ontospy_graph.all_skos_concepts:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "concept",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_conceptinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.all_shapes:

            # SHAPES = ENTITIES TREE

            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "shapes", 'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyShapeTree()) }
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-shapes.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - SHAPES ======

            for entity in self.ontospy_graph.all_shapes:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "shape",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_shapeinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)



        if self.ontospy_graph.all_individuals:

            # INDIVIDUALS (FLAT) TREE

            extra_context = {
                    "ontograph": self.ontospy_graph, 
                    "theme": self.theme,
                    "treetype" : "individuals",
                    'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyIndividualsTree())}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-individuals.html"
            self._save2File(contents, FILE_NAME, browser_output_path)
            
            # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.all_individuals:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "individual",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate(
                        "html-multi/browser/browser_individualinfo.html",
                        extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        return main_url




class KompleteVizMultiModel(KompleteViz):
    """
    Specialized version that supports customizing where the static url / folder are.

    The idea is to pass a location which can be shared by multiple html outputs. (eg multiple html-complex ontology folders)

    eg

    python -m ontospy.viz.scripts.export_all -o ~/Desktop/test2/ --theme random
    """


    def __init__(self, ontospy_graph, title="", theme="", static_url="", output_path_static=""):
        """
        Init
        """
        super(KompleteVizMultiModel, self).__init__(ontospy_graph, title, theme)
        self.static_files = ["custom", "libs"]
        self.theme = validate_theme(theme)
        self.static_url = static_url  # eg "../static"
        self.output_path_static = output_path_static  # eg full path to a top level
        # note: the following serves to make sure self.static_url is passed correctly
        self.basic_context_data = self._build_basic_context()






# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = KompleteViz(g, title="", theme=random_theme())
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
