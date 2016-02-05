#!/usr/bin/env python


"""
OntoSPy Shell Module
michele.pasin@gmail.com

# docs:
# https://docs.python.org/2/library/cmd.html
# https://hg.python.org/cpython/file/2.7/Lib/cmd.py
# http://pymotw.com/2/cmd/

# Colorama cheatsheet: https://pypi.python.org/pypi/colorama
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

"""



import os, cmd, random, urllib2, shutil, platform
from colorama import Fore, Back, Style

from . import ontospy
from . import _version 
from .core.util import *
from .core.quotes import QUOTES





_intro_ = """******										
***											  
* OntoSPy Interactive Ontology Browser %s *
***											  
******									   """

STARTUP_MESSAGE = Style.BRIGHT + _intro_ % _version.VERSION + Style.RESET_ALL





class Shell(cmd.Cmd):
	"""Simple command processor example."""

	DEFAULT_COL = Fore.RED
	prompt = DEFAULT_COL + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL
	intro = "Type 'help' to get started, TAB to explore commands.\n"

	doc_header = 'Commands'
	misc_header = 'Miscellaneous'
	undoc_header = 'Undocumented commands'
	
	ruler = '-'
	
	def emptyline(self):
		""" override default behaviour of running last command """
		pass
		
	def __init__(self):
		 """
		 self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		 self.currentEntity = {'name' : obj.locale or obj.uri, 'object' : obj, 'type' : 'class'} 
																		# or 'property' or 'concept'
		 """
		 # useful vars
		 self.LOCAL = ontospy.ONTOSPY_LOCAL
		 self.LOCAL_MODELS = ontospy.get_home_location()
		 self.ontologies = ontospy.get_localontologies()
		 self.current = None
		 self.currentEntity = None
		 
		 cmd.Cmd.__init__(self)


	# HELPER METHODS
	# --------	

	def _get_prompt(self, onto="", entity="", default=DEFAULT_COL):
		""" changes the prompt contextually """
		if entity:
			onto = self.current['file']
			temp1_1 = default + Style.NORMAL + '%s: ' % truncate(onto, 20)
			temp1_2 = default + Style.BRIGHT + '%s' % entity
			temp2 = '<%s>: ' % (temp1_1 + temp1_2)
			return default + Style.BRIGHT + temp2 + Style.RESET_ALL
		elif onto:
			temp1 = default + '%s' % onto 
			temp2 = '<%s>: ' % temp1
			return default + Style.BRIGHT + temp2 + Style.RESET_ALL
		else:
			return default + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL
	
	
	def _print(self, ms, style="TIP"):
		""" abstraction for managing color printing """
		styles1 = {'IMPORTANT' : Style.BRIGHT, 
					'TIP': Style.DIM, 
					'URI' : Style.BRIGHT,  
					'TEXT' : Fore.GREEN, 
					'MAGENTA' : Fore.MAGENTA ,
					'BLUE' : Fore.BLUE ,
					'GREEN' : Fore.GREEN ,
					'RED' : Fore.RED ,
					'DEFAULT' : Style.DIM ,
					}
		try:
			print styles1[style] + ms + Style.RESET_ALL 
		except:
			print styles1['DEFAULT'] + ms + Style.RESET_ALL

	def _printM(self, messages):
		"""print a list of strings - for the mom used by stats printout"""
		if len(messages) == 2:
			print Style.BRIGHT + messages[0] + Style.RESET_ALL + Fore.BLUE + messages[1] + Style.RESET_ALL
		else:
			print "Not implemented"


	def _clear_screen(self):
		""" http://stackoverflow.com/questions/18937058/python-clear-screen-in-shell """
		if platform.system() == "Windows":
			tmp = os.system('cls') #for window
		else:
			tmp = os.system('clear') #for Linux
		return True


	def _printTriples(self, entity):
		""" display triples """
		self._print("----------------", "TIP")
		self._print(unicode(entity.uri) , "IMPORTANT")
		for x in entity.triples:
			self._print("=> " + unicode(x[1]) , "MAGENTA")
			self._print(".... " + unicode(x[2]) , "GREEN")
		self._print("----------------", "TIP")


	def _print_entity_intro(self, g=None, entity=None, first_time=True):
		"""after a selection, prints on screen basic info about onto or entity, plus change prompt 
		2015-10-18: removed the sound
		2016-01-18: entity is the shell wrapper around the ontospy entity
		"""
		if entity:
			self._clear_screen()
			obj = entity['object']
			self._print("Loaded %s: <%s>" % (entity['type'].capitalize(), str(obj.uri)), "TIP")
			self._print("----------------", "TIP")
			# self._print(obj.bestDescription(), "TEXT")
			if first_time:
				self.prompt = self._get_prompt(entity=self.currentEntity['name'])
		elif g:
			if first_time:
				self._clear_screen()
				# playSound(ontospy.ONTOSPY_SOUNDS)	 # new..
				self._print("Loaded graph: <" + self.current['fullpath'] + ">", 'TIP')
			g.printStats()
			if g.ontologies:
				for o in g.ontologies:
					self._print("==> Ontology URI: <%s>" % str(o.uri), "TIP")
				self._print("----------------", "TIP")
				# self._print(o.bestDescription(), "TEXT")
			if first_time:
				self.prompt = self._get_prompt(self.current['file'])


	def _printDescription(self, hrlinetop=True):
		"""generic method to print out a description"""
		if hrlinetop:
			self._print("----------------")
		NOTFOUND = "[not found]"
		if self.currentEntity:
			obj = self.currentEntity['object']
			label = obj.bestLabel() or NOTFOUND
			description = obj.bestDescription() or NOTFOUND
			self._print("Title: " + label, "TEXT")
			self._print("Description: " + description, "TEXT")
				
		else:
			for obj in self.current['graph'].ontologies:
				self._print("==> Ontology: <%s>" % str(obj.uri), "IMPORTANT")
				self._print("----------------", "TIP")
				label = obj.bestLabel() or NOTFOUND
				description = obj.bestDescription() or NOTFOUND
				self._print("Title: " + label, "TEXT")
				self._print("Description: " + description, "TEXT")
		self._print("----------------", "TIP")
		

	def _printStats(self, hrlinetop=True):
		"""
		print more informative stats about the object
		"""
		if hrlinetop:
			self._print("----------------")
		if not self.currentEntity:	# ==> ontology level 
			g = self.current['graph']			
			self._print("Ontologies......: %d" % len(g.ontologies))
			self._print("Classes.........: %d" % len(g.classes))
			self._print("Properties......: %d" % len(g.properties))
			self._print("..annotation....: %d" % len(g.annotationProperties))
			self._print("..datatype......: %d" % len(g.datatypeProperties))
			self._print("..object........: %d" % len(g.objectProperties))
			self._print("Concepts(SKOS)..: %d" % len(g.skosConcepts))
			self._print("----------------")

		elif self.currentEntity['type'] == 'class':
			x = self.currentEntity['object']
			self._printM(["Parents......[%d]  " % len(x.parents()), "%s" % "; ".join([p.qname for p in x.parents()])])
			self._printM(["\nAncestors....[%d]  " % len(x.ancestors()), "%s" % "; ".join([p.qname for p in x.ancestors()])])
			self._printM(["\nChildren.....[%d]  " % len(x.children()), "%s" % "; ".join([p.qname for p in x.children()])])
			self._printM(["\nDescendants..[%d]  " % len(x.descendants()), "%s" % "; ".join([p.qname for p in x.descendants()])])
			self._printM(["\nIn Domain of.[%d]  " % len(x.domain_of), "%s" % "; ".join([p.qname for p in x.domain_of])])
			self._printM(["\nIn Range of..[%d]  " % len(x.range_of), "%s" % "; ".join([p.qname for p in x.range_of])])
			self._printM(["\nInstances....[%d]  " % len(x.all()), "%s" % "; ".join([p.qname for p in x.all()])])
			self._print("----------------")
																			
		elif self.currentEntity['type'] == 'property':
			x = self.currentEntity['object']
			self._printM(["Parents......[%d]  " % len(x.parents()), "%s" % "; ".join([p.qname for p in x.parents()])])
			self._printM(["\nAncestors....[%d]  " % len(x.ancestors()), "%s" % "; ".join([p.qname for p in x.ancestors()])])
			self._printM(["\nChildren.....[%d]  " % len(x.children()), "%s" % "; ".join([p.qname for p in x.children()])])
			self._printM(["\nDescendants..[%d]  " % len(x.descendants()), "%s" % "; ".join([p.qname for p in x.descendants()])])
			self._printM(["\nHas Domain ..[%d]  " % len(x.domains), "%s" % "; ".join([p.qname for p in x.domains])])
			self._printM(["\nHas Range ...[%d]  " % len(x.ranges), "%s" % "; ".join([p.qname for p in x.ranges])])
			self._print("----------------")

		elif self.currentEntity['type'] == 'concept':
			x = self.currentEntity['object']
			self._printM(["Parents......[%d]  " % len(x.parents()), "%s" % "; ".join([p.qname for p in x.parents()])])
			self._printM(["\nAncestors....[%d]  " % len(x.ancestors()), "%s" % "; ".join([p.qname for p in x.ancestors()])])
			self._printM(["\nChildren.....[%d]  " % len(x.children()), "%s" % "; ".join([p.qname for p in x.children()])])
			self._printM(["\nDescendants..[%d]  " % len(x.descendants()), "%s" % "; ".join([p.qname for p in x.descendants()])])
			self._print("----------------")

		else:
			self._print("Not implemented") 
				
				



	def _selectFromList(self, _list, using_pattern=True):
		"""
		Generic method that lets users pick an item from a list via raw_input
		*using_pattern* flag to know if we're showing all choices or not
		Note: the list items need to be OntoSPy entities.
		"""
		if not _list:
			self._print("No matching items.", "TIP")
			return None
		if using_pattern and len(_list) == 1: # removed
			pass
			# return _list[0]
		if using_pattern:
			self._print("%d matching items: \n--------------" % len(_list), "TIP")
		else:
			self._print("%d items available: \n--------------" % len(_list), "TIP")
		counter = 1
		_temp = []
		for el in _list:
			if hasattr(el, 'uri'):
				_temp += [Fore.BLUE + Style.BRIGHT + "[%d] " % counter + Style.RESET_ALL + str(el.uri)]
			else:
				_temp += [Fore.BLUE + Style.BRIGHT + "[%d] " % counter + Style.RESET_ALL + str(el)]
			counter += 1
		pprint2columns(_temp)
		
		self._print("--------------")
		self._print("Please select one option by entering its number: ")
		var = raw_input()
		try:
			var = int(var)
			return _list[var-1]
		except:
			self._print("Selection not valid")
			return None


	def _next_ontology(self):
		"""Dynamically retrieves the next ontology in the list"""
		currentfile = self.current['file']
		try:
			idx = self.ontologies.index(currentfile)
			return self.ontologies[idx+1]
		except:
			return self.ontologies[0]



	# MAIN METHODS
	# --------


	def _load_ontology(self, filename):
		""" loads an ontology from the local repository 
			note: if the ontology does not have a cached version, it is created
		"""
		fullpath = self.LOCAL_MODELS + filename
		g = ontospy.get_pickled_ontology(filename)
		if not g:
			g = ontospy.do_pickle_ontology(filename)
		self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		self.currentEntity = None
		self._print_entity_intro(g)


	def _select_ontology(self, line):
		"""try to select an ontology NP: the actual load from FS is in <_load_ontology> """
		try:
			var = int(line)	 # it's a string
			if var in range(1, len(self.ontologies)+1):
				self._load_ontology(self.ontologies[var-1])
		except ValueError:
			out = []
			for each in self.ontologies:
				if line in each:
					out += [each]
			choice = self._selectFromList(out, line)
			if choice:
				self._load_ontology(choice)


	def _select_class(self, line):			
		"""try to match a class and load it from the graph"""	
		g = self.current['graph']
		if not line:
			out = g.classes
			using_pattern=False
		else:
			using_pattern=True
			if line.isdigit():
				line =	int(line)
			out = g.getClass(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out, using_pattern)
				if choice:
					self.currentEntity = {'name' : choice.locale or choice.uri, 'object' : choice, 'type' : 'class'}				
			else:
				self.currentEntity = {'name' : out.locale or out.uri, 'object' : out, 'type' : 'class'}				
			# ..finally:
			if self.currentEntity:
				self._print_entity_intro(entity=self.currentEntity)
				
				# self.prompt = self._get_prompt(entity=self.currentEntity['name'])
		else:
			print "not found"


	def _select_property(self, line):			
		"""try to match a property and load it"""
		g = self.current['graph']
		if not line:
			out = g.properties
			using_pattern=False
		else:
			using_pattern=True			
			if line.isdigit():
				line =	int(line)
			out = g.getProperty(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out, using_pattern)
				if choice:
					self.currentEntity = {'name' : choice.locale or choice.uri, 'object' : choice, 'type' : 'property'} 

			else:
				self.currentEntity = {'name' : out.locale or out.uri, 'object' : out, 'type' : 'property'}	
			
			# ..finally:
			if self.currentEntity:
				self._print_entity_intro(entity=self.currentEntity) 
		else:
			print "not found"
			

	def _select_concept(self, line):
		"""try to match a class and load it"""
		g = self.current['graph']
		if not line:
			out = g.skosConcepts
			using_pattern=False
		else:
			using_pattern=True
			if line.isdigit():
				line =	int(line)
			out = g.getSkosConcept(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out, using_pattern)
				if choice:
					self.currentEntity = {'name' : choice.locale or choice.uri, 'object' : choice, 'type' : 'concept'}
			else:
				self.currentEntity = {'name' : out.locale or out.uri, 'object' : out, 'type' : 'concept'}
			# ..finally:
			if self.currentEntity:
				self._print_entity_intro(entity=self.currentEntity)

		else:
			print "not found"




	# COMMANDS
	# --------
	# NOTE: all commands should start with 'do_' and must pass 'line'



	def do_ls(self, line):
		"""Shows entities of a given kind. \nOptions: [ ontologies | classes | properties | concepts ]"""
		line = line.split()
		_pattern = ""
		if len(line) > 1:
			# _pattern = line[1]	
			pass		
		opts = [ 'ontologies', 'classes' , 'properties' , 'concepts' ]

		if (not line) or (line[0] not in opts):
			self._print("Usage: ls [%s]" % "|".join([x for x in opts]))

		elif line[0] == "ontologies":
			if not self.ontologies:
				self._print("No ontologies in the local repository. Run 'ontospy --help' or 'ontospy --import' from the command line. ")
			else:
				self._select_ontology(_pattern)

		elif line[0] in opts and not self.current:
			self._print("Please select an ontology first")

		elif line[0] == "classes":
			g = self.current['graph']
			if g.classes:
				self._select_class(_pattern)
			else:
				self._print("No classes available.")

		elif line[0] == "properties":
			g = self.current['graph']
			if g.properties:
				self._select_property(_pattern)
			else:
				self._print("No properties available.") 

		elif line[0] == "concepts":
			g = self.current['graph']
			if g.skosConcepts:
				self._select_concept(_pattern)
			else:
				self._print("No concepts available.")	

		else: # should never arrive here
			pass


	def do_get(self, line):
		"""Finds entities matching a given string pattern. \nOptions: [ ontologies | classes | properties | concepts ]"""
		line = line.split()
		_pattern = ""
		if len(line) > 1:
			_pattern = line[1]			
		opts = [ 'ontology', 'class' , 'property' , 'concept' ]

		if (not line) or (line[0] not in opts) or (not _pattern):
			self._print("Usage: get [%s] string-pattern" % "|".join([x for x in opts]))

		elif line[0] == "ontology":
			if not self.ontologies:
				self._print("No ontologies in the local repository. Run 'ontospy --help' or 'ontospy --import' from the command line. ")
			else:
				self._select_ontology(_pattern)

		elif line[0] in opts and not self.current:
			self._print("Please select an ontology first")

		elif line[0] == "class":
			g = self.current['graph']
			if g.classes:
				self._select_class(_pattern)
			else:
				self._print("No classes available.")

		elif line[0] == "property":
			g = self.current['graph']
			if g.properties:
				self._select_property(_pattern)
			else:
				self._print("No properties available.") 

		elif line[0] == "concept":
			g = self.current['graph']
			if g.skosConcepts:
				self._select_concept(_pattern)
			else:
				self._print("No concepts available.")	

		else: # should never arrive here
			pass
							
	def do_tree(self, line):
		"""Shows the subsumption tree of an ontology.\nOptions: [classes | properties | concepts] classes"""
		opts = [ 'classes' , 'properties' , 'concepts' ]
		if not self.current:
			self._print("Please select an ontology first")
			return None
		
		line = line.split() 
		g = self.current['graph']

		if (not line) or (line[0] not in opts):
			self._print("Usage: tree [%s]" % "|".join([x for x in opts]))

		elif line[0] == "classes":			
			if g.classes:
				g.printClassTree(showids=False, labels=False, showtype=True)
			else:
				self._print("No classes available.")							
		
		elif line[0] == "properties":
			if g.properties:
				g.printPropertyTree(showids=False, labels=False, showtype=True)
			else:
				self._print("No properties available.")
		
		elif line[0] == "concepts":
			if g.skosConcepts:
				g.printSkosTree(showids=False, labels=False, showtype=True)
			else:
				self._print("No concepts available.")

		else: # never get here
			pass	



	def do_show(self, line):
		"""Shows stuff @todo"""
		opts = [ 'namespaces', 'description', 'overview', 'toplayer', 'parents', 'children', 'stats', 'triples' ]
		
		if not self.current:
			self._print("Please select an ontology first")
			return None
		
		line = line.split() 
		g = self.current['graph']
		
		# get arg, or default to 'overview'
		if not line:
			line = ['overview']	 # default
		elif line and (line[0] not in opts):
			self._print("Usage: show [%s]" % "|".join([x for x in opts]))

		# do commands
		if line[0] == "description":		
			self._printDescription()		

		elif line[0] == "stats":	
			self._printStats()
			
		elif line[0] == "overview": 
			self._printDescription()
			self._printStats(hrlinetop=False)
				
		elif line[0] == "namespaces":			
			for x in g.namespaces:
				self._print("@prefix %s: <%s> ." % (x[0], x[1])) 
								
		elif line[0] == "toplayer":			
			for x in g.toplayer:
				print x.qname
		
		elif line[0] == "parents":
			if self.currentEntity:
				for x in self.currentEntity['object'].parents():
					print x.qname
			else:
				self._print("Please select an entity first.") 

		elif line[0] == "children":			
			if self.currentEntity:
				for x in self.currentEntity['object'].children():
					print x.qname
			else:
				self._print("Please select an entity first.") 

		elif line[0] == "triples":	
			if self.currentEntity:
				self._printTriples(self.currentEntity['object'])
				# self.currentEntity['object'].printTriples()
			else:
				for o in g.ontologies:
					self._printTriples(o)
					# o.printTriples()
																			
		else:
			pass # never get here
				



	def do_serialize(self, line):
		"""Serialize an entity into an RDF flavour"""
		opts = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml']
		
		if not self.current:
			self._print("Please select an ontology first")
			return None
		
		line = line.split() 
		g = self.current['graph']

		if (not line) or (line[0] not in opts):
			self._print("Usage: serialize [%s]" % "|".join([x for x in opts]))
		
		elif self.currentEntity:
			self.currentEntity['object'].printSerialize(line[0])

		else:	
			for o in g.ontologies:
				o.printSerialize(line[0])

	
									
	def do_next(self, line):
		"""Jump to the next entities (ontology, class or property) depending on context"""
		if not self.current:
			print "Please select an ontology first"
		elif self.currentEntity:
			g = self.current['graph']
			if self.currentEntity['type'] == 'class':
				nextentity = g.nextClass(self.currentEntity['object'].uri)
				self._select_class(str(nextentity.uri))
			elif self.currentEntity['type'] == 'property':
				nextentity = g.nextProperty(self.currentEntity['object'].uri)
				self._select_property(str(nextentity.uri))
			elif self.currentEntity['type'] == 'concept':
				nextentity = g.nextConcept(self.currentEntity['object'].uri)
				self._select_concept(str(nextentity.uri))
			else:
				print "Not implemented" 
		else:
			if len(self.ontologies) > 1:
				nextonto = self._next_ontology()
				self._load_ontology(nextonto)
			else:
				self._print("Only one ontology available in repository.")	 


	def do_back(self, line):
		"Go back one step. From entity => ontology; from ontology => ontospy top level."
		if self.currentEntity:
			self.currentEntity = None
			self.prompt = self._get_prompt(self.current['file'])
		else:
			self.current = None
			self.prompt = self._get_prompt()

	def do_quit(self, line):
		"Exit OntoSPy shell"
		self._clear_screen()
		return True


	def do_zen(self, line):
		"""Inspiring quotes for the working ontologist"""
		_quote = random.choice(QUOTES)
		# print _quote['source']
		print Style.DIM + unicode(_quote['text'])
		print Style.BRIGHT + unicode(_quote['source']) + Style.RESET_ALL


	def default(self, line):
		"default message when a command is not recognized"
		foo = ["Don't recognize that command. Try 'help' for some suggestions.", "That looks like the wrong command", "Are you sure you mean that? Try 'help' for some suggestions."]
		print(random.choice(foo))



	# AUTOCOMPLETE METHODS
	# --------

	def complete_ls(self, text, line, begidx, endidx):
		"""completion for ls command"""
		
		options = ['ontologies', 'classes', 'properties', 'concepts']

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	

	def complete_get(self, text, line, begidx, endidx):
		"""completion for find command"""
		
		options = ['ontology', 'class', 'property', 'concept']

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	
				
	def complete_tree(self, text, line, begidx, endidx):
		"""completion for tree command"""
		
		options = ['classes', 'properties', 'concepts']

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	

	def complete_show(self, text, line, begidx, endidx):
		"""completion for show command"""
		
		opts = [ 'namespaces', 'overview', 'description', 'toplayer', 'parents', 'children', 'stats', 'triples']

		if not text:
			completions = opts
		else:
			completions = [ f
							for f in opts
							if f.startswith(text)
							]
		return completions	
		
	def complete_serialize(self, text, line, begidx, endidx):
		"""completion for serialize command"""
		
		opts = [ 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

		if not text:
			completions = opts
		else:
			completions = [ f
							for f in opts
							if f.startswith(text)
							]
		return completions	



	
def main():
	""" standalone line script """
	
	print "OntoSPy " + ontospy.VERSION
	
	Shell()._clear_screen()
	print Style.BRIGHT + "** OntoSPy Interactive Ontology Browser " + ontospy.VERSION + " **" + Style.RESET_ALL
	ontospy.get_or_create_home_repo()
	Shell().cmdloop()
	raise SystemExit, 1
		
		

if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e