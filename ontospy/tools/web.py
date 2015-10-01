#!/usr/bin/env python

# encoding: utf-8

"""
UTILITY TO GET A LIST OF RDF MODELS FROM PREFIX.CC

Copyright (c) 2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Shows a list of ontologies by querying http://prefix.cc/popular/all

"""

MODULE_VERSION = 0.2
USAGE = "ontospy-web <options>"


import time, optparse, os, rdflib


from ..libs.graph import Graph
from ..libs.util import *



def getCatalog(source="http://prefix.cc/popular/all.file.vann", query=""):
	""" 
	extracts a list of ontology URIs from http://prefix.cc/popular/all
	
	>query: a query string to match 
	
	"""

	printDebug("----------\nReading source...")	
	g = Graph(source)
	
	out = []
	for x in g.ontologies:
		if query:
			if query in unicode(x.prefix) or query in unicode(x.uri):
				out += [(unicode(x.prefix), unicode(x.uri))]
		else:
			out += [(unicode(x.prefix), unicode(x.uri))]
		
	printDebug("----------\n%d results found." % len(out))
	
	return out			


	
def printCatalog(_list):
	""" 
	prints out to terminal
	"""
	for x in _list:
		print x[0], " ==> ", x[1]			





def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=ontospy.VERSION)

	parser.add_option("-a", "--all",
			action="store_true", default=False, dest="all",
			help="Show all entries found by querying http://prefix.cc/popular/all.")

	parser.add_option("-q", "",
			action="store", type="string", default="", dest="query",
			help="A query string used to match the catalog entries.")
			
	opts, args = parser.parse_args()

	if not opts.all and not opts.query:
		parser.print_help()
		sys.exit(0)

	return opts, args



	
def main():
	""" command line script """
	
	print "OntoSPy " + ontospy.VERSION

	opts, args = parse_options()
					
	sTime = time.time()
				
	_list = getCatalog(query=opts.query)
	printCatalog(_list)

	
	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	printDebug("-" * 10) 
	printDebug("Time:	   %0.2fs" %  tTime)




				
	
if __name__ == '__main__':
	import sys
	from .. import ontospy
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e
