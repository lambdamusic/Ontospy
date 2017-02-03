# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import *
import json

from .utils import build_D3treeStandard


# TEMPLATE: D3 INTERACTIVE TREE

#
# ===========
# Comments:
# ===========
#






def run(graph, save_on_github=False, main_entity=None):
	"""
	2016-02-19: new version with tabbed or all trees in one page ##unfinished

	<graph> : an ontospy graph
	<entity> : flag to determine which entity tree to display

	output = string

	2016-02-24: added <save_on_github>
	"""

	try:
		ontology = graph.ontologies[0]
		uri = ontology.uri
	except:
		ontology = None
		uri = ";".join([s for s in graph.sources])

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "d3_tree.html", "r")

	t = Template(ontotemplate.read())

	c_mylist = build_D3treeStandard(0, 99, 1, graph.toplayer)
	p_mylist = build_D3treeStandard(0, 99, 1, graph.toplayerProperties)
	s_mylist = build_D3treeStandard(0, 99, 1, graph.toplayerSkosConcepts)

	c_total = len(graph.classes)
	p_total = len(graph.properties)
	s_total = len(graph.skosConcepts)

	# hack to make sure that we have a default top level object
	JSON_DATA_CLASSES = json.dumps({'children' : c_mylist, 'name' : 'owl:Thing', 'id' : "None" })
	JSON_DATA_PROPERTIES = json.dumps({'children' : p_mylist, 'name' : 'Properties', 'id' : "None" })
	JSON_DATA_CONCEPTS = json.dumps({'children' : s_mylist, 'name' : 'Concepts', 'id' : "None" })


	c = Context({
					"ontology": ontology,
					"main_uri" : uri,
					"STATIC_PATH": ONTOSPY_VIZ_STATIC,
					"save_on_github" : save_on_github,
					"classes": graph.classes,
					"classes_TOPLAYER": len(graph.toplayer),
					"properties": graph.properties,
					"properties_TOPLAYER": len(graph.toplayerProperties),
					"skosConcepts": graph.skosConcepts,
					"skosConcepts_TOPLAYER": len(graph.toplayerSkosConcepts),
					"TOTAL_CLASSES": c_total,
					"TOTAL_PROPERTIES": p_total,
					"TOTAL_CONCEPTS": s_total,
					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
					'JSON_DATA_PROPERTIES' : JSON_DATA_PROPERTIES,
					'JSON_DATA_CONCEPTS' : JSON_DATA_CONCEPTS,
				})

	rnd = t.render(c)

	return safe_str(rnd)










if __name__ == '__main__':
	import sys
	try:

		# script for testing - must launch this module
		# >python -m viz.viz_d3tree

		func = locals()["run"] # main func dynamically
		run_test_viz(func)

		sys.exit(0)

	except KeyboardInterrupt as e: # Ctrl-C
		raise e



