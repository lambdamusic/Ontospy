

# # ===========
# September 29, 2014: testing an onto docs generation library
# ===========


import rdflib
from rdflib.namespace import FOAF, OWL, RDF, RDFS

from ontospy import *

try:
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()
	# https://docs.djangoproject.com/en/dev/ref/templates/api/
except:
	print "Please install the django library first."
	raise


o = Ontology("test/npg2014-09-05.owl")


ontotemplate = open("htmltemplates/ontotemplate.html", "r")	

t = Template(ontotemplate.read())

c = Context({"classes": [o.classRepresentation(c) for c in o.allclasses]})
rnd = t.render(c) 


output = open("output_ontodocs.html", "w")
output.write(rnd)
output.close()