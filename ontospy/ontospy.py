#!/usr/bin/env python
# encoding: utf-8



"""
ONTOSPY
Copyright (c) 2013-2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI. 

>>> python ontospy.py -h

More info in the README file.

"""


import sys, os, time, optparse, os.path, shutil, cPickle

from libs.graph import Graph, SparqlEndpoint
from libs.util import bcolors

from _version import *


ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
# get file location
_dirname, _filename = os.path.split(os.path.abspath(__file__))
ONTOSPY_DEFAULT_SCHEMAS_DIR = _dirname + "/data/schemas/"  # comes with installer



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


def get_picked_ontology(fullpath_localonto):
	""" <fullpath_localonto> eg /Users/michele.pasin/.ontospy/skos.rdf"""
	pickledfile = fullpath_localonto+".pickle"
	if os.path.isfile(pickledfile):
		return cPickle.load(open(pickledfile, "rb"))
	else:
		return None


def do_pickle_ontology(fullpath):
	try:
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
	

	parser.add_option("", "--list",
			action="store_true", default=False, dest="listlocal",
			help="List ontologies in the local repository.")
	
	parser.add_option("", "--local",
			action="store_true", default=False, dest="loadlocal",
			help="Load ontologies from the local repository.")		

	parser.add_option("", "--shell",
			action="store_true", default=False, dest="shell",
			help="Interact with ontologies via the wonderful ontospy shell.")	
			
	parser.add_option("", "--web",
			action="store_true", default=False, dest="web",
			help="List ontologies registered on http://prefix.cc/popular/all.") 

	parser.add_option("", "--setup",
			action="store_true", default=False, dest="setup",
			help="Creates a local repository of ontologies.") 
						
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

	if not opts.shell and not opts.listlocal and not opts.loadlocal and not opts.web and not opts.setup and len(args) < 1:
		parser.print_help()
		sys.exit(0)
		
	return opts, args


	
def main():
	""" command line script """
	
	print "OntoSPy " + VERSION + "\n-----------"

	
	# ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
	
	opts, args = parse_options()

	if opts.listlocal:		
		action_listlocal()
		raise SystemExit, 1


	if opts.loadlocal:		
		args = action_loadLocal(args)


	if opts.shell:	
		import shell	
		shell.Shell().cmdloop()
		raise SystemExit, 1
		
		
	if opts.web:
		import catalog
		options = catalog.viewCatalog()
		for x in options:
			print x[0], " ==> ", x[1]
		raise SystemExit, 1


	if opts.setup:
		action_setupHomeFolder()
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
		if opts.loadlocal:
			# check if there's a pickled version
			g = get_picked_ontology(args[0]) or Graph(args[0])
		else:
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


def action_loadLocal(args):
	""" tries to match one of the locally stored ontologies - just returns the full path
		(loading happens in main method)
	 """
	ontologies = get_localontologies()
	if ontologies:
		if args:
			success = False
			for each in ontologies:
				if args[0] in each:
					print "==> match: %s" % each
					args = [ONTOSPY_LOCAL + "/" + each]
					success = True
					return args
			if not success:
				print "No matching ontology name found."
				raise SystemExit, 1
		else:
			counter = 0
			for file in ontologies:
				counter += 1
				print bcolors.BLUE, "[%d]" % counter,  bcolors.ENDC, file
			while True:
				var = raw_input("\nWhich ontology? (q=exit, number=load)\n")
				if var == 'q':
					raise SystemExit, 1
				try:
					var = int(var)  # it's a string
				except:
					var = 0
				if var in range(1, len(ontologies)+1):
					args = [ONTOSPY_LOCAL + "/" + ontologies[var-1]]
					return args
			
	else:
		raise SystemExit, 1




def action_setupHomeFolder():
	""" creates the ~/.ontospy dir where data will be added """
	dosetup = True
	
	if os.path.exists(ONTOSPY_LOCAL):
		var = raw_input("Ontospy folder already exists. Reset? (y/n)")
		if var == "y":
			shutil.rmtree(ONTOSPY_LOCAL)
			dosetup = True
		else:
			var == "n"
			dosetup = False
		print var
	
	if dosetup == True:
		os.mkdir(ONTOSPY_LOCAL)		
		# copy schemas in this folder 
		onlyfiles = [ f for f in os.listdir(ONTOSPY_DEFAULT_SCHEMAS_DIR) if os.path.isfile(os.path.join(ONTOSPY_DEFAULT_SCHEMAS_DIR,f)) ]
		for file in onlyfiles:
			if not file.startswith("."):
				print ".. copied <%s>" % file 
				shutil.copy(ONTOSPY_DEFAULT_SCHEMAS_DIR+file, ONTOSPY_LOCAL)
				
		var = raw_input("=====\nDo caching? This will speed up loading time considerably. (y/n)")
		if var == "y":
			ontologies = get_localontologies()
			for onto in ontologies:
				fullpath = ONTOSPY_LOCAL + "/" + onto
				do_pickle_ontology(fullpath)

			print "===COMPLETED==="		
				
		else:
			var == "n"
			print var		






	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e



	

