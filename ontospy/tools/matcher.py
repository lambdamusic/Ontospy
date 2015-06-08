#!/usr/bin/env python
# encoding: utf-8


"""
>python tools/matcher.py data/schemas/npgcore_latest.ttl data/schemas/foaf.rdf 
Loaded 630 triples
started scanning...
----------
Ontologies found: 1
Classes found...: 15
Properties found: 67
Annotation......: 7
Datatype........: 26
Object..........: 34
Loaded 3478 triples
started scanning...
----------
Ontologies found: 1
Classes found...: 64
Properties found: 253
Annotation......: 36
Datatype........: 133
Object..........: 84
----------
Matching...
Person ==~== Term: npg:Person 
<Class *http://www.w3.org/2000/10/swap/pim/contact#Person*>
...<Class *http://ns.nature.com/terms/Person*>
Document ==~== Term: npg:Document 
<Class *http://xmlns.com/foaf/0.1/Document*>
...<Class *http://ns.nature.com/terms/Document*>
Document ==~== Term: npg:DocumentAsset 
<Class *http://xmlns.com/foaf/0.1/Document*>
...<Class *http://ns.nature.com/terms/DocumentAsset*>
Organization ==~== Term: npg:Organization 
<Class *http://xmlns.com/foaf/0.1/Organization*>
...<Class *http://ns.nature.com/terms/Organization*>
Person ==~== Term: npg:Person 
<Class *http://xmlns.com/foaf/0.1/Person*>
...<Class *http://ns.nature.com/terms/Person*>
PersonalProfileDocument ==~== Term: npg:Document 
<Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>
...<Class *http://ns.nature.com/terms/Document*>


"""


USAGE = "Usage..."
VERSION = 0.1


import ontospy, rdflib
import time, optparse, csv
from difflib import SequenceMatcher
from libs.util import *


def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

	
def matcher(graph1, graph2, confidence=0.5, output_file="matching_results.csv"):
	""" 
	takes two graphs and matches its classes based on qname, label etc.. 
	@todo extend to properties and skos etc..
	"""

	printDebug("----------\nNow matching...")
	
	f = open(output_file, 'wt')
	counter = 0
	
	try:
		writer = csv.writer(f)
		writer.writerow( ('entity name source', 'entity name destination', 'entity uri source', 'entity uri destination') )
		
		for x in graph1.classes:
			l1 = str(x.bestLabel())
		
			for y in graph2.classes:
				l2 = str(y.bestLabel())
						
				if similar(l1, l2) > confidence:	
					counter += 1				
					writer.writerow([l1, l2, x.uri, y.uri])


	finally:
		f.close()
		
	printDebug("%d candidates found." % counter)
				
				




def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	
	# parser.add_option("-c", "--confidence",
	#		action="store_true", default=False, dest="confidence",
	#		help="Print detailed information for all entities in the ontology.")

	parser.add_option("-o", "--outputfile",
			action="store", type="string", default="matching_results.csv", dest="outputfile",
			help="The name of the output csv file.")
			
	parser.add_option("-c", "--confidence",
			action="store", type="float", default=0.5, dest="confidence",
			help="@TODO 0.1-0.9 degree of confidence for similarity matching.")
						
	opts, args = parser.parse_args()

	# if len(args) < 1:
	#	parser.print_help()
	#	raise SystemExit, 1

	return opts, args



	
def main():
	""" command line script """
	
	opts, args = parse_options()
	
	if len(args) < 2:
		printDebug("Please provide two arguments.") 
		sys.exit(0)

	if type(opts.confidence) != float:
		opts.confidence = 0.5
	
	sTime = time.time()
	
	g1 = ontospy.Graph(args[0])
	g2 = ontospy.Graph(args[1])
	
	matcher(g1, g2, opts.confidence, opts.outputfile)
	
	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	printDebug("-" * 10) 
	printDebug("Time:	   %0.2fs" %  tTime)




				
	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e

