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

from libs.graph import Graph, SparqlEndpoint
from libs.util import bcolors, pprinttable

from _version import *


# local repository constants
ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
ONTOSPY_LOCAL_MODELS = ONTOSPY_LOCAL + "/models"
ONTOSPY_LOCAL_CACHE = ONTOSPY_LOCAL + "/cache"

# python package installation
_dirname, _filename = os.path.split(os.path.abspath(__file__))
ONTOSPY_DEFAULT_SCHEMAS_DIR = _dirname + "/data/schemas/"  # comes with installer
ONTOSPY_SOUNDS = _dirname + "/data/sounds/"


def get_or_create_home_repo(reset=False):
	"""Check to make sure we never operate with a non existing local repo """
	dosetup = True
	if os.path.exists(ONTOSPY_LOCAL):
		dosetup = False
		print Style.DIM + "Local repository: <%s>" % ONTOSPY_LOCAL + Style.RESET_ALL
		if reset:
			var = raw_input("Reset the local repository and all of its contents? (y/n) ")
			if var == "y":
				shutil.rmtree(ONTOSPY_LOCAL)
				dosetup = True
			else:
				var == "n"

	if dosetup:
		os.mkdir(ONTOSPY_LOCAL)
		os.mkdir(ONTOSPY_LOCAL_MODELS)
		os.mkdir(ONTOSPY_LOCAL_CACHE)
		print Fore.GREEN + "Setup successfull: local repository created at <%s>" % ONTOSPY_LOCAL + Style.RESET_ALL
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
		print "No local repository found. Use the --reset command"					
	return res


def get_pickled_ontology(filename):
	""" try to retrieve a cached ontology """
	pickledfile =  ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
	if os.path.isfile(pickledfile):
		return cPickle.load(open(pickledfile, "rb"))
	else:
		return None



# def do_pickle_ontology(filename, g=None):
#	  """
#	  from a valid filename, generate the graph instance and pickle it too
#	  note: option to pass a pre-generated graph instance too
#	  """
#	  if not g:
#		  g = Graph(ONTOSPY_LOCAL_MODELS + "/" + filename)
#	  pickledpath =	 ONTOSPY_LOCAL_CACHE + "/" + filename + ".pickle"
#	  cPickle.dump(g, open( pickledpath, "wb" ) )
#	  print Style.DIM + ".. cached <%s>" % pickledpath + Style.RESET_ALL
#	  return g
	
	
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





def action_reset():
	"""just a wrapper.. possibly to be extended in the future"""
	get_or_create_home_repo(reset=True)


def action_cache():
	print """The existing cache will be erased and recreated."""
	print """This operation may take several minutes, depending on how many files exist in your local repository."""
	var = raw_input(Style.BRIGHT + "=====\nProceed? (y/n) " + Style.RESET_ALL)
	if var == "y":
		repo_contents = get_localontologies()
		print Style.BRIGHT + "\n=====\n%d ontologies available in the local repository\n=====" % len(repo_contents) + Style.RESET_ALL
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
				do_pickle_ontology(onto, g)

		print Style.BRIGHT + "===Completed===" + Style.RESET_ALL

	else:
		print "Goodbye"


def action_listlocal():
	""" list all local files """
	ontologies = get_localontologies()
	if ontologies:
		print ""
		temp = []
		from collections import namedtuple
		Row = namedtuple('Row',['N','File','Added','Cached'])
		counter = 0
		for file in ontologies:
			counter += 1
			name = file
			try:
				mtime = os.path.getmtime(ONTOSPY_LOCAL_MODELS + "/" + file)
			except OSError:
				mtime = 0
			last_modified_date = str(datetime.datetime.fromtimestamp(mtime))

			cached = str(os.path.exists(ONTOSPY_LOCAL_CACHE + "/" + file + ".pickle"))
			temp += [Row(str(counter),name,last_modified_date,cached)]
		pprinttable(temp)
		print ""
	else:
		print "No files in the local repository. Use the --import command."


def action_import(location):
	"""import files into the local repo """

	# 1) extract file from location and save locally
	fullpath = ""
	try:
		if location.startswith("http://"):
			headers = "Accept: application/rdf+xml"
			req = urllib2.Request(location, headers)
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
				action_import(filepath)
	else:
		print "Not a valid directory"





def action_webimport():
	"""List models from web catalog (prefix.cc) and ask which one to import"""

	import catalog
	options = catalog.viewCatalog()
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
				action_import(ontouri)
			except:
				continue








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
		if g.classes:
			print Style.BRIGHT + "\nClass Taxonomy\n" + "-" * 10  + Style.RESET_ALL
			g.printClassTree(showids=False, labels=opts['labels'])
		if g.properties:
			print Style.BRIGHT + "\nProperty Taxonomy\n" + "-" * 10	 + Style.RESET_ALL
			g.printPropertyTree(showids=False, labels=opts['labels'])
		if g.skosConcepts:
			print Style.BRIGHT + "\nSKOS Taxonomy\n" + "-" * 10	 + Style.RESET_ALL
			g.printSkosTree(showids=False, labels=opts['labels'])
			
		
		
		#
		# if not opts['ontoannotations'] and not opts['propertytaxonomy']:
		#	opts['classtaxonomy'] = True # default


def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	

			
	parser.add_option("", "--shell",
			action="store_true", default=False, dest="shell",
			help="Interactive explorer of the ontologies in the local repository")	
			
	parser.add_option("", "--repo",
			action="store_true", default=False, dest="repo",
			help="List ontologies in the local repository") 

	parser.add_option("", "--import",
			action="store_true", default=False, dest="_import",
			help="Imports file/folder/url into the local repository") 

	parser.add_option("", "--web",
			action="store_true", default=False, dest="web",
			help="List and import schemas registered on http://prefix.cc/") 

	parser.add_option("", "--cache",
			action="store_true", default=False, dest="cache",
			help="Rebuild the cache for the local repository")

	parser.add_option("", "--reset",
			action="store_true", default=False, dest="reset",
			help="Resets the local repository by removing all existing files")
			
	parser.add_option("-a", "",
			action="store_true", default=False, dest="ontoannotations",
			help="Print the ontology annotations/metadata.")
			
	parser.add_option("-c", "",
			action="store_true", default=False, dest="classtaxonomy",
			help="Print the class taxonomy.")

	parser.add_option("-p", "",
			action="store_true", default=False, dest="propertytaxonomy",
			help="Print the property taxonomy.")

	parser.add_option("-s", "",
			action="store_true", default=False, dest="skostaxonomy",
			help="Print the SKOS taxonomy.")
			
	parser.add_option("-l", "",
			action="store_true", default=False, dest="labels",
			help="Print entities labels as well as URIs (used with -c or -p or -s).")

			
	opts, args = parser.parse_args()

	if not opts.shell and not opts.reset and not opts.repo and not opts.cache and not opts.web and len(args) < 1:
		parser.print_help()
		sys.exit(0)
		
	return opts, args






	
def main():
	""" command line script """
	
	print "OntoSPy " + VERSION
	opts, args = parse_options()
	
	# reset local stuff
	if opts.reset:
		action_reset()
		raise SystemExit, 1


	# list local ontologies
	if opts.repo:
		get_or_create_home_repo()
		action_listlocal()
		raise SystemExit, 1

		
	# cache local ontologies
	if opts.cache:
		get_or_create_home_repo()
		action_cache()
		raise SystemExit, 1

	# import an ontology
	if opts._import:
		get_or_create_home_repo()
		_location = args[0]
		if os.path.isdir(_location):
			action_import_folder(_location)
		else:
			action_import(_location)
		action_listlocal()	
		raise SystemExit, 1

	# launch shell
	if opts.shell:
		import shell
		shell.Shell()._clear_screen()
		print Style.BRIGHT + "** OntoSPy Interactive Ontology Documentation Environment " + VERSION + " **" +\
			Style.RESET_ALL
		get_or_create_home_repo()
		shell.Shell().cmdloop()
		raise SystemExit, 1
		
	# load web catalog
	if opts.web:
		get_or_create_home_repo()
		action_webimport()
		raise SystemExit, 1

		
	print_opts = {
					'ontoannotations' : opts.ontoannotations, 
					'classtaxonomy' : opts.classtaxonomy, 
					'propertytaxonomy' : opts.propertytaxonomy,
					'skostaxonomy' : opts.skostaxonomy,
					'labels' : opts.labels,
				}

	get_or_create_home_repo()  # for all other cases
	sTime = time.time()

	# load the ontology
	if args:
		g = Graph(args[0])
	
		shellPrintOverview(g, print_opts)


	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	print "\n", Style.DIM + "Time:	   %0.2fs" %  tTime + Style.RESET_ALL



	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e



	

