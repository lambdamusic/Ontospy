#!/usr/bin/env python
# encoding: utf-8



"""
ONTOSPY
Copyright (c) 2013-2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI. 

>>> python ontospy.py -h

More info in the README file.

"""


import sys, os, time, optparse, os.path, shutil, cPickle, urllib2

from colorama import Fore, Back, Style

from libs.graph import Graph, SparqlEndpoint
from libs.util import bcolors

from _version import *


ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
# get file location
_dirname, _filename = os.path.split(os.path.abspath(__file__))
ONTOSPY_DEFAULT_SCHEMAS_DIR = _dirname + "/data/schemas/"  # comes with installer
ONTOSPY_SOUNDS = _dirname + "/data/sounds/"


def get_or_create_home_repo(reset=False):
	dosetup = True
	if os.path.exists(ONTOSPY_LOCAL):
		dosetup = False
		print Style.DIM + "Local repository: <%s>" % ONTOSPY_LOCAL + Style.RESET_ALL
		if reset:
			var = raw_input("Reset the local repository and all of its contents? (y/n)")
			if var == "y":
				shutil.rmtree(ONTOSPY_LOCAL)
				dosetup = True
			else:
				var == "n"
			print var	
	if dosetup:
		os.mkdir(ONTOSPY_LOCAL)		
		print Fore.GREEN + "Setup successfull: local repository created at <%s>" % ONTOSPY_LOCAL + Style.RESET_ALL
	return ONTOSPY_LOCAL	
	


def get_localontologies():
	"returns a list of file names in the ontologies folder"
	res = []
	if os.path.exists(ONTOSPY_LOCAL):
		for f in os.listdir(ONTOSPY_LOCAL):
			if os.path.isfile(os.path.join(ONTOSPY_LOCAL,f)):
				if not f.startswith(".") and not f.endswith(".pickle"):
					res += [f]
	else:
		print "No local repository found. Try --setup first."					
	return res


def get_pickled_ontology(fullpath_localonto):
	""" <fullpath_localonto> eg /Users/michele.pasin/.ontospy/skos.rdf"""
	pickledfile = fullpath_localonto+".pickle"
	if os.path.isfile(pickledfile):
		return cPickle.load(open(pickledfile, "rb"))
	else:
		return None


def do_pickle_ontology(fullpath, g=None):
	""" from a valid fullpath, generate the grpah instance and pickle it too
		note: option to pass a pre-generated graph instance too  
	"""
	try:
		if not g:
			g = Graph(fullpath)
		pickledpath = fullpath + ".pickle"
		cPickle.dump(g, open( pickledpath, "wb" ) )
		print "\n.. cached <%s>" % pickledpath
	except: 
		g = Graph(fullpath)
		print "\n.. ERROR caching <%s>" % pickledpath
	return g



##################
# 
#  COMMAND LINE 
#
##################



def shellPrintOverview(g, opts):
	ontologies = g.ontologies
	
	
	if not opts['ontoannotations'] and not opts['propertytaxonomy']:
		opts['classtaxonomy'] = True # default
	
	if opts['classtaxonomy']:
		print "\nClass Taxonomy\n" + "-" * 10 
		g.printClassTree(showids=False, labels=opts['labels'])
		
	if opts['ontoannotations']:
		for o in ontologies:
			print "\nOntology Annotations\n-----------"
			o.printTriples()
	
	if opts['propertytaxonomy']:
		print "\nProperty Taxonomy\n" + "-" * 10 
		g.printPropertyTree(showids=False, labels=opts['labels'])




def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	

	parser.add_option("", "--repo",
			action="store_true", default=False, dest="repo",
			help="List ontologies in the local repository")	

	parser.add_option("", "--import",
			action="store_true", default=False, dest="_import",
			help="Imports file/folder/url into the local repository") 

	parser.add_option("", "--web",
			action="store_true", default=False, dest="web",
			help="List and import schemas registered on http://prefix.cc/") 
			
	parser.add_option("", "--shell",
			action="store_true", default=False, dest="shell",
			help="Interactive explorer of the ontologies in the local repository")	
				
	parser.add_option("-a", "",
			action="store_true", default=False, dest="ontoannotations",
			help="Print the ontology annotations/metadata.")
			
	parser.add_option("-c", "",
			action="store_true", default=False, dest="classtaxonomy",
			help="Print the class taxonomy.")

	parser.add_option("-p", "",
			action="store_true", default=False, dest="propertytaxonomy",
			help="Print the property taxonomy.")

	parser.add_option("-l", "",
			action="store_true", default=False, dest="labels",
			help="Print entities labels as well as URIs (used with -c or -p).")

			
	opts, args = parser.parse_args()

	if not opts.shell and not opts.repo and not opts.web and len(args) < 1:
		parser.print_help()
		sys.exit(0)
		
	return opts, args


	
def main():
	""" command line script """
	
	print "OntoSPy " + VERSION + "\n-----------"
	
	# ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
	
	opts, args = parse_options()

	# list local ontologies
	if opts.repo:		
		get_or_create_home_repo()
		action_listlocal()
		raise SystemExit, 1

	# import an ontology
	if opts._import:		
		get_or_create_home_repo()		
		_location = args[0]
		if os.path.isdir(_location):
			action_import_folder(_location)
		else:
			action_import(_location)
		raise SystemExit, 1

	# launch shell
	if opts.shell:	
		get_or_create_home_repo()
		import shell	
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
					'labels' : opts.labels,
				}
	
	sTime = time.time()

	# load the ontology
	if args:
		g = Graph(args[0])
	
		shellPrintOverview(g, print_opts)


	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	print "-" * 10 
	print "Time:	   %0.2fs" %  tTime





def action_listlocal():
	""" list all local files """
	ontologies = get_localontologies()
	if ontologies:
		for file in ontologies:
			print ONTOSPY_LOCAL + "/" + file



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
			fullpath = ONTOSPY_LOCAL+ "/" + filename

			file_ = open(fullpath, 'w')
			file_.write(res.read())
			file_.close()
	
		else:
			if os.path.isfile(location):
				filename = location.split("/")[-1] or location.split("/")[-2]
				fullpath = ONTOSPY_LOCAL + "/" + filename
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
		do_pickle_ontology(fullpath, g) 

	# finally...
	return g
	


def action_import_folder(location):	
	""" @todo :"""
	
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
	""" @todo : just a list of ontos for now"""
	
	import catalog
	options = catalog.viewCatalog()
	counter = 1
	for x in options:
		print Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + x[0] + " ==> ", Fore.RED +  x[1], Style.RESET_ALL
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





	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e



	

