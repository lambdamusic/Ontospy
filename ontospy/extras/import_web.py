# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""
UTILITY TO GET A LIST OF RDF MODELS FROM PREFIX.CC

Copyright (c) 2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Shows a list of ontologies by querying http://prefix.cc/popular/all

"""

from __future__ import print_function

MODULE_VERSION = 0.3
USAGE = "ontospy-web <options>"


import time, optparse, os, rdflib, sys

from .. import ontospy
from ..core.graph import Graph
from ..core.util import *



def getCatalog(source="http://prefix.cc/popular/all.file.vann", query=""):
	"""
	extracts a list of ontology URIs from http://prefix.cc/popular/all

	>query: a query string to match

	"""

	printDebug("----------\nReading source...")
	g = Graph(source, verbose=False)

	out = []
	for x in g.ontologies:
		if query:
			if query in unicode(x.prefix).lower() or query in unicode(x.uri).lower():
				out += [(unicode(x.prefix), unicode(x.uri))]
		else:
			out += [(unicode(x.prefix), unicode(x.uri))]

	printDebug("----------\n%d results found." % len(out))

	return out




def action_webimport(options):
	"""
	List models from web catalog (prefix.cc) and ask which one to import
	2015-10-10: originally part of main ontospy; now standalone only
	"""

	# options = web.getCatalog()
	counter = 1
	for x in options:
		print(Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + x[0] + " ==> ", Fore.RED +	 x[1], Style.RESET_ALL)
		# print(Fore.BLUE + x[0], " ==> ", x[1])
		counter += 1

	while True:
		var = raw_input(Style.BRIGHT + "=====\nSelect ID to import: (q=quit)\n" + Style.RESET_ALL)
		if var == "q":
			break
		else:
			try:
				_id = int(var)
				ontouri = options[_id - 1][1]
				print(Fore.RED + "\n---------\n" + ontouri + "\n---------" + Style.RESET_ALL)
				ontospy.action_import(ontouri)
			except:
				print("Error retrieving file. Import failed.")
				continue





def get_LOV_vocabularies(baseuri="http://lov.okfn.org/dataset/lov/api/v2/vocabulary/list"):
	"""
	pulls the json from the LOV vocabulary list
	"""
	import requests

	query = requests.get(baseuri, params={})

	return query.json()


def print_LOV_data(_json_list):

	for d in _json_list:
		print("%s ==> %s" % (d['titles'][0]['value'], d['uri']))







# ---------------------------------
# following section mainly for testing
# ---------------------------------



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
		# sys.exit(0)

	return opts, args




def main():
	""" command line script """

	print("OntoSpy " + ontospy.VERSION)
	ontospy.get_or_create_home_repo()

	opts, args = parse_options()

	sTime = time.time()

	# _list = getCatalog(query=opts.query)
	# action_webimport(_list)

	d = get_LOV_vocabularies()
	print_LOV_data(d)


	# finally:
	# print(some stats....)
	eTime = time.time()
	tTime = eTime - sTime
	printDebug("-" * 10)
	printDebug("Time:	   %0.2fs" %  tTime, "comment")






if __name__ == '__main__':

	# from .. import ontospy
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
