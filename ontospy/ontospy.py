# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTOSPY
Copyright (c) 2013-2016 __Michele Pasin__ <http://www.michelepasin.org>.
All rights reserved.

Run it from the command line by passing it an ontology URI,
or check out the help:

>>> python ontospy.py -h

More info in the README file.

"""

from __future__ import print_function

import sys, os, time, optparse, os.path, shutil, requests

try:
	import cPickle
except ImportError:
	import pickle as cPickle

try:
	import urllib2
except ImportError:
	import urllib as urllib2

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

from colorama import Fore, Style


from . import *  # imports __init__
from ._version import *
from .actions import *
from .core.graph import Graph
from .core.util import *




SHELL_EXAMPLES = """
Quick Examples:

  > ontospy ~/Desktop/mymodel.rdf          # ==> inspect a local RDF file
  > ontospy -l                             # ==> list ontologies available in the local library
  > ontospy -s http://xmlns.com/foaf/spec/ # ==> download FOAF vocabulary and save it in library

More info: <ontospy.readthedocs.org>
------------
"""




##################
#
#  COMMAND LINE MAIN METHODS
#
##################






def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.

	https://docs.python.org/2/library/optparse.html

	note: invoke help with `parser.print_help()`

	"""

	class MyParser(optparse.OptionParser):
		def format_epilog(self, formatter):
			return self.epilog

	parser = MyParser(usage=USAGE, version=VERSION, epilog=SHELL_EXAMPLES)

	parser.add_option("-r", "",
			action="store_true", default=False, dest="_shell",
			help="REPL: launch the interactive shell.")

	parser.add_option("-l", "",
			action="store_true", default=False, dest="_library",
			help="LIBRARY: list ontologies saved in the local library.")

	parser.add_option("-e", "",
			action="store_true", default=False, dest="labels",
			help="VERBOSE: show entities labels as well as URIs.")

	parser.add_option("-b", "",
			action="store_true", default=False, dest="_bootstrap",
			help="BOOTSTRAP: get started with some widely used ontologies.")

	parser.add_option("-s", "",
			action="store_true", default=False, dest="_save",
			help="SAVE: save a file/folder/url into the local library.")

	parser.add_option("-i", "",
			action="store_true", default=False, dest="_web",
			help="IMPORT: import a vocabulary from an online directory.")

	parser.add_option("-v", "",
			action="store_true", default=False, dest="_export",
			help="VISUALIZE: create a graphical representation of a vocabulary.")

	parser.add_option("-g", "",
			action="store_true", default=False, dest="_gist",
			help="EXPORT-AS-GIST: save visualization online as a Github Gist.")


	opts, args = parser.parse_args()

	if not args and not (opts._bootstrap or opts._export or opts._gist or opts._save
						 or opts._library or opts._shell or opts._web):
		parser.print_help()
		sys.exit(0)

	return opts, args, parser







def main():
	""" command line script """

	printDebug("OntoSpy " + VERSION, "important")
	printDebug("Local library: '%s'" % get_home_location())
	printDebug("------------")

	opts, args, parser = parse_options()
	sTime = time.time()

	get_or_create_home_repo()

	print_opts = {
					'labels' : opts.labels,
				}

	# -s launch shell
	if opts._shell:
		from .shell import Shell, STARTUP_MESSAGE
		Shell()._clear_screen()
		print(STARTUP_MESSAGE)
		Shell().cmdloop()
		raise SystemExit(1)

	#
	# if not (args or opts._library or opts._save or opts._web or opts._export or opts._gist) and not opts._bootstrap:
    #


	# select a model from the local ontologies
	elif opts._export or opts._gist:
		# if opts._gist and not opts._export:
		# 	printDebug("WARNING: the -g option must be used in combination with -e (=export)")
		# 	sys.exit(0)
		import webbrowser
		url = action_visualize(args, opts._gist)
		if url:# open browser
			webbrowser.open(url)

		# continue and print(timing at bottom )



	# select a model from the local ontologies (assuming it's not opts._export)
	elif opts._library:
		filename = action_listlocal()
		if filename:
			g = get_pickled_ontology(filename)
			if not g:
				g = do_pickle_ontology(filename)
			shellPrintOverview(g, print_opts)
			# printDebug("----------\n" + "Completed", "comment")
		# continue and print(timing at bottom )


	# bootstrap local repo
	elif opts._bootstrap:
		action_bootstrap()

	# import an ontology (ps implemented in both .ontospy and .extras)
	elif opts._save:
		if not args:
			printDebug("WARNING: please specify a file/folder/url to import into local library.")
			sys.exit(0)
		_location = args[0]
		if os.path.isdir(_location):
			res = action_import_folder(_location)
		else:
			res = action_import(_location)
		if res:
			printDebug("----------\n" + "Completed (note: load a local model by typing `ontospy -l`)", "comment")
		# continue and print(timing at bottom)



	elif opts._web:
		action_webimport()
		raise SystemExit(1)




	# last case: a new URI/path is passed
	# load the ontology when a uri is passed manually
	elif args:
		printDebug("You passed the argument: <%s>" % str(args[0]), "comment")
		g = Graph(args[0])
		shellPrintOverview(g, print_opts)

	# finally: print(some stats.... )
	eTime = time.time()
	tTime = eTime - sTime
	printDebug("\n----------\n" + "Time:	   %0.2fs" %  tTime, "comment")




if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
