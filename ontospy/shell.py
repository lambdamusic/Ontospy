
# docs:
# https://docs.python.org/2/library/cmd.html
# https://hg.python.org/cpython/file/2.7/Lib/cmd.py
# http://pymotw.com/2/cmd/

import os, cmd, random, urllib2, shutil
from colorama import Fore, Back, Style

# Colorama: https://pypi.python.org/pypi/colorama
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

import ontospy
from libs.util import *


class Shell(cmd.Cmd):
	"""Simple command processor example."""

	prompt = Fore.BLUE + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL
	intro = "Ready to go. Type 'help' to get started. Use TAB to explore commands."

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
		g = ontospy.get_picked_ontology(fullpath)
		if not g:
			g = ontospy.do_pickle_ontology(fullpath)
		self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		print "Loaded ", self.current['fullpath']
		self.prompt = self._get_prompt(filename)


	def _select_class(self, line):			
		# try to match a class and load it
		g = self.current['graph']
		if line.isdigit():
			line =	int(line)
		out = g.getClass(line)
		if out:
			if type(out) == type([]):
				out[0].describe()
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
				out[0].describe()
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
					print "==> first match: %s" % out[0]
					out[0].printTriples()
				else:
					out.printTriples()
			else:
				print "not found"


	def _import_ontology(self, location):
		""" imports an ontology from the web, or from an external file, and adds it to the repo
			note: create the cached version too
		"""
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
				fullpath = self.LOCAL + "/" + filename
	
				file_ = open(fullpath, 'w')
				file_.write(res.read())
				file_.close()
				
			else:
				filename = location.split("/")[-1] or location.split("/")[-2]
				fullpath = self.LOCAL + "/" + filename
				shutil.copy(location, fullpath)
			print "Saving local copy..."	
		except:
			print "Error retrieving file. Please make sure <%s> is a valid location." % location
			if os.path.exists(fullpath):
				os.remove(fullpath)
			return None
		
		# 2) check if valid RDF and cache it
		try:
			g = ontospy.Graph(fullpath)
			self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
			print "Loaded ", self.current['fullpath']
			self.prompt = self._get_prompt(filename)
		except:
			g = None
			if os.path.exists(fullpath):
				os.remove(fullpath)
			print "Error parsing file. Please make sure %s contains valid RDF." % location
		
		if g:
			self.ontologies = ontospy.get_localontologies()
			ontospy.do_pickle_ontology(fullpath, g) 

		# finally...
		return g



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
			print "No ontology loaded. Use the 'load' command"


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

	def do_list(self, line):
		"""List is a context aware command.
			\nIf no ontology > list ontologies	
			\nIf ontology > list 'classes' [default] or 'properties'
		""" 
		if line == "ontologies":
			self._list_ontologies()
		elif not self.current:
			if line:
				print "Please select an ontology first :"
			self._list_ontologies()
		else: # self.current exists
			g = self.current['graph']
			if line == "properties": 
				g.printPropertyTree(showids=True, labels=False)
			if not line or line == "classes": 
				g.printClassTree(showids=True, labels=False)		
			else:
				print "Not a valid argument"

	def complete_list(self, text, line, begidx, endidx):
		cmds = ['ontologies', 'classes', 'properties']
		if not text:
			completions = cmds
		else:
			completions = [ f
							for f in cmds
							if f.startswith(text)
							]
		return completions

		

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
		

	def do_import(self, line):
		""" Import an ontology from the web (or local file) into the local repository. """ 
		if not line:
			print "Please specify a URI or local path to import from"	
		else:
			self._import_ontology(line)
					
			

	def do_select_class(self, line):
		"""Select a class""" 
		if not self.current:	
			print "Please select an ontology first"
		else:
			# 2: class or property case
			if line:
				if len(line.split()) == 1:
					line = "class " + line
				arg, val = line.split()[0], line.split()[1]
				if arg not in ['class', 'property']:
					print "Valid arguments are 'class' [default] and 'property'"
				else:
					if arg == "class":
						self._select_class(val)
					elif arg == "property":
						self._select_property(val)



	def do_select(self, line):
		"""Select an object - context aware
		\nontology: Load one of the ontologies in the local repository. 
		""" 
		if not self.current:	
			# 1: ontology case [only from top level]
			if not line:
				print "Please specify the ontology you want to select:"		
				self._list_ontologies()
			else:
				self._select_ontology(line)
		else:
			# 2: class or property case
			if line:
				if len(line.split()) == 1:
					line = "class " + line
				arg, val = line.split()[0], line.split()[1]
				if arg not in ['class', 'property']:
					print "Valid arguments are 'class' [default] and 'property'"
				else:
					if arg == "class":
						self._select_class(val)
					elif arg == "property":
						self._select_property(val)


	def complete_select(self, text, line, begidx, endidx):
		"""context aware completion for select command"""
		
		if False:
			print "\ntext:", text # text is always the last bit: "select class cito" = cito
			print "line:", line   # line is the whole line including command
		
		if not self.current:
			options = self.ontologies[:]
		elif line.strip().startswith("select class"):
			g = self.current['graph']
			options = [x.qname for x in g.classes]
		elif line.strip().startswith("select property"):
			g = self.current['graph']
			options = [x.qname for x in g.properties]	
		else:
			options = ['class', 'property']
			
		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions						
				

	#
	# def do_classes(self, line):
	# 	"Show classes for current ontology"
	# 	if not self.current:
	# 		print "No ontology loaded"
	# 	else:
	# 		g = self.current['graph']
	# 		if not line:
	# 			g.printClassTree(showids=True, labels=False)
	# 		else:
	# 			# try to match a class and load it
	# 			if line.isdigit():
	# 				line =	int(line)
	# 			out = g.getClass(line)
	# 			if out:
	# 				if type(out) == type([]):
	# 					out[0].describe()
	# 				else:
	# 					out.describe()
	# 			else:
	# 				print "not found"
	#
	#
	# def do_properties(self, line):
	# 	"Show properties for current ontology"
	# 	if not self.current:
	# 		print "No ontology loaded"
	# 	else:
	# 		g = self.current['graph']
	# 		if not line:
	# 			g.printPropertyTree(showids=True, labels=False)
	# 		else:
	# 			# try to match a class and load it
	# 			if line.isdigit():
	# 				line =	int(line)
	# 			out = g.getProperty(line)
	# 			if out:
	# 				if type(out) == type([]):
	# 					out[0].describe()
	# 				else:
	# 					out.describe()
	# 			else:
	# 				print "not found"

				
	def do_annotations(self, line):
		"Show annotations for current ontology"
		if not self.current:
			print "No ontology loaded"
		else:
			g = self.current['graph']
			for o in g.ontologies:
				o.printTriples()
						

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



if __name__ == '__main__':
	Shell().cmdloop()