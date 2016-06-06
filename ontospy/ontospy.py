# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTOSPY
Copyright (c) 2013-2016 __Michele Pasin__ <michelepasin.org>.
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
from .core.graph import Graph
from .core.util import *




SHELL_EXAMPLES = """
Quick Examples:
  > ontospy http://xmlns.com/foaf/spec/    # ==> prints info about FOAF
  > ontospy http://xmlns.com/foaf/spec/ -i # ==> prints info and save local copy
  > ontospy http://xmlns.com/foaf/spec/ -g # ==> exports ontology data into a github gist

  For more, visit ontospy.readthedocs.org

"""





# ===========
# COMMAND LINE ACTIONS
# ===========




def actionSelectFromLocal():
	" select a file from the local repo "

	options = get_localontologies()

	counter = 1
	printDebug("------------------", 'comment')
	if not options:
		printDebug("Your local library is empty. Use 'ontospy -i <uri>' to add more ontologies to it.")
	else:
		data = []
		for x in options:
			data += [ Fore.BLUE + Style.BRIGHT + "[%d] " % counter + Style.RESET_ALL + x + Style.RESET_ALL]
			counter += 1

		# from util.
		pprint2columns(data)

		while True:
			printDebug("------------------\nSelect a model by typing its number: (q=quit)", "important")
			var = raw_input()
			if var == "q":
				return None
			else:
				try:
					_id = int(var)
					ontouri = options[_id - 1]
					printDebug("You selected:", "comment")
					printDebug("---------\n" + ontouri + "\n---------", "red")
					return ontouri
				except:
					printDebug("Please enter a valid number.", "comment")
					continue



def action_import(location, verbose=True, lock=None):
	"""import files into the local repo
		<lock> was used by the Threaded routine *now removed* 2016-04-24

	"""

	location = str(location) # prevent errors from unicode being passed

	# 1) extract file from location and save locally
	ONTOSPY_LOCAL_MODELS = get_home_location()
	fullpath = ""
	try:
		if location.startswith("www."): #support for lazy people
			location = "http://%s" % str(location)
		if location.startswith("http"):
			# print("here")
			headers = {'Accept': "application/rdf+xml"}
			req = urllib2.Request(location, headers=headers)
			res = urllib2.urlopen(req)
			final_location = res.geturl()  # after 303 redirects
			printDebug("Saving data from <%s>" % final_location, "green")
			# filename = final_location.split("/")[-1] or final_location.split("/")[-2]
			filename = location.replace("http://", "").replace("/", "_")
			if not filename.lower().endswith(('.rdf', '.owl', '.rdfs', '.ttl', '.n3')):
				filename = filename + ".rdf"
			fullpath = ONTOSPY_LOCAL_MODELS + "/" + filename # 2016-04-08
			# fullpath = ONTOSPY_LOCAL_MODELS + filename

			# print("==DEBUG", final_location, "**", filename,"**", fullpath)

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
		# print("Saved local copy")
	except:
		printDebug("Error retrieving file. Please make sure <%s> is a valid location." % location, "important")
		if os.path.exists(fullpath):
			os.remove(fullpath)
		return None

	try:
		g = Graph(fullpath, verbose=verbose)
		printDebug("----------")
	except:
		g = None
		if os.path.exists(fullpath):
			os.remove(fullpath)
		printDebug("Error parsing file. Please make sure %s contains valid RDF." % location, "important")

	if g:
		printDebug("Caching...", "red")
		do_pickle_ontology(filename, g)
		printDebug("----------\n...completed!", "important")

	# finally...
	return g





def action_import_folder(location):
	"""Try to import all files from a local folder"""

	if os.path.isdir(location):
		onlyfiles = [ f for f in os.listdir(location) if os.path.isfile(os.path.join(location,f)) ]
		for file in onlyfiles:
			if not file.startswith("."):
				filepath = os.path.join(location,file)
				print(Fore.RED + "\n---------\n" + filepath + "\n---------" + Style.RESET_ALL)
				return action_import(filepath)
	else:
		printDebug("Not a valid directory", "important")
		return None





def action_bootstrap():
	"""Bootstrap the local REPO with a few cool ontologies"""
	printDebug("--------------")
	printDebug("The following ontologies will be imported:")
	printDebug("--------------")
	count = 0
	for s in BOOTSTRAP_ONTOLOGIES:
		count += 1
		print(count, "<%s>" % s)

	printDebug("--------------")
	printDebug("Note: this operation may take several minutes.")
	printDebug("Are you sure? [Y/N]")
	var = raw_input()
	if var == "y" or var == "Y":
		for uri in BOOTSTRAP_ONTOLOGIES:
			try:
				printDebug("--------------")
				action_import(uri, verbose=False)
			except:
				printDebug("OPS... An Unknown Error Occurred - Aborting Installation")
		return True
	else:
		printDebug("--------------")
		printDebug("Goodbye")
		return False







def action_webimport_select():
	""" select from the available online directories for import """
	DIR_OPTIONS = {1 : "http://lov.okfn.org", 2 : "http://prefix.cc/popular/"}
	selection = None
	while True:
		printDebug("----------")
		text = "Please select which online directory to scan: (enter=quit)\n"
		for x in DIR_OPTIONS:
			text += "%d) %s\n" % (x, DIR_OPTIONS[x])
		var = raw_input(text + "> ")
		if var == "q" or var == "":
			return None
		else:
			try:
				selection = int(var)
				test = DIR_OPTIONS[selection]  #throw exception if number wrong
				break
			except:
				printDebug("Invalid selection. Please try again.", "important")
				continue


	printDebug("----------")
	text = "Search for a specific keyword? (enter=show all)\n"
	var = raw_input(text + "> ")
	keyword = var

	try:
		if selection == 1:
			action_webimport_LOV(keyword=keyword)
		elif selection == 2:
			action_webimport_PREFIXCC(keyword=keyword)
	except:
		printDebug("Sorry, the online repository seems to be unreachable.")

	return True



def action_webimport_LOV(baseuri="http://lov.okfn.org/dataset/lov/api/v2/vocabulary/list", keyword=""):
	"""
	2016-03-02: import from json list
	"""

	printDebug("----------\nReading source... <%s>" % baseuri)
	query = requests.get(baseuri, params={})
	all_options = query.json()
	options = []

	# pre-filter if necessary
	if keyword:
		for x in all_options:
			if keyword in x['uri'].lower() or keyword in x['titles'][0]['value'].lower() or keyword in x['nsp'].lower():
				options.append(x)
	else:
		options = all_options

	printDebug("----------\n%d results found.\n----------" % len(options))

	if options:
		# display:
		counter = 1
		for x in options:
			uri, title, ns = x['uri'], x['titles'][0]['value'], x['nsp']
			# print("%s ==> %s" % (d['titles'][0]['value'], d['uri']))

			print(Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + uri + " ==> ", Fore.RED + title, Style.RESET_ALL)

			counter += 1

		while True:
			var = raw_input(Style.BRIGHT + "=====\nSelect ID to import: (q=quit)\n" + Style.RESET_ALL)
			if var == "q":
				break
			else:
				try:
					_id = int(var)
					ontouri = options[_id - 1]['uri']
					print(Fore.RED + "\n---------\n" + ontouri + "\n---------" + Style.RESET_ALL)
					action_import(ontouri)
				except:
					print("Error retrieving file. Import failed.")
					continue



def action_webimport_PREFIXCC(keyword=""):
	"""
	List models from web catalog (prefix.cc) and ask which one to import
	2015-10-10: originally part of main ontospy; now standalone only
	"""

	from extras.import_web import getCatalog
	options = getCatalog(query=keyword)

	counter = 1
	for x in options:
		print(Fore.BLUE + Style.BRIGHT + "[%d]" % counter, Style.RESET_ALL + x[0] + " ==> ", Fore.RED +	 x[1], Style.RESET_ALL)
		# print(Fore.BLUE + x[0], " ==> ", x[1])
		counter += 1

	while True:
		var = raw_input(Style.BRIGHT + "=====\nSelect ID to import: (q=quit)\n" + Style.RESET_ALL)
		if var == "q":
			break
		else:
			try:
				_id = int(var)
				ontouri = options[_id - 1][1]
				print(Fore.RED + "\n---------\n" + ontouri + "\n---------" + Style.RESET_ALL)
				action_import(ontouri)
			except:
				print("Error retrieving file. Import failed.")
				continue





def action_export(args, save_gist, fromshell=False):
	"""
	export model into another format eg html, d3 etc...
	<fromshell> : the local name is being passed from ontospy shell
	"""

	from extras import exporter

	# select from local ontologies:
	if not(args):
		ontouri = actionSelectFromLocal()
		if ontouri:
			islocal = True
		else:
			raise SystemExit(1)
	elif fromshell:
		ontouri = args
		islocal = True
	else:
		ontouri = args[0]
		islocal = False


	# select a visualization
	viztype = exporter._askVisualization()
	if not viztype:
		return None
		# raise SystemExit, 1


	# get ontospy graph
	if islocal:
		g = get_pickled_ontology(ontouri)
		if not g:
			g = do_pickle_ontology(ontouri)
	else:
		g = Graph(ontouri)



	# viz DISPATCHER
	if viztype == 1:
		contents = exporter.htmlBasicTemplate(g, save_gist)

	elif viztype == 2:
		contents = exporter.interactiveD3Tree(g, save_gist)


	# once viz contents are generated, save file locally or on github
	if save_gist:
		urls = exporter.saveVizGithub(contents, ontouri)
		printDebug("...documentation saved on GitHub!", "comment")
		printDebug("Gist: " + urls['gist'], "important")
		printDebug("Blocks Gist: " + urls['blocks'], "important")
		printDebug("Full Screen Blocks Gist: " + urls['blocks_fullwin'], "important")
		url = urls['blocks'] # defaults to full win
	else:
		url = exporter.saveVizLocally(contents)
		printDebug("...documentation generated! [%s]" % url, "comment")

	return url






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
	if not args and not opts._library and not opts._import and not opts._web and not opts._export and not opts._gist and not opts._bootstrap:
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
