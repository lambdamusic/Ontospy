# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# ===========
# PYTHON SCRIPT THAT GENERATES AN HTML TABLE FROM AN RDF ONTOLOGY FILE.
#
# Dependencies: rdflib; ontospy; django.
#
# Installation:
#	a) install package manager https://pip.pypa.io/en/latest/installing.html
#	b) pip install [rdflib, ontospy, django]
#
#
# USAGE
# python ontodocs.py /path/to/somefile.rdf > output.html
# ===========



try:
	# https://docs.djangoproject.com/en/dev/ref/templates/api/
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()
except:
	raise Exception("Cannot find the django library.")

try:
	import rdflib
except:
	raise Exception("Cannot find the rdflib library.")

try:
	from ontospy.ontospy import *
except:
	raise Exception("Cannot find the ontospy library.")





def generate_html_table(afile):
	"""
	From an RDF file this outputs a nicely formatted html table.
	NOTE: Customized for the nature.com/ontologies portal.
	"""

	o = Ontology(afile)

	ontotemplate = open("template.html", "r")

	t = Template(ontotemplate.read())

	metadata = []
	for a in o.ontologyAnnotations():
		if type(a[1]) == rdflib.term.Literal:
			metadata += [(a[0], "\"%s\"" % a[1])]
		else:
			metadata += [(a[0], a[1])]

	c = Context({
					"metadata": metadata,
					"classes": [o.classRepresentation(c) for c in o.allclasses],
					"objproperties": [o.propertyRepresentation(c) for c in o.allobjproperties],
					"dataproperties": [o.propertyRepresentation(c) for c in o.alldataproperties],
					"annotationproperties": [o.propertyRepresentation(c) for c in o.allannotationproperties],
					"instances": [o.instanceRepresentation(c) for c in o.allinstances],
				})

	rnd = t.render(c)

	return rnd




def _safe_print(u, errors="replace"):
    """Safely print the given string.

    If you want to see the code points for unprintable characters then you
    can use `errors="xmlcharrefreplace"`.
	http://code.activestate.com/recipes/576602-safe-print/
    """
    s = u.encode(sys.stdout.encoding or "utf-8", errors)
    print(s)




def main(argv):
	# get parameters
	if argv:
		rdf_filepath = argv[0]
	else:
		print("Usage: 'python ontodocs.py /path/to/somefile.rdf > output.html'")
		sys.exit(0)

	_safe_print(generate_html_table(rdf_filepath))
	# print generate_html_table(rdf_filepath)





if __name__ == "__main__":
	try:
		main(sys.argv[1:])
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
