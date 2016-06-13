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

from colorama import Fore, Style


from . import *  # imports __init__
from ._version import *
from .actions import *
from .core.graph import Graph
from .core.util import *




SHELL_EXAMPLES = """
Quick Examples:
  > ontospy http://xmlns.com/foaf/spec/    # ==> prints info about FOAF
  > ontospy http://xmlns.com/foaf/spec/ -i # ==> prints info and save local copy
  > ontospy http://xmlns.com/foaf/spec/ -g # ==> exports ontology data into a github gist

  For more, visit ontospy.readthedocs.org

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

	parser.add_option("-l", "",
			action="store_true", default=False, dest="_library",
			help="LIBRARY: select ontologies saved in the local library")

	parser.add_option("-v", "",
			action="store_true", default=False, dest="labels",
			help="VERBOSE: show entities labels as well as URIs")

	parser.add_option("-b", "",
			action="store_true", default=False, dest="_bootstrap",
			help="BOOTSTRAP: save some sample ontologies into the local library")

	parser.add_option("-i", "",
			action="store_true", default=False, dest="_import",
			help="IMPORT: save a file/folder/url into the local library")

	parser.add_option("-w", "",
			action="store_true", default=False, dest="_web",
			help="IMPORT-FROM-REPO: import from an online directory")

	parser.add_option("-e", "",
			action="store_true", default=False, dest="_export",
			help="EXPORT: export a model into another format (e.g. html)")

	parser.add_option("-g", "",
			action="store_true", default=False, dest="_gist",
			help="EXPORT-AS-GIST: export output as a Github Gist.")


	opts, args = parser.parse_args()

	return opts, args, parser







def main():
	""" command line script """

	printDebug("OntoSpy " + VERSION, "comment")
	opts, args, parser = parse_options()
	sTime = time.time()

	get_or_create_home_repo()

	print_opts = {
					'labels' : opts.labels,
				}


	# default behaviour: launch shell
	if not (args or opts._library or opts._import or opts._web or opts._export or opts._gist) and not opts._bootstrap:
		from shell import Shell, STARTUP_MESSAGE
		Shell()._clear_screen()
		print(STARTUP_MESSAGE)
		Shell().cmdloop()
		raise SystemExit(1)


	# select a model from the local ontologies
	elif opts._export or opts._gist:
		# if opts._gist and not opts._export:
		# 	printDebug("WARNING: the -g option must be used in combination with -e (=export)")
		# 	sys.exit(0)
		import webbrowser
		url = action_export(args, opts._gist)
		if url:# open browser
			webbrowser.open(url)

		# continue and print(timing at bottom )



	# select a model from the local ontologies (assuming it's not opts._export)
	elif opts._library:
		filename = actionSelectFromLocal()
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
		printDebug("----------\n" + "Completed (note: load a local model by typing `ontospy -l`)", "comment")

	# import an ontology (ps implemented in both .ontospy and .extras)
	elif opts._import:
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
		action_webimport_select()
		raise SystemExit(1)




	# last case: a new URI/path is passed
	# load the ontology when a uri is passed manually
	elif args:
		printDebug("----------\nYou passed the argument: <%s>" % str(args[0]), "comment")
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
