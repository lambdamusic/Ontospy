# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

import os, sys
import json

from ..core import *
from ..core.utils import *
from ..core.builder import *  # loads and sets up Django
from ..core.viz_factory import VizFactory






# TEMPLATE: D3 PACK HIERARCHY
# http://mbostock.github.io/d3/talk/20111116/pack-hierarchy.html
# https://github.com/d3/d3/wiki/Pack-Layout
# http://bl.ocks.org/nilanjenator/4950148





class D3PackHierarchyViz(VizFactory):
    """
    D3 PackHierarchyViz

    """


    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(D3PackHierarchyViz, self).__init__(ontospy_graph, title)
        self.static_files = ["libs/d3-v3", "libs/jquery"]


    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        jsontree_classes = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayer_classes)
        c_total = len(self.ontospy_graph.all_classes)


        if len(self.ontospy_graph.toplayer_classes) == 1:
            # the first element can be the single top level
            JSON_DATA_CLASSES = json.dumps(jsontree_classes[0])
        else:
            # hack to make sure that we have a default top level object
            JSON_DATA_CLASSES = json.dumps({'children': jsontree_classes, 'name': 'owl:Thing',})


        extra_context = {
                        "ontograph": self.ontospy_graph,
    					"TOTAL_CLASSES": c_total,
    					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
                        }

        # Ontology - MAIN PAGE
        contents = self._renderTemplate("d3/d3_packHierarchy.html", extraContext=extra_context)
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        return main_url




# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = D3PackHierarchyViz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
