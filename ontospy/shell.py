
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
	
	def __init__(self):
		 """
		 """
		 # useful vars
		 self.LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
		 self.ontologies = self._get_files()
		 self.current = None
		 cmd.Cmd.__init__(self)

	def _get_prompt(self, stringa=""):
		if stringa:
			temp = '<%s>: ' % stringa
			return bcolors.PINK + temp + bcolors.ENDC
		else:
			return bcolors.BLUE + '<OntoSPy>: ' + bcolors.ENDC

	def _get_files(self):
		if os.path.exists(self.LOCAL):
			onlyfiles = [ f for f in os.listdir(self.LOCAL) if os.path.isfile(os.path.join(self.LOCAL,f)) ]
			return [f for f in onlyfiles if not f.startswith(".")]
		else:
			print "No local repository found. Run 'ontospy --setup' first."
			return []

	def _load_ontology(self, filename):
		file = self.LOCAL + "/" + filename
		self.current = file
		g = ontospy.Graph(file)
		print "Loaded ", file
		self.prompt = self._get_prompt(filename)

	# COMMANDS
	# --------
	# NOTE: all commands should start with 'do_' and must pass 'line'
	# eg
	#
	# def do_prompt(self, line):
	#	"Change the interactive prompt"
	#	self.prompt = line + ': '
	
	

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
		
				

	def do_top(self, line):
		"Unload any ontology and go back to top level"
		self.current = None
		self.prompt = self._get_prompt(qu)
						
	def do_quit(self, line):
		"Exit OntoSPy shell"
		return True
		
	def default(self, line):
		"default message when a command is not recognized"
		foo = ["Wow first time I hear that", "That looks like the wrong command", "Are you sure you mean that? try 'help' for some suggestions"]
		print(random.choice(foo))



if __name__ == '__main__':
	Shell().cmdloop()