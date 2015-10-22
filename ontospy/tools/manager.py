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
				mtime = os.path.getmtime(ontospy.ONTOSPY_LOCAL_MODELS + "/" + file)
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
	var = raw_input(Style.BRIGHT + "=====\nProceed? (y/n) " + Style.RESET_ALL)
	if var == "y":
		repo_contents = ontospy.get_localontologies()
		print Style.BRIGHT + "\n=====\n%d ontologies available in the local library\n=====" % len(repo_contents) + Style.RESET_ALL
		for onto in repo_contents:
			fullpath = ontospy.ONTOSPY_LOCAL_MODELS + "/" + onto
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
			
	parser.add_option("-c", "--cache",
			action="store_true", default=False, dest="cache",
			help="Rebuild the cache for the local library (recommended)")
			
	parser.add_option("-e", "--erase",
			action="store_true", default=False, dest="erase",
			help="Erase the local library by removing all existing files")

	parser.add_option("-i", "--import",
			action="store_true", default=False, dest="_import",
			help="Import a file/folder/url into the local library.") 
						
	opts, args = parser.parse_args()

	if opts._import and not args:
		printDebug("Please specify a file/folder/url to import into local library.", 'important')
		sys.exit(0)
		
	if not opts.list and not opts.cache and not opts.erase and not opts._import:
		parser.print_help()
		sys.exit(0)

	return opts, args



	
def main():
	""" command line script """
	
	print "OntoSPy " + ontospy.VERSION
	
	 
	
	
	opts, args = parse_options()

	# reset local stuff
	if opts.erase:
		action_erase()
		raise SystemExit, 1
	
	# select a model from the local ontologies
	if opts.list:
		ontospy.get_or_create_home_repo()
		action_listlocal()
		raise SystemExit, 1 
	
	# cache local ontologies
	if opts.cache:
		sTime = time.time()
		ontospy.get_or_create_home_repo()
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
		ontospy.get_or_create_home_repo()
		_location = args[0]
		if os.path.isdir(_location):
			res = ontospy.action_import_folder(_location)
		else:
			res = ontospy.action_import(_location)
		if res: 
			printDebug("\n----------\n" + "Completed (note: load a local model by typing `ontospy -l`)", "comment")	
		raise SystemExit, 1
				
	
if __name__ == '__main__':
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e
