#!/usr/bin/env python
# encoding: utf-8



from .. import ontospy 
from .util import *

try:
	# https://docs.djangoproject.com/en/dev/ref/templates/api/
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()	
except:
	raise Exception("Cannot find the django library.")
	
	


def djangoTemplate(graph):
	""" 
	From an RDF file this outputs a nicely formatted html table. 
	NOTE: Customized for the nature.com/ontologies portal.
	2015-10-14: imported for testing...
	"""
	
	o = graph.ontologies[0]
	
	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_LOCAL_TEMPLATES + "template1.html", "r")
	
	t = Template(ontotemplate.read())

	metadata = []
	if o.annotations:
		for a in o.annotations:
			if type(a[1]) == rdflib.term.Literal:
				metadata += [(a[0], "\"%s\"" % a[1])]
			else:
				metadata += [(a[0], a[1])]
			
	c = Context({	
					"metadata": metadata,
					"classes": graph.classes,
					"objproperties": graph.objectProperties,
					"dataproperties": graph.datatypeProperties,
					"annotationproperties": graph.annotationProperties,
					"instances": []
				})
	
	rnd = t.render(c) 

	return rnd
	
	
	
	

def ontologyHtmlTree(graph, element = None):
	""" 
	outputs a recursive html tree representation 

	EG:
	<ul id="example" class="filetree">
			<li><span class="folder">Folder 2</span>
					<ul>
							<li><span class="folder">Subfolder 2.1</span>
									<ul>
											<li><span class="file">File 2.1.1</span></li>
											<li><span class="file">File 2.1.2</span></li>
									</ul>
							</li>
							<li><span class="file">File 2.2</span></li>
					</ul>
			</li>
			<li class="closed"><span class="folder">Folder 3 (closed at start)</span></li>
			<li><span class="file">File 4</span></li>
	</ul>

	"""
	if not element:
		children = graph.toplayer
	else:
		children = element.children()
	stringa = "<ul>"
	for x in children:
		# print x
		stringa += "<li>%s" % uri2niceString(x.uri, graph.namespaces)
		stringa += ontologyHtmlTree(graph, x)
		stringa += "</li>"
	stringa += "</ul>"
	return stringa


