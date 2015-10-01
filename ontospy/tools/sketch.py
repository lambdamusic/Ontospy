#!/usr/bin/env python

# encoding: utf-8

"""
TURTLE SKETCH
Copyright (c) 2014 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Use the interpreter interactively to create a turtle RDF model.  

++ Tip: make this file executable: chmod +x sketch.py ++ 

"""



import sys, os, urllib2
import logging
import rdflib	 # so we have it available as a namespace
from rdflib import exceptions, URIRef, RDFS, RDF, BNode, OWL
from rdflib.namespace import Namespace, NamespaceManager


from .. import ontospy

# http://stackoverflow.com/questions/17393664/no-handlers-could-be-found-for-logger-rdflib-term
logging.basicConfig()




class Sketch(object):
	"""
	====Sketch v 0.3====
	
	add()  ==> add turtle statements to the graph (http://www.w3.org/TR/turtle/)
	...........SHORTCUTS: 
	...........'class' = owl:Class
	...........'sub' = rdfs:subClassOf
	
	show() ==> shows the graph. Can take an OPTIONAL argument for the format.
	...........eg one of['xml', 'n3', 'turtle', 'nt', 'pretty-xml', dot'] 
	
	clear()	 ==> clears the graph
	...........all triples are removed
	
	omnigraffle() ==> creates a dot file and opens it with omnigraffle
	...........First you must set Omingraffle as your system default app for dot files!
	
	quit() ==> exit 
	
	====Happy modeling====
	"""
	def __init__(self, text=""):
		super(Sketch, self).__init__()
		
		self.rdfGraph = rdflib.Graph()
		self.namespace_manager = NamespaceManager(self.rdfGraph)
		
		self.SUPPORTED_FORMATS = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'dot']
		
		PREFIXES = [
					("", "http://this.sketch#"),
					("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
					("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
					("xml", "http://www.w3.org/XML/1998/namespace"),
					("xsd", "http://www.w3.org/2001/XMLSchema#"),
					('foaf', "http://xmlns.com/foaf/0.1/"),
					("skos", "http://www.w3.org/2004/02/skos/core#"),
					("owl", "http://www.w3.org/2002/07/owl#"),
					]
		for pref in PREFIXES:
			self.bind(pref)
		if text:
			self.add(text)
		
	def add(self, text="", default_continuousAdd=True):
		"""add some turtle text"""
		if not text and default_continuousAdd:
			self.continuousAdd()
		else:
			pprefix = ""
			for x,y in self.rdfGraph.namespaces():
				pprefix += "@prefix %s: <%s> . \n" % (x, y)
			# add final . if missing
			if text and (not text.strip().endswith(".")):
				text += " ."
			# smart replacements
			text = text.replace(" sub ", " rdfs:subClassOf ")
			text = text.replace(" class ", " owl:Class ")
			# finally
			self.rdfGraph.parse(data=pprefix+text, format="turtle")
	
	
	# note: problem here if typying ### on first line! 
	def continuousAdd(self):
		print "Multi-line input. Enter ### when finished."
		temp = ""
		sentinel = "###"
		for line in iter(raw_input, sentinel):
			if line.strip() == sentinel:
				break
			if not line.strip().endswith("."):
				line += " ."	
			temp += "%s" % line
		self.add(temp, False) # default_continuousAdd=False	
	
	def bind(self, prefixTuple):
		p, k = prefixTuple
		self.rdfGraph.bind(p, k)
	
	def clear(self):
		""""
		Clears the graph 
			@todo add ability to remove specific triples
		"""
		self.rdfGraph.remove((None, None, None))


	def serialize(self, aformat="turtle"):
		"""
		Serialize graph using the format required
		"""
		if aformat and aformat not in self.SUPPORTED_FORMATS:
			return "Sorry. Allowed formats are %s" % str(self.SUPPORTED_FORMATS)
		if aformat == "dot":
			return self.__serializedDot()
		else:
			# use stardard rdf serializations
			return self.rdfGraph.serialize(format=aformat)

	def __serializedDot(self):
		"""
		DOT format:
		digraph graphname {
			 a -> b [label=instanceOf];
			 b -> d [label=isA];
		 }	
		"""
		temp = ""
		for x,y,z in self.rdfGraph.triples((None, None, None)):
			temp += """"%s" -> "%s" [label="%s"];\n""" % (self.namespace_manager.normalizeUri(x), self.namespace_manager.normalizeUri(z), self.namespace_manager.normalizeUri(y))
		temp = "digraph graphname {\n%s}" % temp
		return temp


	def omnigraffle(self):
		""" tries to open an export directly in omnigraffle """
		temp = self.serialize("dot")
		
		try:  # try to put in the user/tmp folder 
			from os.path import expanduser
			home = expanduser("~")
			filename = home + "/tmp/turtle_sketch.dot"
			f = open(filename, "w")
		except:
			filename = "turtle_sketch.dot"
			f = open(filename, "w")
		f.write(temp)
		f.close()
		try:
			os.system("open " + filename)
		except:
			os.system("start " + filename)

		
	def show(self, aformat="turtle"):
		print self.serialize(aformat)

	def docs(self):
		print self.__docs__		









##################
# 
#  Standalone Mode:
#
##################




def main(argv=None):
	"""
	September 18, 2014: if an arg is passed, we visualize it
	Otherwise a simple shell gets opened. 

	"""
	
	print "OntoSPy " + ontospy.VERSION

	if argv:
		print "Argument passing not implemented yet"
		if False:
			onto = Model(argv[0])
			for x in onto.getClasses():
				print x
			onto.buildPythonClasses()
			s = Sketch()
	
	else:

		intro = """Good morning. Ready to Turtle away. Type docs() for help.""" 
		# idea: every time provide a different ontology maxim!
		
		def docs():
			print "\n".join([x.strip() for x in Sketch.__doc__.splitlines()])
		
		default_sketch = Sketch()
		
		def add(text=""):
			default_sketch.add(text)
		def show(aformat=None):
			if aformat:
				default_sketch.show(aformat)
			else:
				default_sketch.show()			
		def bind(prefixTuple):
			default_sketch.bind(prefixTuple)
		def clear():
			default_sketch.clear()
		def omnigraffle():
			default_sketch.omnigraffle()
		
		
		try:
			# note: this requires IPython 0.11 or above
			import IPython
			IPython.embed(banner1=intro)
		except:
			import code
			code.interact(banner=intro, local=dict(globals(), **locals()))
	# finally
	sys.exit(0)


if __name__ == '__main__':
	main(sys.argv[1:])
