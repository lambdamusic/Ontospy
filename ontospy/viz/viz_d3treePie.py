# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import *
import json



# TEMPLATE: D3 TREE PIE
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
	ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "d3_treePie.html", "r")
	t = Template(ontotemplate.read())

	c_total = len(graph.classes)
	c_toplayer = len(graph.toplayer)

	mydict = build_D3treepie(0, 99, 1, graph.toplayer)

	# JSON_DATA_CLASSES = json.dumps({'children': mylist, 'name': 'owl:Thing',})
	JSON_DATA_CLASSES = json.dumps(["owl:Thing", [c_toplayer, c_toplayer], mydict])

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




def build_D3treepie(old, MAX_DEPTH, level=1, toplayer=None):
	"""
	Create the JSON needed by the treePie viz
	http://bl.ocks.org/adewes/4710330/94a7c0aeb6f09d681dbfdd0e5150578e4935c6ae

	Eg

	['origin' , [n1, n2],
			{ 'name1' :
				['name1', [n1, n2],
					{'name1-1' : ...}
				] ,
			} ,
	]

	"""
	d = {}
	if not old:
		old = toplayer
	for x in old:
		label = x.bestLabel(quotes=False).replace("_", " ")
		if x.children() and level < MAX_DEPTH:
			size = len(x.children())
			d[x.qname] = [label, [size, size],
						  build_D3treepie(x.children(), MAX_DEPTH, level + 1)]
		else:
			size = 1
			d[x.qname] = [label, [size, size], {}]

	return d



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

