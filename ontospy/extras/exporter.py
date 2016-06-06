# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


# EXPORTER.PY : util to visualize an ontology as html or similar


import time, optparse, sys, webbrowser

from .. import ontospy
from ..core.util import *

import json
# django loading requires different steps based on version
# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django
if django.get_version() > '1.7':
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()
	django.setup()
	settings.TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [
	            # insert your TEMPLATE_DIRS here
	            ontospy.ONTOSPY_LOCAL_TEMPLATES + "components",
	        ],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
	                # list if you haven't customized them:
	                'django.contrib.auth.context_processors.auth',
	                'django.template.context_processors.debug',
	                'django.template.context_processors.i18n',
	                'django.template.context_processors.media',
	                'django.template.context_processors.static',
	                'django.template.context_processors.tz',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]

else:
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()





MODULE_VERSION = 0.2


# manually edited
RENDER_OPTIONS = [
	(1, "Plain HTML (W3C docs style)"),
	(2, "Interactive javascript tree (D3 powered)"),
]






# TEMPLATE: HTML BASIC



def htmlBasicTemplate(graph, save_on_github=False):
	"""
	From a graph instance outputs a nicely formatted html documentation file.
	2015-10-21: mainly used with w3c template

	Django templates API: https://docs.djangoproject.com/en/dev/ref/templates/api/

	output = string

	2016-02-24: added <save_on_github>
	"""

	try:
		ontology = graph.ontologies[0]
		uri = ontology.uri
	except:
		ontology = None
		uri = graph.graphuri

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_LOCAL_TEMPLATES + "html/index.html", "r")

	t = Template(ontotemplate.read())


	c = Context({
					"ontology": ontology,
					"main_uri" : uri,
					"classes": graph.classes,
					"objproperties": graph.objectProperties,
					"dataproperties": graph.datatypeProperties,
					"annotationproperties": graph.annotationProperties,
					"skosConcepts": graph.skosConcepts,
					"instances": []
				})

	rnd = t.render(c)

	return _safe_str(rnd)









# TEMPLATE: D3 INTERACTIVE TREE


def interactiveD3Tree(graph, save_on_github=False):
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
		uri = graph.graphuri

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_LOCAL_TEMPLATES + "d3tree/d3tree.html", "r")

	t = Template(ontotemplate.read())

	c_mylist = _buildJSON_standardTree(graph.toplayer, MAX_DEPTH=99)
	c_total = len(graph.classes)

	p_mylist = _buildJSON_standardTree(graph.toplayerProperties, MAX_DEPTH=99)
	p_total = len(graph.properties)

	s_mylist = _buildJSON_standardTree(graph.toplayerSkosConcepts, MAX_DEPTH=99)
	s_total = len(graph.skosConcepts)

	# hack to make sure that we have a default top level object
	JSON_DATA_CLASSES = json.dumps({'children' : c_mylist, 'name' : 'OWL:Thing', 'id' : "None" })
	JSON_DATA_PROPERTIES = json.dumps({'children' : p_mylist, 'name' : 'Properties', 'id' : "None" })
	JSON_DATA_CONCEPTS = json.dumps({'children' : s_mylist, 'name' : 'Concepts', 'id' : "None" })


	c = Context({
					"ontology": ontology,
					"main_uri" : uri,
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
					"STATIC_PATH" : ontospy.ONTOSPY_LOCAL_TEMPLATES + "components/libs/" ,
				})

	rnd = t.render(c)

	return _safe_str(rnd)









# ===========
# Utilities
# ===========





def _safe_str(u, errors="replace"):
    """Safely print the given string.

    If you want to see the code points for unprintable characters then you
    can use `errors="xmlcharrefreplace"`.
	http://code.activestate.com/recipes/576602-safe-print/
    """
    s = u.encode(sys.stdout.encoding or "utf-8", errors)
    return s





def _buildJSON_standardTree(old, MAX_DEPTH, level=1):
	"""
	  For d3s viz like the expandable tree
	  all we need is a json with name, children and size .. eg

	  {
	 "name": "flare",
	 "children": [
	  {
	   "name": "analytics",
	   "children": [
		{
		 "name": "cluster",
		 "children": [
		  {"name": "AgglomerativeCluster", "size": 3938},
		  {"name": "CommunityStructure", "size": 3812},
		  {"name": "HierarchicalCluster", "size": 6714},
		  {"name": "MergeEdge", "size": 743}
		 ]
		},
		etc...
	"""
	out = []
	for x in old:
		d = {}
		# print "*" * level, x.label
		d['name'] = x.bestLabel()
		d['id'] = x.id
		# d['size'] = x.npgarticlestot or 10	 # setting 10 as default size
		if x.children() and level < MAX_DEPTH:
			d['children'] = _buildJSON_standardTree(x.children(), MAX_DEPTH, level+1)
		out += [d]

	return out











def _askVisualization():
	"""
	ask user which viz output to use
	"""
	while True:
		text = "Please select an output format for the ontology visualization: (q=quit)\n"
		for viz in RENDER_OPTIONS:
			text += "%d) %s\n" % (viz[0], viz[1])
		var = raw_input(text + ">")
		if var == "q":
			return None
		else:
			try:
				n = int(var)
				test = RENDER_OPTIONS[n-1]  #throw exception if number wrong
				return n
			except:
				printDebug("Invalid selection. Please try again.", "important")
				continue



def saveVizLocally(contents, filename = "index.html"):
	filename = ontospy.ONTOSPY_LOCAL_VIZ + "/" + filename

	f = open(filename,'w')
	f.write(contents) # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call it

	url = "file:///" + filename
	return url




def saveVizGithub(contents, ontouri):
	title = "OntoSpy: ontology export"
	readme = """This ontology documentation was automatically generated with OntoSpy (https://github.com/lambdamusic/OntoSpy).
	The graph URI is: %s""" % str(ontouri)
	files = {
	    'index.html' : {
	        'content': contents
	        },
	    'README.txt' : {
	        'content': readme
	        },
	    'LICENSE.txt' : {
	        'content': """The MIT License (MIT)

Copyright (c) 2016 OntoSpy project [http://ontospy.readthedocs.org/]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
	        }
	    }
	urls = save_anonymous_gist(title, files)
	return urls






def generateViz(graph, visualization):
	"""
	<visualization>: an integer mapped to the elements of RENDER_OPTIONS
	"""

	if visualization == 1:
		contents = render.htmlBasicTemplate(graph)

	elif visualization == 2:
		contents = render.interactiveD3Tree(graph)

	return contents






