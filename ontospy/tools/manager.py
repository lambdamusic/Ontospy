#!/usr/bin/env python

# encoding: utf-8

"""
UTILITY TO MANAGE THE LOCAL ONTOSPY LIBRARY

Copyright (c) 2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""

MODULE_VERSION = 0.1
USAGE = "ontospy-manager <options>"


import time, optparse, os, rdflib, sys, datetime

from .. import ontospy 
from ..libs.graph import Graph
from ..libs.util import *





def action_listlocal():
	""" 
	list all local files 
	2015-10-18: removed 'cached' from report
	"""
	ontologies = ontospy.get_localontologies()
	ONTOSPY_LOCAL_MODELS = ontospy.get_home_location()

	if ontologies:
		print ""
		temp = []
		from collections import namedtuple
		Row = namedtuple('Row',['N','Added', 'File'])
		# Row = namedtuple('Row',['N','Added','Cached', 'File'])
		counter = 0
		for file in ontologies:
			counter += 1
			name = Style.BRIGHT + file + Style.RESET_ALL
			try:
				mtime = os.path.getmtime(ONTOSPY_LOCAL_MODELS + "/" + file)
			except OSError:
				mtime = 0
			last_modified_date = str(datetime.datetime.fromtimestamp(mtime))

			# cached = str(os.path.exists(ONTOSPY_LOCAL_CACHE + "/" + file + ".pickle"))
			temp += [Row(str(counter),last_modified_date, name)]
		pprinttable(temp)
		print ""
	else:
		print "No files in the local library. Use the --import command."




def action_erase():
	"""just a wrapper.. possibly to be extended in the future"""
	ontospy.get_or_create_home_repo(reset=True)
	return True




def action_cache():
	print """The existing cache will be erased and recreated."""
	print """This operation may take several minutes, depending on how many files exist in your local library."""
	ONTOSPY_LOCAL_MODELS = ontospy.get_home_location()
	
	var = raw_input(Style.BRIGHT + "=====\nProceed? (y/n) " + Style.RESET_ALL)
	if var == "y":
		repo_contents = ontospy.get_localontologies()
		print Style.BRIGHT + "\n=====\n%d ontologies available in the local library\n=====" % len(repo_contents) + Style.RESET_ALL
		for onto in repo_contents:
			fullpath = ONTOSPY_LOCAL_MODELS + "/" + onto
			try:
				print Fore.RED + "\n=====\n" + onto + Style.RESET_ALL
				print "Loading graph..."
				g = Graph(fullpath)
				print "Loaded ", fullpath
			except:
				g = None
				print "Error parsing file. Please make sure %s contains valid RDF." % fullpath

			if g:
				print "Caching..."
				ontospy.do_pickle_ontology(onto, g)

		print Style.BRIGHT + "===Completed===" + Style.RESET_ALL

	else:
		print "Goodbye"







def getPrefixCatalog(source="http://prefix.cc/popular/all.file.vann", query=""):
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




def action_webimport(options):
	"""
	List models from web catalog (prefix.cc) and ask which one to import
	2015-10-10: originally part of main ontospy; now standalone only 
	"""

	# options = web.getCatalog()
	counter = 1
	for x in options:
		print Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + x[0] + " ==> ", Fore.RED +	 x[1], Style.RESET_ALL
		# print Fore.BLUE + x[0], " ==> ", x[1]
		counter += 1

	while True:
		var = raw_input(Style.BRIGHT + "=====\nSelect ID to import: (q=exit)\n" + Style.RESET_ALL)
		if var == "q":
			break
		else:
			try:
				_id = int(var)
				ontouri = options[_id - 1][1]
				print Fore.RED + "\n---------\n" + ontouri + "\n---------" + Style.RESET_ALL
				ontospy.action_import(ontouri)
			except:
				print "Error retrieving file. Import failed."
				continue








def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=ontospy.VERSION)

	
	
	parser.add_option("-l", "--list",
			action="store_true", default=False, dest="list",
			help="Select ontologies saved in the local library.") 

	parser.add_option("-u", "--update",
			action="store_true", default=False, dest="_setup",
			help="Update local library location.") 

	parser.add_option("-d", "--delete",
			action="store_true", default=False, dest="_delete",
			help="[@todo] Delete ontologies from the local library.") 
						
	parser.add_option("-c", "--cache",
			action="store_true", default=False, dest="cache",
			help="Force caching of the local library (for faster loading)")
			
	parser.add_option("-e", "--erase",
			action="store_true", default=False, dest="erase",
			help="Erase the local library by removing all existing files")

	parser.add_option("-i", "--import",
			action="store_true", default=False, dest="_import",
			help="Import a file/folder/url into the local library.") 

	parser.add_option("-w", "--importweb",
			action="store_true", default=False, dest="_web",
			help="Import vocabularies registered on http://prefix.cc/popular.") 
	
	# parser.add_option("-q", "",
	# 		action="store", type="string", default="", dest="query",
	# 		help="A query string used to match the catalog entries.")
									
	opts, args = parser.parse_args()

	if opts._import and not args:
		printDebug("Please specify a file/folder/url to import into local library.", 'important')
		sys.exit(0)
		
	if not opts._setup and not opts.list and not opts.cache and not opts.erase and not opts._import and not opts._web:
		parser.print_help()
		sys.exit(0)

	return opts, args



	
def main():
	""" command line script """
	
	print "OntoSPy " + ontospy.VERSION
	ontospy.get_or_create_home_repo()
		 
	opts, args = parse_options()

	# move local lib
	if opts._setup:
		ontospy.set_home_location(asknew=True)
		raise SystemExit, 1
		
	# reset local stuff
	if opts.erase:
		action_erase()
		raise SystemExit, 1
	
	# select a model from the local ontologies
	if opts.list:		
		action_listlocal()
		raise SystemExit, 1 
	
	# cache local ontologies
	if opts.cache:
		sTime = time.time()
		action_cache()
		# finally: print some stats....
		eTime = time.time()
		tTime = eTime - sTime
		printDebug("-" * 10)
		printDebug("Time:	   %0.2fs" %  tTime, "comment")
		raise SystemExit, 1


	# import an ontology
	# note: method duplicated in .ontospy and .tools.manager
	if opts._import:
		_location = args[0]
		if os.path.isdir(_location):
			res = ontospy.action_import_folder(_location)
		else:
			res = ontospy.action_import(_location)
		if res: 
			printDebug("\n----------\n" + "Completed (note: load a local model by typing `ontospy -l`)", "comment")	
		raise SystemExit, 1
			
			
	if opts._web:
		# _list = getPrefixCatalog(query=opts.query) # 2015-11-01: no query for now
		_list = getPrefixCatalog(query="")
		action_webimport(_list)		
				
	
if __name__ == '__main__':
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e
