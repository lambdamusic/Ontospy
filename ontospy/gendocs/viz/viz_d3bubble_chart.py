# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

import os, sys
import json

from ..utils import *
from ..actions import * 
from ..viz_factory import VizFactory

# ===========
# D3 BUBBLE CHART
# ===========


class Dataviz(VizFactory):
    """
    D3 Bubbles

    """

    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(Dataviz, self).__init__(ontospy_graph, title)
        self.static_files = ["libs/d3-v3", "libs/jquery"]

    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        c_total = len(self.ontospy_graph.all_classes)
        p_total = len(self.ontospy_graph.all_properties)
        s_total = len(self.ontospy_graph.all_skos_concepts)

        main_url = None

        if c_total:
            c_mylist = build_D3bubbleChart(0, 99, 1,
                                            self.ontospy_graph.toplayer_classes)
            # hack to make sure that we have a default top level object
            JSON_DATA_CLASSES = json.dumps({
                'children': c_mylist,
                'name': 'owl:Thing',
                'id': "None"
            })

            extra_context = {
                "ontograph": self.ontospy_graph,
                "thispage": "classes",
                "TOTAL_CLASSES": c_total,
                "TOTAL_PROPERTIES": p_total,
                "TOTAL_CONCEPTS": s_total,
                "TOTAL_OBJECTS": c_total,
                "TOTAL_OBJECTS_TOPLAYER": len(self.ontospy_graph.toplayer_classes),
                'JSON_DATA_OBJECTS': JSON_DATA_CLASSES,
            }

            # Classes - MAIN PAGE
            contents = self._renderTemplate(
                "d3/d3_bubble_chart.html", extraContext=extra_context)
            
            if not main_url: 
                FILE_NAME = "index.html"
                main_url = self._save2File(contents, FILE_NAME, self.output_path)
            else:
                FILE_NAME = "classes.html"
                self._save2File(contents, FILE_NAME, self.output_path)
            


        if p_total:
            p_mylist = build_D3bubbleChart(0, 99, 1,
                                            self.ontospy_graph.toplayer_properties)
            JSON_DATA_PROPERTIES = json.dumps({
                'children': p_mylist,
                'name': 'Properties',
                'id': "None"
            })

            extra_context = {
                "ontograph": self.ontospy_graph,
                "thispage": "properties",
                "TOTAL_CLASSES": c_total,
                "TOTAL_PROPERTIES": p_total,
                "TOTAL_CONCEPTS": s_total,
                "TOTAL_OBJECTS": p_total,
                "TOTAL_OBJECTS_TOPLAYER": len(self.ontospy_graph.toplayer_properties),
                'JSON_DATA_OBJECTS': JSON_DATA_PROPERTIES,
            }

            # Properties PAGE
            contents = self._renderTemplate(
                "d3/d3_bubble_chart.html", extraContext=extra_context)
            
            if not main_url: 
                FILE_NAME = "index.html"
                main_url = self._save2File(contents, FILE_NAME, self.output_path)
            else:
                FILE_NAME = "properties.html"
                self._save2File(contents, FILE_NAME, self.output_path)
            

        if s_total:
            s_mylist = build_D3bubbleChart(0, 99, 1,
                                            self.ontospy_graph.toplayer_skos)
            JSON_DATA_CONCEPTS = json.dumps({
                'children': s_mylist,
                'name': 'Concepts',
                'id': "None"
            })

            extra_context = {
                "ontograph": self.ontospy_graph,
                "thispage": "concepts",
                "TOTAL_CLASSES": c_total,
                "TOTAL_PROPERTIES": p_total,
                "TOTAL_CONCEPTS": s_total,
                "TOTAL_OBJECTS": s_total,
                "TOTAL_OBJECTS_TOPLAYER": len(self.ontospy_graph.toplayer_skos),
                'JSON_DATA_OBJECTS': JSON_DATA_CONCEPTS,
            }

            # Concepts PAGE
            contents = self._renderTemplate(
                "d3/d3_bubble_chart.html", extraContext=extra_context)

            if not main_url: 
                FILE_NAME = "index.html"
                main_url = self._save2File(contents, FILE_NAME, self.output_path)
            else:
                FILE_NAME = "skos.html"
                self._save2File(contents, FILE_NAME, self.output_path)

        return main_url
        


# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = Dataviz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
