
# docs:
# https://docs.python.org/2/library/cmd.html
# http://pymotw.com/2/cmd/

import os, cmd, random
import ontospy
from libs.util import *


class Shell(cmd.Cmd):
	"""Simple command processor example."""

	prompt = bcolors.BLUE + '<OntoSPy>: ' + bcolors.ENDC
	intro = "Ontology is a work of love."

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
			temp = '<%s>: ' % stringa
			return bcolors.BLUE + temp + bcolors.ENDC
		else:
			return bcolors.BLUE + '<OntoSPy>: ' + bcolors.ENDC

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




	# COMMANDS
	# --------
	# NOTE: all commands should start with 'do_' and must pass 'line'
	

	def do_ontologies(self, line):
		if not line:
			# list out all ontologies
			counter = 0
			for file in self.ontologies:
				counter += 1
				print bcolors.PINK, "[%d]" % counter,  bcolors.ENDC, file	
		else:
			# try to match an ontology and load it
			try:
				var = int(line)	 # it's a string
				if var in range(1, len(self.ontologies)+1):
					self._load_ontology(self.ontologies[var-1])
			except:
				if line in self.ontologies:
					self._load_ontology(line)
				else:
					print "not found"

	def complete_ontologies(self, text, line, begidx, endidx):
		if not text:
			completions = self.ontologies[:]
		else:
			completions = [ f
							for f in self.ontologies
							if f.startswith(text)
							]
		return completions
		

	def do_classes(self, line):
		"Show classes for current ontology"
		if not self.current:
			print "No ontology loaded"
		else:
			g = self.current['graph']
			g.printClassTree(showids=True, labels=False)


	def do_properties(self, line):
		"Show properties for current ontology"
		if not self.current:
			print "No ontology loaded"
		else:
			g = self.current['graph']
			g.printPropertyTree(showids=True, labels=False)
				
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