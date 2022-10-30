# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# ==================
# VIZ SIGMA JS
# ==================


import os, sys
import json

from ..utils import *
from ..actions import * 
from ..viz_factory import VizFactory





class Dataviz(VizFactory):
    """
    Sigma JS

    """


    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(Dataviz, self).__init__(ontospy_graph, title)
        self.static_files = ["libs/sigma", "libs/jquery"]


    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        c_mydict = build_class_json(self.ontospy_graph.all_classes)
        JSON_DATA_CLASSES = json.dumps(c_mydict)


        extra_context = {
                        "ontograph": self.ontospy_graph,
                        'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
                        }

        # Ontology - MAIN PAGE
        contents = self._renderTemplate("sigma/sigmajs.html", extraContext=extra_context)
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        return main_url




import random

def _classColor(x):
    if not x.parents():
        return "#FFD8DD"
    elif not x.children():
        return "#C4F5FF"
    else:
        return "#C8FFB3"

def build_class_json(classes):
    nodes = [{
                    "id": "owlthing",
                    "label": "owl:Thing",
                    "x": random.random(),
                    "y": random.random(),
                    "color" : "grey",
                    "size": 5
                }]
    edges = []
    for x in classes:
        temp = {
                    "id": x.id,
                    "label": x.bestLabel(quotes=False),
                    "x": random.random(),
                    "y": random.random(),
                    "color" : _classColor(x),
                    "size": len(x.descendants()) or 1
                }
        nodes.append(temp)

        if not x.parents():
            # add a relationship to OWL THING
            edges.append({
                "id": "%s-%s" % (x.id, "owlthing"),
                "source": "owlthing",
                "target": x.id,
                "color": '#ccc',
                "hover_color": '#000'
            })

        for el in x.children():
            temp2 = {
                "id": "%s-%s" % (x.id, el.id),
                "source": x.id,
                "target": el.id,
                 # "type": 'curve',
                "color": '#ccc',
                "hover_color": '#000'
            }
            edges.append(temp2)

    result = {
            "nodes": nodes ,
            "edges" : edges,
        }

    return result





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


