#!/usr/bin/env python
# encoding: utf-8

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
		



def _safe_str(u, errors="replace"):
    """Safely print the given string.
    
    If you want to see the code points for unprintable characters then you
    can use `errors="xmlcharrefreplace"`.
	http://code.activestate.com/recipes/576602-safe-print/
    """
    s = u.encode(sys.stdout.encoding or "utf-8", errors)
    return s
	


	
	


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
			

	

