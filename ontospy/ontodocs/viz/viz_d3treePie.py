# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


import os, sys
import json

from ..core import *
from ..core.utils import *
from ..core.builder import *  # loads and sets up Django
from ..core.viz_factory import VizFactory




# ===========
# D3 TREE PIE
# ===========




class D3TreePieViz(VizFactory):
	"""
	D3 TREE PIE

	"""


	def __init__(self, ontospy_graph, title=""):
		"""
		Init
		"""
		super(D3TreePieViz, self).__init__(ontospy_graph, title)
		self.static_files = ["libs/d3-v3", "libs/jquery"]


	def _buildTemplates(self):
		"""
		OVERRIDING THIS METHOD from Factory
		"""

		jsontree_classes = build_D3treepie(0, 99, 1, self.ontospy_graph.toplayer_classes)
		c_total = len(self.ontospy_graph.all_classes)
		c_toplayer = len(self.ontospy_graph.toplayer_classes)

		# weird - DBCheck!
		JSON_DATA_CLASSES = json.dumps(["owl:Thing", [c_toplayer, c_toplayer], jsontree_classes])

		extra_context = {
						"ontograph": self.ontospy_graph,
						"TOTAL_CLASSES": c_total,
						'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
						}

		# Ontology - MAIN PAGE
		contents = self._renderTemplate("d3/d3_treePie.html", extraContext=extra_context)
		FILE_NAME = "index.html"
		main_url = self._save2File(contents, FILE_NAME, self.output_path)

		return main_url




# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

	TEST_ONLINE = False
	try:

		g = get_onto_for_testing(TEST_ONLINE)

		v = D3TreePieViz(g, title="")
		v.build()
		v.preview()

		sys.exit(0)

	except KeyboardInterrupt as e:  # Ctrl-C
		raise e













#
#
#
# def run(graph, save_on_github=False, main_entity=None):
# 	"""
# 	"""
# 	try:
# 		ontology = graph.all_ontologies[0]
# 		uri = ontology.uri
# 	except:
# 		ontology = None
# 		uri = ";".join([s for s in graph.sources])
#
# 	# ontotemplate = open("template.html", "r")
# 	ontotemplate = open(ONTODOCS_VIZ_TEMPLATES + "d3_treePie.html", "r")
# 	t = Template(ontotemplate.read())
#
# 	c_total = len(graph.classes)
# 	c_toplayer = len(graph.toplayer_classes)
#
# 	mydict = build_D3treepie(0, 99, 1, graph.toplayer_classes)
#
# 	# JSON_DATA_CLASSES = json.dumps({'children': mylist, 'name': 'owl:Thing',})
# 	JSON_DATA_CLASSES = json.dumps(["owl:Thing", [c_toplayer, c_toplayer], mydict])
#
# 	c = Context({
# 					"ontology": ontology,
# 					"main_uri" : uri,
# 					"STATIC_PATH": ONTODOCS_VIZ_STATIC,
# 					"save_on_github" : save_on_github,
# 					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
# 					"TOTAL_CLASSES": c_total,
# 				})
#
# 	rnd = t.render(c)
#
# 	return safe_str(rnd)
#
#
#
#
# def build_D3treepie(old, MAX_DEPTH, level=1, toplayer=None):
# 	"""
# 	Create the JSON needed by the treePie viz
# 	http://bl.ocks.org/adewes/4710330/94a7c0aeb6f09d681dbfdd0e5150578e4935c6ae
#
# 	Eg
#
# 	['origin' , [n1, n2],
# 			{ 'name1' :
# 				['name1', [n1, n2],
# 					{'name1-1' : ...}
# 				] ,
# 			} ,
# 	]
#
# 	"""
# 	d = {}
# 	if not old:
# 		old = toplayer
# 	for x in old:
# 		label = x.bestLabel(quotes=False).replace("_", " ")
# 		if x.children() and level < MAX_DEPTH:
# 			size = len(x.children())
# 			d[x.qname] = [label, [size, size],
# 						  build_D3treepie(x.children(), MAX_DEPTH, level + 1)]
# 		else:
# 			size = 1
# 			d[x.qname] = [label, [size, size], {}]
#
# 	return d
#
#
#
# if __name__ == '__main__':
# 	import sys
# 	try:
# 		# script for testing - must launch this module
# 		# >python -m viz.viz_packh
#
# 		func = locals()["run"] # main func dynamically
# 		run_test_viz(func)
#
# 		sys.exit(0)
#
# 	except KeyboardInterrupt as e: # Ctrl-C
# 		raise e
