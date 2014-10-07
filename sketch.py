#!/usr/bin/env python

# encoding: utf-8

"""
ONTOSPY2
Copyright (c) 2014 __Michele Pasin__ <michelepasin.org>. All rights reserved.


September 11, 2014: started rethinking the library using sparql and retriving OWL classes to start with


"""



import sys, os, urllib2
import logging

import rdflib	 # so we have it available as a namespace
from rdflib import exceptions, URIRef, RDFS, RDF, BNode, OWL
from rdflib.namespace import Namespace, NamespaceManager
from rdflib.plugins import sparql

# http://stackoverflow.com/questions/17393664/no-handlers-could-be-found-for-logger-rdflib-term
logging.basicConfig()




class Sketch(object):
	"""
	====Sketch v 0.1====
	
	Sketch() ==> creates a new sketch 
	show() ==> shows the graph in indented mode (turtle)
	clear()	 ==> clears the graph
	add()  ==> add a turtle string to the graph
	export()  ==> serialize into a graph format (dot only currenlty)
	omnigraffle() ==> creates a dot file and tries to open it with your system default app
	serialize()	 ==> serializes into rdf (arg=format)
	quit() ==> exit 
	
	Turtle syntax ==> http://www.w3.org/TR/turtle/
	
	====Have fun!====
	"""
	def __init__(self, text=""):
		super(Sketch, self).__init__()
		
		self.rdfGraph = rdflib.Graph()
		self.namespace_manager = NamespaceManager(self.rdfGraph)
		
		PREFIXES = [
					("", "http://this.sketch.com#"),
					("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
					("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
					("xml", "http://www.w3.org/XML/1998/namespace"),
					("xsd", "http://www.w3.org/2001/XMLSchema#"),
					('foaf', "http://xmlns.com/foaf/0.1/"),
					("npg", "http://ns.nature.com/terms/"),
					("npgg", "http://ns.nature.com/graphs/"),
					("npgx", "http://ns.nature.com/extensions/"),
					("bibo", "http://purl.org/ontology/bibo/"),
					("skos", "http://www.w3.org/2004/02/skos/core#"),
					("owl", "http://www.w3.org/2002/07/owl#"),
					]
		for pref in PREFIXES:
			self.bind(pref)
		if text:
			self.add(text)
		
	def add(self, text=""):
		"""add some turtle text"""
		if not text:
			self.continuousAdd()
		else:
			pprefix = ""
			for x,y in self.rdfGraph.namespaces():
				pprefix += "@prefix %s: <%s> . \n" % (x, y)
			if not text.strip().endswith("."):
				text += " ."
			self.rdfGraph.parse(data=pprefix+text, format="turtle")
	
	
	def continuousAdd(self):
		print "Multi-line input. Enter ### when finished."
		temp = ""
		sentinel = "###"
		for line in iter(raw_input, sentinel):
			if line.strip() == sentinel:
				break
			if not line.strip().endswith("."):
				line += " ."	
			temp += "%s\n" % line
		self.add(temp)	
	
	def bind(self, prefixTuple):
		p, k = prefixTuple
		self.rdfGraph.bind(p, k)
	
	def clear(self, triple=None):
		if not triple:
			self.rdfGraph.remove((None, None, None))
		else:
			self.rdfGraph.remove(triple)

	def export(self, format="dot"):
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
		temp = self.export("dot")
		filename = "omnigraffle_sketch.dot"
		f = open(filename, "w")
		f.write(temp)
		f.close()
		try:
			os.system("open " + filename)
		except:
			os.system("start " + filename)


	def serialize(self, format="turtle"):
		return self.rdfGraph.serialize(format=format)

	def show(self):
		print self.serialize()

	def docs(self):
		print self.__docs__		









##################
# 
#  Standalone Mode:
#
##################




def main(argv):
	"""
	September 18, 2014: if an arg is passed, we visualize it
	Otherwise a simple shell gets opened. 

	"""
	
	if argv:
		onto = Model(argv[0])
		for x in onto.getClasses():
			print x
		onto.buildPythonClasses()
		s = Sketch()
	
	else:

		# intro1 = """Commands: Sketch() to create a new sketch / quit() to exit."""
		intro = """Good morning. Ready to Turtle away. Type docs() for help.""" # idea: every time provide a different ontology maxim
		
		def docs():
			print "\n".join([x.strip() for x in Sketch.__doc__.splitlines()])
		
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
