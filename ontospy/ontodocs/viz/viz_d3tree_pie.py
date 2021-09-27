# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


# ===========
# D3 TREE PIE
#
# NOT IN USE  / NEEDS MORE TESTING
# ===========







import os, sys
import json

from ..utils import *
from ..builder import *  # loads and sets up Django
from ..viz_factory import VizFactory



class Dataviz(VizFactory):
    """
	D3 TREE PIE

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

        jsontree_classes = build_D3treepie(0, 99, 1,
                                           self.ontospy_graph.toplayer_classes)
        c_total = len(self.ontospy_graph.all_classes)
        c_toplayer = len(self.ontospy_graph.toplayer_classes)

        # weird - DBCheck!
        JSON_DATA_CLASSES = json.dumps(
            ["owl:Thing", [c_toplayer, c_toplayer], jsontree_classes])

        extra_context = {
            "ontograph": self.ontospy_graph,
            "TOTAL_CLASSES": c_total,
            'JSON_DATA_CLASSES': JSON_DATA_CLASSES,
        }

        # Ontology - MAIN PAGE
        contents = self._renderTemplate(
            "d3/d3_treepie.html", extraContext=extra_context)
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

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
