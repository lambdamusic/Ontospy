# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import *
import json
from .utils import build_D3treeStandard


# TEMPLATE: D3 ROTATING CLUSTER
# original source: ...



# ===========
# June 20, 2016 : notes
# ===========
# ....



def run(graph, save_on_github=False, main_entity=None):
	"""
	"""
	try:
		ontology = graph.ontologies[0]
		uri = ontology.uri
	except:
		ontology = None
		uri = ";".join([s for s in graph.sources])

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "d3_cluster.html", "r")
	t = Template(ontotemplate.read())

	c_total = len(graph.classes)

	mylist = build_D3treeStandard(0, 99, 1, graph.toplayer)

	JSON_DATA_CLASSES = json.dumps({'children': mylist, 'name': 'owl:Thing',})

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

