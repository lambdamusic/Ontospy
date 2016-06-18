# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""
UTILITY TO MANAGE THE LOCAL ONTOSPY LIBRARY

Copyright (c) 2015 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""

from __future__ import print_function

MODULE_VERSION = 0.3
USAGE = "ontospy-manager [options]"


import time, optparse, os, rdflib, sys, datetime
from ConfigParser import SafeConfigParser


from . import *
from . import ontospy
from .core.graph import Graph
from .core.util import *






def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.

	https://docs.python.org/2/library/optparse.html

	"""

	parser = optparse.OptionParser(usage=USAGE, version=ontospy.VERSION)


	parser.add_option("-c", "",
			action="store_true", default=False, dest="cache",
			help="CACHE: force caching of the local library (for faster loading).")

	parser.add_option("-u", "",
			action="store_true", default=False, dest="_setup",
			help="UPDATE: enter new path for the local library.")

	parser.add_option("-d", "",
			action="store_true", default=False, dest="_delete",
			help="DELETE: remove a single ontology file from the local library.")

	parser.add_option("-e", "",
			action="store_true", default=False, dest="erase",
			help="ERASE: reset the local library (delete all files).")


	opts, args = parser.parse_args()

	if opts._setup and not args:
		printDebug("Please specify a new location for the local library.", 'important')
		printDebug("E.g. 'ontospy-manager -u /Users/john/ontologies'", 'tip')
		sys.exit(0)

	if not args and not opts._setup and not opts.cache and not opts.erase and not opts._delete:
		parser.print_help()
		sys.exit(0)

	return opts, args




def main():
	""" command line script """

	printDebug("OntoSpy " + ontospy.VERSION, "important")
	printDebug("Local library: '%s'" % ontospy.get_home_location())
	printDebug("------------")
	opts, args = parse_options()

	if not opts._setup:
		ontospy.get_or_create_home_repo()

	# move local lib
	if opts._setup:
		_location = args[0]
		if _location.endswith("/"):
			# dont need the final slash
			_location = _location[:-1]
		output = ontospy.action_update_library_location(_location)
		if output:
			printDebug("Note: no files have been moved or deleted (this has to be done manually)", "comment")
			printDebug("----------\n" + "New location: '%s'" % _location, "important")

		else:
			printDebug("----------\n" + "Please specify an existing folder path.", "important")
		raise SystemExit(1)


	# reset local stuff
	if opts._delete:
		res = ontospy.actions_delete()
		raise SystemExit(1)

	# reset local stuff
	if opts.erase:
		ontospy.action_erase()
		raise SystemExit(1)

	# cache local ontologies
	if opts.cache:
		sTime = time.time()
		ontospy.action_cache()
		# finally: print(some stats....)
		eTime = time.time()
		tTime = eTime - sTime
		printDebug("-" * 10)
		printDebug("Time:	   %0.2fs" %  tTime, "comment")
		raise SystemExit(1)



if __name__ == '__main__':
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt as e: # Ctrl-C
		raise e
