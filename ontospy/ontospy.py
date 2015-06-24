#!/usr/bin/env python
# encoding: utf-8



"""
ONTOSPY
Copyright (c) 2013-2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI. 

>>> python ontospy.py -h

More info in the README file.

"""


import sys, os, time, optparse

from libs.graph import Graph, SparqlEndpoint

from _version import *




##################
# 
#  COMMAND LINE 
#
##################



def shellPrintOverview(g, opts):
	ontologies = g.ontologies
	
	
	if opts['ontoannotations']:
		for o in ontologies:
			print "\nOntology Annotations\n-----------"
			o.printTriples()
				
	if opts['classtaxonomy']:
		print "\nClass Taxonomy\n" + "-" * 10 
		g.printClassTree(showids=False, labels=opts['labels'])
	
	if opts['propertytaxonomy']:
		print "\nProperty Taxonomy\n" + "-" * 10 
		g.printPropertyTree(showids=False, labels=opts['labels'])
		
	
	#
	# if False:
	# 	print "Top Layer:", str([cc.qname for cc in g.toplayer])
	#
	#
	# if False:
	#	for c in g.classes:
	#		print c.qname
	#		print "...direct Supers: ", len(c.directSupers), str([cc.qname for cc in c.directSupers])
	#		print "...direct Subs: ", len(c.directSubs), str([cc.qname for cc in c.directSubs])

		# c.triplesPrint()







def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	

	parser.add_option("-a", "--annotations",
			action="store_true", default=False, dest="ontoannotations",
			help="Print the ontology annotations/metadata.")
			
	parser.add_option("-c", "--classes",
			action="store_true", default=False, dest="classtaxonomy",
			help="Print the class taxonomy.")

	parser.add_option("-p", "--properties",
			action="store_true", default=False, dest="propertytaxonomy",
			help="Print the property taxonomy.")

	parser.add_option("-l", "--labels",
			action="store_true", default=False, dest="labels",
			help="Print entities labels as well as URIs (used in conjunction with -c or -p).")

	parser.add_option("", "--showlocal",
			action="store_true", default=False, dest="showlocal",
			help="Prints the ontologies in the local repository.")

	opts, args = parser.parse_args()

	return opts, args


	
def main():
	""" command line script """
	
	# get file location
	dirname, filename = os.path.split(os.path.abspath(__file__))
	DEFAULT_SCHEMAS_DIR = dirname + "/data/schemas/"
	DEFAULT_ONTO = DEFAULT_SCHEMAS_DIR + "pizza.ttl"
	
	opts, args = parse_options()

	if opts.showlocal:
		onlyfiles = [ f for f in os.listdir(DEFAULT_SCHEMAS_DIR) if os.path.isfile(os.path.join(DEFAULT_SCHEMAS_DIR,f)) ]
		for file in onlyfiles:
			if not file.startswith("."):
				print os.path.join(DEFAULT_SCHEMAS_DIR,file)
		raise SystemExit, 1

	if len(args) < 1:
		print "No argument specified. Use -h for more info."
		raise SystemExit, 1		
	
	print_opts = {
					'ontoannotations' : opts.ontoannotations, 
					'classtaxonomy' : opts.classtaxonomy, 
					'propertytaxonomy' : opts.propertytaxonomy,
					'labels' : opts.labels,
				}
	
	sTime = time.time()

	if args:
		g = Graph(args[0])
	else: # 2015-06-24: deprecated via the test in parse_options
		print "Argument not provided... loading test graph: %s" % DEFAULT_ONTO
		g = Graph(DEFAULT_ONTO)
	
	shellPrintOverview(g, print_opts)


	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	print "-" * 10 
	print "Time:	   %0.2fs" %  tTime



 
	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e



	

