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
	


	
	


# MAIN TEMPLATES: BASIC W3C
	
	

def htmlBasicTemplate(graph):
	""" 
	From a graph instance outputs a nicely formatted html documentation file. 
	2015-10-21: mainly used with w3c template
	
	Django templates API: https://docs.djangoproject.com/en/dev/ref/templates/api/
	
	output = string
	"""
	
	try:
		ontology = graph.ontologies[0]
	except:
		ontology = None
	
	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_LOCAL_TEMPLATES + "html/index.html", "r")
	
	t = Template(ontotemplate.read())

	
	c = Context({	
					"ontology": ontology,
					"classes": graph.classes,
					"objproperties": graph.objectProperties,
					"dataproperties": graph.datatypeProperties,
					"annotationproperties": graph.annotationProperties,
					"skosConcepts": graph.skosConcepts,
					"instances": []
				})
	
	rnd = t.render(c) 

	return _safe_str(rnd)
	








# MAIN TEMPLATES: INTERACTIVE TREE


def interactiveD3Tree(graph, entity="classes"):
	""" 
	2015-10-30: d3 tree
	
	<graph> : an ontospy graph
	<entity> : flag to determine which entity tree to display
	
	output = string
	"""
	
	try:
		ontology = graph.ontologies[0]
	except:
		ontology = None
	
	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_LOCAL_TEMPLATES + "d3tree/index.html", "r")
	
	t = Template(ontotemplate.read())
	
	if entity == "classes":
		mylist = _buildJSON_standardTree(graph.toplayer, MAX_DEPTH=99)
		total = len(graph.classes)
	elif entity == "properties":
		mylist = _buildJSON_standardTree(graph.toplayerProperties, MAX_DEPTH=99)
		total = len(graph.properties)
	elif entity == "skos":
		mylist = _buildJSON_standardTree(graph.toplayerSkosConcepts, MAX_DEPTH=99)
		total = len(graph.skosConcepts)
	
	# hack to make sure that we have a default top level object
	mydict = {'children' : mylist, 'name' : 'Entities'}
		
	JSON_DATA = json.dumps(mydict)
	

	c = Context({	
					"ontology": ontology,
					"total_entities": total, 
					'JSON_DATA' : JSON_DATA,
					"STATIC_PATH" : ontospy.ONTOSPY_LOCAL_TEMPLATES + "d3tree/" ,
				})
	
	rnd = t.render(c) 

	return _safe_str(rnd)
	




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
		# d['size'] = x.npgarticlestot or 10	 # setting 10 as default size
		if x.children() and level < MAX_DEPTH:
			d['children'] = _buildJSON_standardTree(x.children(), MAX_DEPTH, level+1)
		out += [d]
	
	return out
			

	
	


	
#
# def ontologyHtmlTree(graph, element = None):
# 	"""
# 	2015-10-21: not used
# 	outputs a recursive html tree representation
#
# 	EG:
# 	<ul id="example" class="filetree">
# 			<li><span class="folder">Folder 2</span>
# 					<ul>
# 							<li><span class="folder">Subfolder 2.1</span>
# 									<ul>
# 											<li><span class="file">File 2.1.1</span></li>
# 											<li><span class="file">File 2.1.2</span></li>
# 									</ul>
# 							</li>
# 							<li><span class="file">File 2.2</span></li>
# 					</ul>
# 			</li>
# 			<li class="closed"><span class="folder">Folder 3 (closed at start)</span></li>
# 			<li><span class="file">File 4</span></li>
# 	</ul>
#
# 	"""
# 	if not element:
# 		children = graph.toplayer
# 	else:
# 		children = element.children()
# 	stringa = "<ul>"
# 	for x in children:
# 		# print x
# 		stringa += "<li>%s" % uri2niceString(x.uri, graph.namespaces)
# 		stringa += ontologyHtmlTree(graph, x)
# 		stringa += "</li>"
# 	stringa += "</ul>"
# 	return stringa


