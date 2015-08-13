
# docs:
# https://docs.python.org/2/library/cmd.html
# https://hg.python.org/cpython/file/2.7/Lib/cmd.py
# http://pymotw.com/2/cmd/

import os, cmd, random, urllib2, shutil, platform
from colorama import Fore, Back, Style

# Colorama: https://pypi.python.org/pypi/colorama
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

import ontospy
from libs.util import *
from libs.quotes import QUOTES


class Shell(cmd.Cmd):
	"""Simple command processor example."""

	prompt = Fore.BLUE + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL
	intro = "Type 'help' to get started. Use TAB to explore commands."

	doc_header = 'Commands'
	misc_header = 'Miscellaneous'
	undoc_header = 'Undocumented commands'
	
	ruler = '-'
	
	def emptyline(self):
		""" override default behaviour of running last command """
		pass
		
	def __init__(self):
		 """
		 """
		 # useful vars
		 self.LOCAL = ontospy.ONTOSPY_LOCAL
		 self.ontologies = ontospy.get_localontologies()
		 self.current = None
		 
		 cmd.Cmd.__init__(self)


	# HELPER METHODS
	# --------	

	def _get_prompt(self, stringa=""):
		""" changes the prompt contextually """
		if stringa:
			temp1 = Fore.RED + '%s' % stringa 
			temp2 = '<OntoSPy: %s>: ' % temp1
			return Fore.BLUE + Style.BRIGHT + temp2 + Style.RESET_ALL
		else:
			return Fore.BLUE + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL

	def _clear_screen(self):
		""" http://stackoverflow.com/questions/18937058/python-clear-screen-in-shell """
		if platform.system() == "Windows":
			tmp = os.system('cls') #for window
		else:
			tmp = os.system('clear') #for Linux
		return True

	def _select_ontology(self, line):
		# if 
		try:
			var = int(line)	 # it's a string
			if var in range(1, len(self.ontologies)+1):
				self._load_ontology(self.ontologies[var-1])
		except:
			if line in self.ontologies:
				self._load_ontology(line)
			else:
				success = False
				for each in self.ontologies:
					if line in each:
						print "==> match: %s" % each
						self._load_ontology(each)
						success = True
						break
				if not success:		
					print "not found"
					
	def _list_ontologies(self):
		counter = 0
		for file in self.ontologies:
			counter += 1
			print Fore.BLUE + Style.BRIGHT + "[%d]" % counter,	Fore.RED, file, Style.RESET_ALL				


	def _load_ontology(self, filename):
		""" loads an ontology from the local repository 
			note: if the ontology does not have a cached version, it is created
		"""
		fullpath = self.LOCAL + "/" + filename		
		g = ontospy.get_pickled_ontology(fullpath)
		if not g:
			g = ontospy.get_pickled_ontology(fullpath)
		self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		self._clear_screen()
		print "Loaded ", self.current['fullpath']
		g.printStats()
		self.prompt = self._get_prompt(filename)


	def _selectFromList(self, _list):
		""" generic method that lets users pick an item from a list via raw_input """
		if len(_list) == 1: # if by any chance there's no need to select a choice
			return _list[0]
		print "%d matching results: " % len(_list)
		counter = 1
		for el in _list:
			print Fore.BLUE + Style.BRIGHT + "[%d] " % counter, Style.RESET_ALL, el.uri
			counter += 1
		var = raw_input("Please select one entity: ")
		try:
			var = int(var)
			return _list[var-1]
		except:
			print "Selection no valid"
			return None
			


	def _select_class(self, line):			
		# try to match a class and load it
		g = self.current['graph']
		if line.isdigit():
			line =	int(line)
		out = g.getClass(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out)
				if choice:
					choice.describe()
			else:
				out.describe()
		else:
			print "not found"


	def _select_property(self, line):			
		# try to match a class and load it
		g = self.current['graph']
		if line.isdigit():
			line =	int(line)
		out = g.getProperty(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out)
				if choice:
					choice.describe()
			else:
				out.describe()
		else:
			print "not found"
			
			
	def _triples(self, g, line=None):
		if not line:
			# show ontology annotations
			for o in g.ontologies:
				o.printTriples()
		else:	
			if line.isdigit():
				line =	int(line)
			out = g.getEntity(line)
			if out:
				if type(out) == type([]):
					choice = self._selectFromList(out)
					if choice:
						choice.printTriples()
				else:
					out.printTriples()
			else:
				print "not found"

	def _serialize(self, g, line=None):
		if not line:
			# show ontology annotations
			for o in g.ontologies:
				self._printSerialize(o)
		else:	
			if line.isdigit():
				line =	int(line)
			out = g.getEntity(line)
			if out:
				if type(out) == type([]):
					choice = self._selectFromList(out)
					if choice:
						self._printSerialize(choice)
				else:
					self._printSerialize(out)
			else:
				print "not found"

	def _printSerialize(self, entity):
		"wrapper around main printSerialize function"
		print Fore.RED + Style.BRIGHT + entity.uri + Style.RESET_ALL
		print "-----------"
		entity.printSerialize()

	#
	# def _import_ontology(self, location):
	#	""" imports an ontology from the web, or from an external file, and adds it to the repo
	#		note: create the cached version too
	#	"""
	#	# 1) extract file from location and save locally
	#	fullpath = ""
	#	try:
	#		if location.startswith("http://"):
	#			headers = "Accept: application/rdf+xml"
	#			req = urllib2.Request(location, headers)
	#			res = urllib2.urlopen(req)
	#			final_location = res.geturl()  # after 303 redirects
	#			print "Loaded <%s>" % final_location
	#			filename = final_location.split("/")[-1] or final_location.split("/")[-2]
	#			fullpath = self.LOCAL + "/" + filename
	#
	#			file_ = open(fullpath, 'w')
	#			file_.write(res.read())
	#			file_.close()
	#
	#		else:
	#			filename = location.split("/")[-1] or location.split("/")[-2]
	#			fullpath = self.LOCAL + "/" + filename
	#			shutil.copy(location, fullpath)
	#		print "Saving local copy..."
	#	except:
	#		print "Error retrieving file. Please make sure <%s> is a valid location." % location
	#		if os.path.exists(fullpath):
	#			os.remove(fullpath)
	#		return None
	#
	#	# 2) check if valid RDF and cache it
	#	try:
	#		g = ontospy.Graph(fullpath)
	#		self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
	#		print "Loaded ", self.current['fullpath']
	#		self.prompt = self._get_prompt(filename)
	#	except:
	#		g = None
	#		if os.path.exists(fullpath):
	#			os.remove(fullpath)
	#		print "Error parsing file. Please make sure %s contains valid RDF." % location
	#
	#	if g:
	#		self.ontologies = ontospy.get_localontologies()
	#		ontospy.do_pickle_ontology(fullpath, g)
	#
	#	# finally...
	#	return g



	# COMMANDS
	# --------
	# NOTE: all commands should start with 'do_' and must pass 'line'


	# def do_ontologies(self, line):
	#	""" List the available ontologies in the local repository. """
	#	self._list_ontologies()

		
	def do_current(self, line):
		""" List the ontology currently loaded""" 
		 # {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		if self.current:
			print self.current['file']
		else:
			print "No ontology loaded. Use the 'ontology' command"


	def do_triples(self, line):
		""" Triples is a context aware command.
			If no ontology > no triples \n
			if ontology = show annotations \n
			if entity = show triples 
		""" 
		# print "If no ontology > no triples \n if ontology = show annotations \n if entity = show triples"
		if self.current:
			g = self.current['graph']			
			self._triples(g, line)		
		else:
			print "Please select an ontology first."


	def do_serialize(self, line):
		""" Serialize an entity into an RDF format. 
		\nValid options are: xml, n3, turtle, nt, pretty-xml, trix @todo
		""" 
		# print "If no ontology > no triples \n if ontology = show annotations \n if entity = show triples"
		if self.current:
			g = self.current['graph']			
			self._serialize(g, line)		
		else:
			print "Please select an ontology first."


	def do_classes(self, line):
		if not self.current:
			print "Please select an ontology first"
		else: # self.current exists
			g = self.current['graph']
			g.printClassTree(showids=True, labels=False)			

	def do_properties(self, line):
		if not self.current:
			print "Please select an ontology first"
		else: # self.current exists
			g = self.current['graph']
			g.printPropertyTree(showids=True, labels=False)


	# def complete_list(self, text, line, begidx, endidx):
	# 	cmds = ['ontologies', 'classes', 'properties']
	# 	if not text:
	# 		completions = cmds
	# 	else:
	# 		completions = [ f
	# 						for f in cmds
	# 						if f.startswith(text)
	# 						]
	# 	return completions

	#
	# def do_import(self, line):
	#	""" Import an ontology into the local repository. Either from:
	#	\nweb: eg import http://xmlns.com/foaf/spec/index.rdf
	#	\nlocal file: eg /home/Desktop/foaf.rdf
	#	\nlocal folder: eg /home/Desktop/models/. """
	#	if not line:
	#		print "Please specify a URI or local path to import from"
	#	else:
	#		self._import_ontology(line)
	
	# SELECT OPERATIONS
			
	def do_ontology(self, line):
		"""Select an ontology""" 
		
		if not self.ontologies:
			print "No ontologies in the local repository. Use the 'import' command. "
		else:
			if line:
				self._select_ontology(line)
			else:
				print "Please select an ontology"
				self._list_ontologies()
				
	def do_class(self, line):
		"""Select a class""" 
		if not self.current:	
			print "Please select an ontology first"
		elif line:
			self._select_class(line)
		else:
			print "Enter a class name or number, or use <tab> to autocomplete"

	def do_property(self, line):
		"""Select a property""" 
		if not self.current:	
			print "Please select an ontology first"
		elif line:
			self._select_property(line)
		else:
			print "Enter a class name or number, or use <tab> to autocomplete"



	def complete_ontology(self, text, line, begidx, endidx):
		"""completion for select command"""
		
		options = self.ontologies[:]

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions						
			
	
	def complete_class(self, text, line, begidx, endidx):
		"""completion for select command"""
		
		if self.current:
			g = self.current['graph']
			options = [x.locale for x in g.classes]
		else:
			options = []

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions		


	def complete_property(self, text, line, begidx, endidx):
		"""completion for select command"""
		
		if self.current:
			g = self.current['graph']
			options = [x.locale for x in g.properties]
		else:
			options = []

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	

				
	def do_annotations(self, line):
		"Show annotations for current ontology"
		if not self.current:
			print "No ontology loaded"
		else:
			g = self.current['graph']
			for o in g.ontologies:
				o.printTriples()
	
		

	def do_delete(self, line):
		""" Delete an ontology from the local repository. """ 
		if not line:
			print "Please specify an ontology name" 
		else:
			fullpath = self.LOCAL + "/" + line
			if os.path.exists(fullpath):
				var = raw_input("Are you sure? (y/n)")
				if var == "y":
					os.remove(fullpath)
					if os.path.exists(fullpath + ".pickle"):
						os.remove(fullpath + ".pickle")
					self.ontologies = ontospy.get_localontologies()
					print "Deleted %s" % fullpath
			else:
				print "Not found"

	def complete_delete(self, text, line, begidx, endidx):
		if not text:
			completions = self.ontologies[:]
		else:
			completions = [ f
							for f in self.ontologies
							if f.startswith(text)
							]
		return completions
							

	def do_top(self, line):
		"Unload any ontology and go back to top level"
		self.current = None
		self.prompt = self._get_prompt()
						
	def do_quit(self, line):
		"Exit OntoSPy shell"
		return True
		
	def default(self, line):
		"default message when a command is not recognized"
		foo = ["Wow first time I hear that", "That looks like the wrong command", "Are you sure you mean that? try 'help' for some suggestions"]
		print(random.choice(foo))
	
	def do_inspiration(self, line):
		_quote = random.choice(QUOTES)
		# print _quote['source']
		print Style.DIM + unicode(_quote['text'])
		print Style.BRIGHT + unicode(_quote['source']) + Style.RESET_ALL


if __name__ == '__main__':
	Shell().cmdloop()