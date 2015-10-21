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
	
	


def _safe_str(u, errors="replace"):
    """Safely print the given string.
    
    If you want to see the code points for unprintable characters then you
    can use `errors="xmlcharrefreplace"`.
	http://code.activestate.com/recipes/576602-safe-print/
    """
    s = u.encode(sys.stdout.encoding or "utf-8", errors)
    return s
	
	
	
	

def djangoTemplate(graph):
	""" 
	From a graph instance outputs a nicely formatted html documentation file. 
	2015-10-21: mainly used with w3c template
	
	output = string
	"""
	
	try:
		ontology = graph.ontologies[0]
	except:
		ontology = None
	
	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ontospy.ONTOSPY_LOCAL_TEMPLATES + "w3c/index.html", "r")
	
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
	
	
	


	

def ontologyHtmlTree(graph, element = None):
	""" 
	2015-10-21: not used
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


