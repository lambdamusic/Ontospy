# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# VIZ MARKDOWN
#
#



from .. import *
from ..core.utils import *
from ..core.manager import *

from .utils import *
from .viz_factory import VizFactory

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

# django loading requires different steps based on version
# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django

# http://stackoverflow.com/questions/1714027/version-number-comparison
from distutils.version import StrictVersion

if StrictVersion(django.get_version()) > StrictVersion('1.7'):
    from django.conf import settings
    from django.template import Context, Template

else:
    from django.conf import settings
    from django.template import Context, Template


import os, sys
import json



class D3TreeViz(VizFactory):
    """
    D3 viz tree

    """


    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(D3TreeViz, self).__init__(ontospy_graph, title)
        self.static_files = ["libs/d3-v2", "libs/jquery"]


    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """


        c_mylist = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayer)
        p_mylist = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayerProperties)
        s_mylist = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayerSkosConcepts)

        c_total = len(self.ontospy_graph.classes)
        p_total = len(self.ontospy_graph.properties)
        s_total = len(self.ontospy_graph.skosConcepts)


        if False:
            # testing how a single tree would look like
            JSON_DATA_CLASSES = json.dumps(
            {'children' :
                [ {'children' : c_mylist, 'name' : 'Classes', 'id' : "classes" },
                {'children' : p_mylist, 'name' : 'Properties', 'id' : "properties" },
                {'children' : s_mylist, 'name' : 'Concepts', 'id' : "concepts" }],
                'name' : 'Entities', 'id' : "root"
                }
                )

        # hack to make sure that we have a default top level object
        JSON_DATA_CLASSES = json.dumps({'children' : c_mylist, 'name' : 'owl:Thing', 'id' : "None" })
        JSON_DATA_PROPERTIES = json.dumps({'children' : p_mylist, 'name' : 'Properties', 'id' : "None" })
        JSON_DATA_CONCEPTS = json.dumps({'children' : s_mylist, 'name' : 'Concepts', 'id' : "None" })

    #
	# c = Context({
	# 				"ontology": ontology,
	# 				"main_uri" : uri,
	# 				"STATIC_PATH": ONTOSPY_VIZ_STATIC,
	# 				"save_on_github" : save_on_github,
	# 				"classes": graph.classes,
	# 				"classes_TOPLAYER": len(graph.toplayer),
	# 				"properties": graph.properties,
	# 				"properties_TOPLAYER": len(graph.toplayerProperties),
	# 				"skosConcepts": graph.skosConcepts,
	# 				"skosConcepts_TOPLAYER": len(graph.toplayerSkosConcepts),
	# 				"TOTAL_CLASSES": c_total,
	# 				"TOTAL_PROPERTIES": p_total,
	# 				"TOTAL_CONCEPTS": s_total,
	# 				'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
	# 				'JSON_DATA_PROPERTIES' : JSON_DATA_PROPERTIES,
	# 				'JSON_DATA_CONCEPTS' : JSON_DATA_CONCEPTS,
	# 			})
    #
    #

        extra_context = {
                        "ontograph": self.ontospy_graph,
    					"TOTAL_CLASSES": c_total,
    					"TOTAL_PROPERTIES": p_total,
    					"TOTAL_CONCEPTS": s_total,
    					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
    					'JSON_DATA_PROPERTIES' : JSON_DATA_PROPERTIES,
    					'JSON_DATA_CONCEPTS' : JSON_DATA_CONCEPTS,
                        }

        # Ontology - MAIN PAGE
        contents = self._renderTemplate("misc/d3tree.html", extraContext=extra_context)
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        return main_url




# if called directly, for testing purposes run the basic HTML rendering

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        if TEST_ONLINE:
            from ..core.ontospy import Ontospy
            g = Ontospy("http://cohere.open.ac.uk/ontology/cohere.owl#")
        else:
            uri, g = get_random_ontology(50)

        v = D3TreeViz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
