#!/usr/bin/env python

# encoding: utf-8

"""
UTILITY TO MANAGE THE LOCAL ONTOSPY LIBRARY

Copyright (c) 2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""

MODULE_VERSION = 0.3
USAGE = "ontospy-manager [options]"


import time, optparse, os, rdflib, sys, datetime
from ConfigParser import SafeConfigParser

from .. import ontospy 
from ..core.graph import Graph
from ..core.util import *






def action_update_library_location(_location):
	"""
	Sets the folder that contains models for the local library 
	@todo: add options to move things over etc..
	note: this is called from 'manager' 
	"""
	
	# if not(os.path.exists(_location)):
	# 	os.mkdir(_location)
	# 	printDebug("Creating new folder..", "comment")
	
	printDebug("Old location: '%s'" % ontospy.get_home_location(), "comment")
	
	if os.path.isdir(_location):
		
		config = SafeConfigParser()
		config_filename = ontospy.ONTOSPY_LOCAL + '/config.ini'
		config.read(config_filename)
		if not config.has_section('models'):
			config.add_section('models')
		
		config.set('models', 'dir', _location)
		with open(config_filename, 'w') as f:			
			config.write(f) # note: this does not remove previously saved settings 
		
		return _location
	else:
		return None




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




def actions_delete():
	"""
	delete an ontology from the local repo
	"""

	filename = ontospy.actionSelectFromLocal()
	ONTOSPY_LOCAL_MODELS = ontospy.get_home_location()
	
	if filename:
		fullpath = ONTOSPY_LOCAL_MODELS + filename
		if os.path.exists(fullpath):
			var = raw_input("Are you sure? (y/n)")
			if var == "y":
				os.remove(fullpath)
				printDebug("Deleted %s" % fullpath, "important")
				cachepath = ontospy.ONTOSPY_LOCAL_CACHE + filename + ".pickle"
				# @todo: do this operation in /cache...
				if os.path.exists(cachepath):
					os.remove(cachepath)
					printDebug("Deleted %s" % cachepath, "important")
				
				return True

	return False

	




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
			help="List ontologies saved in the local library.") 

	parser.add_option("-u", "--update",
			action="store_true", default=False, dest="_setup",
			help="Update path of local library.") 

	parser.add_option("-d", "--delete",
			action="store_true", default=False, dest="_delete",
			help="Delete ontologies from the local library.") 
						
	parser.add_option("-c", "--cache",
			action="store_true", default=False, dest="cache",
			help="Force caching of the local library (for faster loading)")
			
	parser.add_option("-e", "--erase",
			action="store_true", default=False, dest="erase",
			help="Erase the local library by removing all existing files")

									
	opts, args = parser.parse_args()

	if opts._setup and not args:
		printDebug("Please specify a folder to be used for the local library e.g. 'ontospy-manager -u /Users/john/ontologies'", 'important')
		sys.exit(0)
				
	if not args and not opts._setup and not opts.list and not opts.cache and not opts.erase and not opts._delete:
		parser.print_help()
		sys.exit(0)

	return opts, args



	
def main():
	""" command line script """
	
	print "OntoSPy " + ontospy.VERSION	 
	opts, args = parse_options()
	
	if not opts._setup:
		ontospy.get_or_create_home_repo()
	
	# move local lib
	if opts._setup:
		_location = args[0]
		output = action_update_library_location(_location)
		if output:
			printDebug("----------\n" + "New location: '%s'" % _location, "important")
			printDebug("Note: no files have been moved or deleted (this has to be done manually)", "comment")
		else:
			printDebug("----------\n" + "Please specify an existing folder path.", "important")
		raise SystemExit, 1
	
	
	# reset local stuff
	if opts._delete:
		res = actions_delete()
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
	
				
	
if __name__ == '__main__':
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e
