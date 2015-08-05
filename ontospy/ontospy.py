#!/usr/bin/env python
# encoding: utf-8



"""
ONTOSPY
Copyright (c) 2013-2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI. 

>>> python ontospy.py -h

More info in the README file.

"""


import sys, os, time, optparse, os.path, shutil

from libs.graph import Graph, SparqlEndpoint
from libs.util import bcolors

from _version import *






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
			action="store_true", default=False, dest="showlocal",
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

	if not opts.shell and not opts.showlocal and not opts.loadlocal and not opts.web and not opts.setup and len(args) < 1:
		parser.print_help()
		sys.exit(0)
		
	return opts, args


	
def main():
	""" command line script """
	
	print "OntoSPy " + VERSION + "\n-----------"

	# get file location
	dirname, filename = os.path.split(os.path.abspath(__file__))
	DEFAULT_SCHEMAS_DIR = dirname + "/data/schemas/"
	DEFAULT_ONTO = DEFAULT_SCHEMAS_DIR + "pizza.ttl"
	
	ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
	
	opts, args = parse_options()

	if opts.showlocal:		
		if os.path.exists(ONTOSPY_LOCAL):
			onlyfiles = [ f for f in os.listdir(ONTOSPY_LOCAL) if os.path.isfile(os.path.join(ONTOSPY_LOCAL,f)) ]
			for file in onlyfiles:
				if not file.startswith("."):
					print ONTOSPY_LOCAL + "/" + file
		else:
			print "No local repository found. Try --setup first."
		

		raise SystemExit, 1



	if opts.loadlocal:		
		args = action_loadLocal(ONTOSPY_LOCAL, args)


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
		action_setupHomeFolder(ONTOSPY_LOCAL, DEFAULT_SCHEMAS_DIR)
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
	# else: # 2015-06-24: deprecated via the test in parse_options
	#	print "Argument not provided... loading test graph: %s" % DEFAULT_ONTO
	#	g = Graph(DEFAULT_ONTO)
	
		shellPrintOverview(g, print_opts)


	# finally:	
	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	print "-" * 10 
	print "Time:	   %0.2fs" %  tTime





def action_setupHomeFolder(ONTOSPY_LOCAL, DEFAULT_SCHEMAS_DIR):
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
		onlyfiles = [ f for f in os.listdir(DEFAULT_SCHEMAS_DIR) if os.path.isfile(os.path.join(DEFAULT_SCHEMAS_DIR,f)) ]
		for file in onlyfiles:
			if not file.startswith("."):
				print ".. copied <%s>" % file 
				shutil.copy(DEFAULT_SCHEMAS_DIR+file, ONTOSPY_LOCAL)



def action_loadLocal(ONTOSPY_LOCAL, args):
	""" 2015-08-04 """
	if os.path.exists(ONTOSPY_LOCAL):
		onlyfiles = [ f for f in os.listdir(ONTOSPY_LOCAL) if os.path.isfile(os.path.join(ONTOSPY_LOCAL,f)) ]
		onlyfiles = [f for f in onlyfiles if not f.startswith(".")]
		
		if args:
			success = False
			for each in onlyfiles:
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
			for file in onlyfiles:
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
				if var in range(1, len(onlyfiles)+1):
					args = [ONTOSPY_LOCAL + "/" + onlyfiles[var-1]]
					return args
			
	else:
		print "No local repository found. Try --setup first."
		raise SystemExit, 1


	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e



	

