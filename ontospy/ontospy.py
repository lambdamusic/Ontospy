#!/usr/bin/env python
# encoding: utf-8



"""
ONTOSPY
Copyright (c) 2013-2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI, or check out the help:

>>> python ontospy.py -h

More info in the README file.

"""


import sys, os, time, optparse, os.path, shutil, cPickle, urllib2, datetime
from colorama import Fore, Back, Style

from .libs.graph import Graph, SparqlEndpoint
from .libs.util import bcolors, pprinttable, printDebug, _clear_screen

from ._version import *


# local repository constants
ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
ONTOSPY_LOCAL_MODELS = ONTOSPY_LOCAL + "/models"
ONTOSPY_LOCAL_VIZ = ONTOSPY_LOCAL + "/viz"
ONTOSPY_LOCAL_CACHE = ONTOSPY_LOCAL + "/.index/cache/"

# python package installation
_dirname, _filename = os.path.split(os.path.abspath(__file__))
ONTOSPY_SOUNDS = _dirname + "/data/sounds/"
ONTOSPY_LOCAL_TEMPLATES = _dirname + "/data/templates/"


def get_or_create_home_repo(reset=False):
	"""Check to make sure we never operate with a non existing local repo """
	dosetup = True
	if os.path.exists(ONTOSPY_LOCAL):
		dosetup = False
		print Style.DIM + "Local library: <%s>" % ONTOSPY_LOCAL + Style.RESET_ALL
		if reset:
			var = raw_input("Delete the local library and all of its contents? (y/n) ")
			if var == "y":
				shutil.rmtree(ONTOSPY_LOCAL)
				dosetup = True
			else:
				var == "n"

	if dosetup or not(os.path.exists(ONTOSPY_LOCAL)):
		os.mkdir(ONTOSPY_LOCAL)
	if dosetup or not(os.path.exists(ONTOSPY_LOCAL_MODELS)):	
		os.mkdir(ONTOSPY_LOCAL_MODELS)
	if dosetup or not(os.path.exists(ONTOSPY_LOCAL_CACHE)):	
		os.mkdir(ONTOSPY_LOCAL_CACHE)
	if dosetup or not(os.path.exists(ONTOSPY_LOCAL_VIZ)):	
		os.mkdir(ONTOSPY_LOCAL_VIZ)	
	if dosetup:
		print Fore.GREEN + "Setup successfull: local library created at <%s>" % ONTOSPY_LOCAL + Style.RESET_ALL
	return ONTOSPY_LOCAL	
	


def get_localontologies():
	"returns a list of file names in the ontologies folder (not the full path)"
	res = []
	if os.path.exists(ONTOSPY_LOCAL_MODELS):
		for f in os.listdir(ONTOSPY_LOCAL_MODELS):
			if os.path.isfile(os.path.join(ONTOSPY_LOCAL_MODELS,f)):
				if not f.startswith(".") and not f.endswith(".pickle"):
					res += [f]
	else:
		print "No local library found. Use the --reset command"					
	return res


def get_pickled_ontology(filename):
	""" try to retrieve a cached ontology """
	pickledfile =  ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
	if os.path.isfile(pickledfile):
		try:
			return cPickle.load(open(pickledfile, "rb"))
		except:
			print Style.DIM + "** WARNING: Cache is out of date ** ...recreating it... " + Style.RESET_ALL
			return None
	else:
		return None


	
def do_pickle_ontology(filename, g=None):
	""" 
	from a valid filename, generate the graph instance and pickle it too
	note: option to pass a pre-generated graph instance too	 
	2015-09-17: added code to increase recursion limit if cPickle fails
		see http://stackoverflow.com/questions/2134706/hitting-maximum-recursion-depth-using-pythons-pickle-cpickle
	"""
	pickledpath =  ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
	if not g:
		g = Graph(ONTOSPY_LOCAL_MODELS + "/" + filename)	
	
	try:				
		cPickle.dump(g, open( pickledpath, "wb" ) )
		print Style.DIM + ".. cached <%s>" % pickledpath + Style.RESET_ALL
	except Exception,e: 
		print Style.BRIGHT + "\n.. ERROR caching <%s>" % filename + Style.RESET_ALL
		print str(e)
		print Style.DIM + "\n.. attempting to increase the recursion limit from %d to %d" % (sys.getrecursionlimit(), sys.getrecursionlimit()*10) + Style.RESET_ALL
 
		try:
			sys.setrecursionlimit(sys.getrecursionlimit()*10)
			cPickle.dump(g, open( pickledpath, "wb" ) )
			print Style.BRIGHT + ".. SUCCESSFULLY cached <%s>" % pickledpath + Style.RESET_ALL
		except Exception,e: 
			print Style.BRIGHT + "\n.. ERROR caching <%s>... aborting..." % filename + Style.RESET_ALL
			print str(e)	
		sys.setrecursionlimit(sys.getrecursionlimit()/10)
	return g





def actionSelectFromLocal():
	" select a file from the local repo "
	
	options = get_localontologies()
	
	counter = 1
	printDebug("------------------", 'comment')
	for x in options:
		print Fore.BLUE + Style.BRIGHT + "[%d] " % counter + Style.RESET_ALL + x + Style.RESET_ALL
		# print Fore.BLUE + x[0], " ==> ", x[1]
		counter += 1
	
	
	while True:
		var = raw_input(Style.DIM + "------------------\nSelect a model by typing its number: (q=exit)\n" + Style.RESET_ALL)
		if var == "q":
			return None
		else:
			try:
				_id = int(var)
				ontouri = options[_id - 1]
				printDebug("You selected:", "comment")
				print Fore.RED + "---------\n" + ontouri + "\n---------" + Style.RESET_ALL
				return ontouri
			except:
				print "Error retrieving ontology. Please select a valid number."
				continue




def action_import(location):
	"""import files into the local repo """

	# 1) extract file from location and save locally
	fullpath = ""
	try:
		if location.startswith("http://"):
			headers = {'Accept': "application/rdf+xml"}
			req = urllib2.Request(location, headers=headers)
			res = urllib2.urlopen(req)
			final_location = res.geturl()  # after 303 redirects
			print "Loaded <%s>" % final_location
			filename = final_location.split("/")[-1] or final_location.split("/")[-2]
			fullpath = ONTOSPY_LOCAL_MODELS + "/" + filename

			file_ = open(fullpath, 'w')
			file_.write(res.read())
			file_.close()
		else:
			if os.path.isfile(location):
				filename = location.split("/")[-1] or location.split("/")[-2]
				fullpath = ONTOSPY_LOCAL_MODELS + "/" + filename
				shutil.copy(location, fullpath)
			else:
				raise ValueError('The location specified is not a file.')
		print "Saved local copy"
	except:
		print "Error retrieving file. Please make sure <%s> is a valid location." % location
		if os.path.exists(fullpath):
			os.remove(fullpath)
		return None

	# 2) check if valid RDF and cache it
	try:
		print "Loading graph..."
		g = Graph(fullpath)
		print "Loaded ", fullpath
	except:
		g = None
		if os.path.exists(fullpath):
			os.remove(fullpath)
		print "Error parsing file. Please make sure %s contains valid RDF." % location

	if g:
		print "Caching..."
		do_pickle_ontology(filename, g)

	# finally...
	return g



def action_import_folder(location):
	"""Try to import all files from a local folder"""

	if os.path.isdir(location):
		onlyfiles = [ f for f in os.listdir(location) if os.path.isfile(os.path.join(location,f)) ]
		for file in onlyfiles:
			if not file.startswith("."):
				filepath = os.path.join(location,file)
				print Fore.RED + "\n---------\n" + filepath + "\n---------" + Style.RESET_ALL
				return action_import(filepath)
	else:
		print "Not a valid directory"
		return None






##################
# 
#  COMMAND LINE 
#
##################




def shellPrintOverview(g, opts):
	ontologies = g.ontologies
				
	if opts['ontoannotations']:
		for o in ontologies:
			print Style.BRIGHT + "\nOntology Annotations\n-----------" + Style.RESET_ALL
			o.printTriples()

	elif opts['classtaxonomy']:
		print Style.BRIGHT + "\nClass Taxonomy\n" + "-" * 10  + Style.RESET_ALL
		g.printClassTree(showids=False, labels=opts['labels'])
			
	elif opts['propertytaxonomy']:
		print Style.BRIGHT + "\nProperty Taxonomy\n" + "-" * 10	 + Style.RESET_ALL
		g.printPropertyTree(showids=False, labels=opts['labels'])

	elif opts['skostaxonomy']:
		print Style.BRIGHT + "\nSKOS Taxonomy\n" + "-" * 10 + Style.RESET_ALL
		g.printSkosTree(showids=False, labels=opts['labels'])
	
	else:
		# default: print anything available 
		for o in ontologies:
			print Style.BRIGHT + "\nOntology Annotations\n-----------" + Style.RESET_ALL
			o.printTriples()
		if g.classes:
			print Style.BRIGHT + "\nClass Taxonomy\n" + "-" * 10  + Style.RESET_ALL
			g.printClassTree(showids=False, labels=opts['labels'])
		if g.properties:
			print Style.BRIGHT + "\nProperty Taxonomy\n" + "-" * 10	 + Style.RESET_ALL
			g.printPropertyTree(showids=False, labels=opts['labels'])
		if g.skosConcepts:
			print Style.BRIGHT + "\nSKOS Taxonomy\n" + "-" * 10	 + Style.RESET_ALL
			g.printSkosTree(showids=False, labels=opts['labels'])
			





def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	

	parser.add_option("-i", "--import",
			action="store_true", default=False, dest="_import",
			help="Import a file/folder/url into the local library.") 

	parser.add_option("-l", "--library",
			action="store_true", default=False, dest="lib",
			help="Select ontologies saved in the local library.") 
			
	parser.add_option("-o", "",
			action="store_true", default=False, dest="ontoannotations",
			help="Show only the ontology annotations/metadata.")
			
	parser.add_option("-c", "",
			action="store_true", default=False, dest="classtaxonomy",
			help="Show only the class taxonomy.")

	parser.add_option("-p", "",
			action="store_true", default=False, dest="propertytaxonomy",
			help="Show only the property taxonomy.")

	parser.add_option("-k", "",
			action="store_true", default=False, dest="skostaxonomy",
			help="Show only the SKOS taxonomy.")
			
	parser.add_option("-a", "",
			action="store_true", default=False, dest="labels",
			help="Show entities labels as well as URIs (used with -c or -p or -k).")

			
	opts, args = parser.parse_args()
	
	if opts._import and not args:
		printDebug("Please specify a file/folder/url to import into local library.", 'important')
		sys.exit(0)
				
	# not opts.shell and not opts.erase and not opts.cache and 
	if not opts.lib and not args:
		parser.print_help()
		sys.exit(0)
			
	return opts, args






	
def main():
	""" command line script """
	
	printDebug("OntoSPy " + VERSION, "comment")
	opts, args = parse_options()
	
	print_opts = {
					'ontoannotations' : opts.ontoannotations, 
					'classtaxonomy' : opts.classtaxonomy, 
					'propertytaxonomy' : opts.propertytaxonomy,
					'skostaxonomy' : opts.skostaxonomy,
					'labels' : opts.labels,
				}

	# select a model from the local ontologies
	if opts.lib:
		get_or_create_home_repo()
		filename = actionSelectFromLocal()
		if filename:
			g = get_pickled_ontology(filename)
			if not g:
				g = do_pickle_ontology(filename)	
			shellPrintOverview(g, print_opts)		
			printDebug("\n----------\n" + "Completed (note: you can explore this model interactively using the `ontospy-shell`)", "comment")	
		raise SystemExit, 1	



	# import an ontology
	# note: method duplicated in .ontospy and .tools.manager
	if opts._import:
		get_or_create_home_repo()
		_location = args[0]
		if os.path.isdir(_location):
			res = action_import_folder(_location)
		else:
			res = action_import(_location)
		if res: 
			printDebug("\n----------\n" + "Completed (note: load a local model by typing `ontospy -l`)", "comment")	
		raise SystemExit, 1

		
	# for all other cases...

	get_or_create_home_repo()  
	sTime = time.time()

	# load the ontology when a uri is passed manually
	if args:
		g = Graph(args[0])	
		shellPrintOverview(g, print_opts)

	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	printDebug("\n----------\n" + "Time:	   %0.2fs" %  tTime, "comment")



	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e



	

