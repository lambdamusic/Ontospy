# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import *
import json

from .utils import build_D3treeStandard


# TEMPLATE: D3 PACK HIERARCHY
# http://mbostock.github.io/d3/talk/20111116/pack-hierarchy.html
# https://github.com/d3/d3/wiki/Pack-Layout
# http://bl.ocks.org/nilanjenator/4950148



# ===========
# June 20, 2016 : notes
# ===========
# ....



def run(graph, save_on_github=False, main_entity=None ):
	"""
	"""
	try:
		ontology = graph.ontologies[0]
		uri = ontology.uri
	except:
		ontology = None
		uri = ";".join([s for s in graph.sources])

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "d3_packHierarchy.html", "r")
	t = Template(ontotemplate.read())

	jsontree_classes = build_D3treeStandard(0, 99, 1, graph.toplayer)
	c_total = len(graph.classes)


	if len(graph.toplayer) == 1:
		# the first element can be the single top level
		JSON_DATA_CLASSES = json.dumps(jsontree_classes[0])
	else:
		# hack to make sure that we have a default top level object
		JSON_DATA_CLASSES = json.dumps({'children': jsontree_classes, 'name': 'owl:Thing',})

	c = Context({
					"ontology": ontology,
					"main_uri" : uri,
					"STATIC_PATH": ONTOSPY_VIZ_STATIC,
					"save_on_github" : save_on_github,
					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
					"TOTAL_CLASSES": c_total,
				})

	rnd = t.render(c)

	return safe_str(rnd)











if __name__ == '__main__':
	import sys
	try:
		# script for testing - must launch this module
		# >python -m viz.viz_packh

		func = locals()["run"] # main func dynamically
		run_test_viz(func)

		sys.exit(0)

	except KeyboardInterrupt as e: # Ctrl-C
		raise e

