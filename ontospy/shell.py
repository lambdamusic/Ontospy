
# docs:
# https://docs.python.org/2/library/cmd.html
# http://pymotw.com/2/cmd/

import os, cmd, random, urllib2, shutil
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
			
				filename = final_location.split("/")[-1] or final_location.split("/")[-2]
				fullpath = self.LOCAL + "/" + filename
	
				file_ = open(fullpath, 'w')
				file_.write(res.read())
				file_.close()
			else:
				filename = location.split("/")[-1] or location.split("/")[-2]
				fullpath = self.LOCAL + "/" + filename
				shutil.copy(location, fullpath)
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


	def do_ontologies(self, line):
		""" List the available ontologies in the local repository. """ 
		counter = 0
		for file in self.ontologies:
			counter += 1
			print bcolors.PINK, "[%d]" % counter,  bcolors.ENDC, file		

	def do_current(self, line):
		""" List the ontology currently loaded""" 
		 # {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		if self.current:
			print self.current['file']
		else:
			print "No ontology loaded. Use the 'load' command"

	def do_load(self, line):
		""" Load one of the ontologies in the local repository. """ 
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
					success = False
					for each in self.ontologies:
						if line in each:
							print "==> match: %s" % each
							self._load_ontology(each)
							success = True
							break
					if not success:		
						print "not found"

	def complete_load(self, text, line, begidx, endidx):
		if not text:
			completions = self.ontologies[:]
		else:
			completions = [ f
							for f in self.ontologies
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
				os.remove(fullpath)
				if os.path.exists(fullpath + ".pickle"):
					os.remove(fullpath + ".pickle")
				self.ontologies = ontospy.get_localontologies()
				print "Deleted %s" % fullpath


	def do_import(self, line):
		""" Import an ontology from the web (or local file) into the local repository. """ 
		if not line:
			print "Please specify a URI or local path to import from"	
		else:
			self._import_ontology(line)
					

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