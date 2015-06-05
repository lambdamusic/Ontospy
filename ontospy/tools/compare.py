"""
module that allows the comparison of two ontologies, ie what classes and properties they have in common


Example:compare a local turtle graph to the FOAF ontology

python compare.py -o http://xmlns.com/foaf/0.1/ test/testTurtle.ttl 

"""



import sys, time, math, optparse, os, urllib2
from collections import namedtuple

import rdflib	 # so we have it available as a namespace

from ontospy import *
from utils import *



__version__ = "0.1"
__copyright__ = "CopyRight (C) 2013 by Michele Pasin"
__license__ = "MIT"
__author__ = "Michele Pasin"
__author_email__ = "michele dot pasin at gmail dot com"

USAGE = "%prog -o masterOntology graph_to_validate`"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)






def compare(referenceOnto, somegraph):
	"""
	Desc
	"""

	spy1 = Ontology(referenceOnto)
	spy2 = Ontology(somegraph)

	class_comparison = {}
	for x in spy2.allclasses:
		if x not in spy1.allclasses:
			class_comparison[x] = False
		else:
			class_comparison[x] = True

	prop_comparison = {}
	for x in spy2.allinferredproperties:
		if x not in spy1.allinferredproperties:
			prop_comparison[x] = False
		else:
			prop_comparison[x] = True


	return {'stats' : {	'classes': len(spy2.allclasses), 
						'properties' : len(spy2.allinferredproperties), 
						'triples' : len(spy2.rdfGraph)}, 
			'class_comparison' : class_comparison ,
			'prop_comparison' : prop_comparison}




def printComparison(results, class_or_prop):
	"""
	Print out the results of the comparison using a nice table
	"""

	data = []
	
	Row = namedtuple('Row',[class_or_prop,'VALIDATED'])

	for k,v in sorted(results.items(), key=lambda x: x[1]):
		data += [Row(k, str(v))]

	pprinttable(data)












def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
 
	parser.add_option("-o", "--ontology",
			action="store", type="string", default="", dest="ontology",
			help="Specifies which ontology to compare to.")

	opts, args = parser.parse_args()

	if len(args) < 1 or not opts.ontology:
		parser.print_help()
		raise SystemExit, 1

	return opts, args





def main():
	# get parameters
	opts, args = parse_options()
	ontology = opts.ontology
	somegraph = args[0]

	if ontology and somegraph:
		sTime = time.time()

		print "\nReference ontology: <%s>" % (ontology)
		print "Graph to validate: <%s>\n" % (somegraph)

		results = compare(ontology, somegraph)


		print "Classes:    %d" % results['stats']['classes']
		print "Properties: %d" % results['stats']['properties']
		print "Triples:    %d" % results['stats']['triples']
		print "-" * 10

		# pretty prints the results

		printComparison(results['class_comparison'], "CLASSES")
		print "-" * 10
		printComparison(results['prop_comparison'], "PROPERTIES")


		# print some stats.... 

		eTime = time.time()
		tTime = eTime - sTime
		print "-" * 10

		print "Time:       %0.2fs" %  tTime

	else:
		sys.exit(0)



if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e


