#!/usr/bin/env python
# encoding: utf-8



"""
ONTOSPY
Copyright (c) 2013-2015 __Michele Pasin__ <michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI. 

>>> python ontospy.py -h

More info in the README file.

"""


import sys, os, urllib2, time, optparse

import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLStore

from util import *
from entities import *
from queryHelper import QueryHelper


class Graph(object):
	"""
	Object that scan an rdf graph for schema definitions (aka 'ontologies') 
	
	In [1]: import ontospy2
	INFO:rdflib:RDFLib Version: 4.2.0

	In [2]: g = ontospy2.Graph("npgcore_latest.ttl")
	Loaded 3478 triples
	Ontologies found: 1
	
	"""

	def __init__(self, source, text=False, endpoint=False, rdf_format=None):
		"""
		Load the graph in memory, then setup all necessary attributes.
		"""
		super(Graph, self).__init__() 

		self.rdfgraph = rdflib.Graph()			
			
		self.graphuri	= None
		self.queryHelper = None # instantiated after we have a graph
		
		self.ontologies = []
		self.classes = []	
		self.namespaces = []
		
		self.properties = [] 
		self.annotationProperties = [] 
		self.objectProperties = []
		self.datatypeProperties = []
		
		self.skosConcepts = []
		
		self.toplayer = []
		self.toplayerProperties = []
		self.toplayerSkosConcepts = []
		
		# keep track of the rdf source		
		self.IS_ENDPOINT = False
		self.IS_FILE = False
		self.IS_URL = False
		self.IS_TEXT = False
		
		# finally		
		self.__loadRDF(source, text, endpoint, rdf_format)
		# extract entities into
		self._scan()

	
	def __repr__(self):
		return "<OntoSPy Graph (%d triples)>" % (len(self.rdfgraph))
				


	
	def __loadRDF(self, source, text, endpoint, rdf_format):
		"""
		Determine what kind of graph we have and load it accordingly
		"""
		
		# LOAD THE GRAPH
				
		if text:
			self.IS_TEXT = True
			rdf_format = rdf_format or "turtle"
		
		
		elif endpoint:
			self.IS_ENDPOINT = True
			# replace graph with ConjunctiveGraph
			self.rdfgraph = rdflib.ConjunctiveGraph(store=SPARQLStore(source))			
			self.graphuri = source	# default uri is www location


		else:

			if type(source) == type("string"):
				if source.startswith("www."): #support for lazy people
					source = "http://%s" % str(source)
				if source.startswith("http://"):
					self.IS_URL = True
					headers = "Accept: application/rdf+xml"
					req = urllib2.Request(source, headers)
					res = urllib2.urlopen(req)
					source = res.geturl()  # after 303 redirects

				self.graphuri = source	# default uri is www location
				rdf_format = rdf_format or guess_fileformat(source)

			elif type(source) == file:
				self.IS_FILE = True				
				self.graphuri = source.name # default uri is filename
				rdf_format = rdf_format or guess_fileformat(source.name)
			
			else:
				raise Exception("You passed an unknown object. Only URIs and files are accepted.") 
			
		#FINALLY, TRY LOADING:		

		try:
			if self.IS_TEXT:			
				self.rdfgraph.parse(data=source, format=rdf_format)
				printDebug("----------\nLoaded %d triples from text" % len(self.rdfgraph))
			elif self.IS_ENDPOINT:
				printDebug("Accessing SPARQL Endpoint <%s>" % self.graphuri)
				printDebug("(note: support for sparql endpoints is still experimental)")
			else:
				self.rdfgraph.parse(source, format=rdf_format)
				printDebug("----------\nLoaded %d triples from <%s>" % (len(self.rdfgraph), self.graphuri))
			# set up the query helper too
			self.queryHelper = QueryHelper(self.rdfgraph)	



		
		except:
			printDebug("\nError Parsing Graph (assuming RDF serialization was *%s*)\n" % (rdf_format))	 
			raise




	def serialize(self, rdf_format="turtle"):
		""" Shortcut that outputs the graph 
		Valid options are: xml, n3, turtle, nt, pretty-xml [trix not working out of the box]
		"""
		return self.rdfgraph.serialize(format=rdf_format)
			
	
	def sparql(self, stringa):
		""" wrapper around a sparql query """
		qres = self.rdfgraph.query(stringa)
		return list(qres)
			

	def __extractNamespaces(self):
		""" 
		Extract graph namespaces.
		Namespaces are given in this format:

			In [01]: for x in graph.namespaces():
					....:			print x
			('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
			('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
			(u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
			('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
			('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
			(u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))

		We assume that a base namespace is implied by an empty prefix		
		"""

		exit = []

		if self.IS_ENDPOINT==True:
			return False

		else:
			
			if self.graphuri not in [y for x,y in self.rdfgraph.namespaces()]:
				# if not base namespace is set, try to simulate one 
				self.rdfgraph.bind("_file_", rdflib.Namespace(self.graphuri))
	
			self.namespaces = sorted(self.rdfgraph.namespaces())
		


	
	# ------------	
	# === main method === #	 
	# ------------
	
	def _scan(self, source=None, text=False, endpoint=False, rdf_format=None):
		""" 
		scan a source of RDF triples 
		build all the objects to deal with the ontology/ies pythonically
				
		In [1]: g.scan("npgcore_latest.ttl")
		Ontologies found: 1
		Out[3]: [<OntoSPy: Ontology object for uri *http://ns.nature.com/terms/*>]
		
		"""
		
		if source: # add triples dynamically
			self.__loadRDF(source, text, endpoint, rdf_format)
		
		printDebug("started scanning...\n----------")
					
		self.__extractNamespaces()
		
		self.__extractOntologies()
		printDebug("Ontologies found...: %d" % len(self.ontologies))
						
		self.__extractClasses()
		printDebug("Classes found......: %d" % len(self.classes))
		
		self.__extractProperties()
		printDebug("Properties found...: %d" % len(self.properties))
		printDebug("Annotation.........: %d" % len(self.annotationProperties))
		printDebug("Datatype...........: %d" % len(self.datatypeProperties))
		printDebug("Object.............: %d" % len(self.objectProperties))

		self.__extractSkosConcepts()
		printDebug("SKOS Concepts......: %d" % len(self.skosConcepts))
				
		self.__computeTopLayer()
		
		printDebug("----------")
			
		

	def printStats(self):
		""" shotcut to pull out useful info for interactive use """
		printDebug("----------------")
		printDebug("Ontologies......: %d" % len(self.ontologies))
		printDebug("Classes.........: %d" % len(self.classes))
		printDebug("Properties......: %d" % len(self.properties))
		printDebug("..annotation....: %d" % len(self.annotationProperties))
		printDebug("..datatype......: %d" % len(self.datatypeProperties))
		printDebug("..object........: %d" % len(self.objectProperties))
		printDebug("Concepts(SKOS)..: %d" % len(self.skosConcepts))
		printDebug("----------------")

	
	def __extractOntologies(self, exclude_BNodes = False, return_string=False):
		"""
		returns Ontology class instances
		
		[ a owl:Ontology ;
			vann:preferredNamespacePrefix "bsym" ;
			vann:preferredNamespaceUri "http://bsym.bloomberg.com/sym/" ],
			
			
				
		"""
		out = []
	
		qres = self.queryHelper.getOntology()

		if qres:
			# NOTE: SPARQL returns a list of rdflib.query.ResultRow (~ tuples..)
			
			for candidate in qres:
				if isBlankNode(candidate[0]):
					if exclude_BNodes:
						continue
					else:
						checkDC_ID = [x for x in self.rdfgraph.objects(candidate[0], rdflib.namespace.DC.identifier)]
						if checkDC_ID:
							out += [Ontology(checkDC_ID[0])]
						else:
							vannprop = rdflib.URIRef("http://purl.org/vocab/vann/preferredNamespaceUri")
							vannpref = rdflib.URIRef("http://purl.org/vocab/vann/preferredNamespacePrefix")
							checkDC_ID = [x for x in self.rdfgraph.objects(candidate[0], vannprop)]
							if checkDC_ID:
								checkDC_prefix = [x for x in self.rdfgraph.objects(candidate[0], vannpref)]
								if checkDC_prefix:
									out += [Ontology(checkDC_ID[0], prefPrefix=checkDC_prefix[0])]
								else:
									out += [Ontology(checkDC_ID[0])]
						
				else:
					out += [Ontology(candidate[0])]
			
			
		else:
			pass
			# printDebug("No owl:Ontologies found")
			
		#finally... add all annotations/triples		
		self.ontologies = out
		for onto in self.ontologies:
			onto.triples = self.queryHelper.entityTriples(onto.uri)
			onto._buildGraph() # force construction of mini graph
		


	##################
	#  
	#  METHODS for MANIPULATING RDFS/OWL CLASSES 
	# 
	#  RDFS:class vs OWL:class cf. http://www.w3.org/TR/owl-ref/ section 3.1
	#
	##################


	def __extractClasses(self):
		""" 
		2015-06-04: removed sparql 1.1 queries
		2015-05-25: optimized via sparql queries in order to remove BNodes
		2015-05-09: new attempt 
		
		Note: queryHelper.getAllClasses() returns a list of tuples, 
		(class, classRDFtype) 
		so in some cases that's duplicates if a class is both RDFS.CLass and OWL.Class
		In this case we keep only OWL.Class as it is more informative.
		"""
		self.classes = [] # @todo: keep adding? 
		
		qres = self.queryHelper.getAllClasses()

		for candidate in qres:
			
			test_existing_cl = self.getClass(uri=candidate[0])
			if not test_existing_cl:
				# create it
				self.classes += [OntoClass(candidate[0], candidate[1], self.namespaces)]
			else:
				# update it
				if candidate[1] == rdflib.OWL.Class:
					# prefer OWL.Class over RDFS.Class
					test_existing_cl.rdftype = rdflib.OWL.Class 
					
				
		
		#add more data
		for aClass in self.classes:
			
			aClass.triples = self.queryHelper.entityTriples(aClass.uri)
			aClass._buildGraph() # force construction of mini graph
			
			aClass.queryHelper = self.queryHelper
			
			# attach to an ontology 
			for uri in aClass.getValuesForProperty(rdflib.RDFS.isDefinedBy):
				onto = self.getOntology(str(uri))
				if onto:
					onto.classes += [aClass]
					aClass.ontology = onto
					
			# add direct Supers				
			directSupers = self.queryHelper.getClassDirectSupers(aClass.uri)
			
			for x in directSupers:
				superclass = self.getClass(uri=x[0])
				if superclass: 
					aClass._parents.append(superclass)
					
					# add inverse relationships (= direct subs for superclass)
					if aClass not in superclass.children():
						 superclass._children.append(aClass)
			



	def __extractProperties(self):
		""" 
		2015-06-04: removed sparql 1.1 queries
		2015-06-03: analogous to get classes	
		
		# instantiate properties making sure duplicates are pruned
		# but the most specific rdftype is kept 
		# eg OWL:ObjectProperty over RDF:property
			
		"""
		self.properties = [] # @todo: keep adding? 
		self.annotationProperties = [] 
		self.objectProperties = []
		self.datatypeProperties = [] 
		
		qres = self.queryHelper.getAllProperties()
				
		for candidate in qres:

			test_existing_prop = self.getProperty(uri=candidate[0])
			if not test_existing_prop:
				# create it
				self.properties += [OntoProperty(candidate[0], candidate[1], self.namespaces)]
			else:
				# update it
				if candidate[1] and (test_existing_prop.rdftype == rdflib.RDF.Property):
					test_existing_prop.rdftype = inferMainPropertyType(candidate[1])


		#add more data
		for aProp in self.properties:
			
			if aProp.rdftype == rdflib.OWL.DatatypeProperty:
				self.datatypeProperties += [aProp]
			elif aProp.rdftype == rdflib.OWL.AnnotationProperty:
				self.annotationProperties += [aProp]
			elif aProp.rdftype == rdflib.OWL.ObjectProperty:
				self.objectProperties += [aProp]
			else:
				pass
			
			aProp.triples = self.queryHelper.entityTriples(aProp.uri)
			aProp._buildGraph() # force construction of mini graph

			# attach to an ontology [2015-06-15: no property type distinction yet]
			for uri in aProp.getValuesForProperty(rdflib.RDFS.isDefinedBy):
				onto = self.getOntology(str(uri))
				if onto:
					onto.properties += [aProp]
					aProp.ontology = onto
					
					
					
			self.__buildDomainRanges(aProp)
			
			# add direct Supers				
			directSupers = self.queryHelper.getPropDirectSupers(aProp.uri)
			
			for x in directSupers:
				superprop = self.getProperty(uri=x[0])
				if superprop: 
					aProp._parents.append(superprop)
				
					# add inverse relationships (= direct subs for superprop)
					if aProp not in superprop.children():
						 superprop._children.append(aProp)
		
	
	
	def __extractSkosConcepts(self):
		""" 
		2015-08-19: first draft
		"""
		self.skosConcepts = [] # @todo: keep adding? 
		
		qres = self.queryHelper.getSKOSInstances()

		for candidate in qres:
			
			test_existing_cl = self.getSkosConcept(uri=candidate[0])
			if not test_existing_cl:
				# create it
				self.skosConcepts += [OntoSkosConcept(candidate[0], None, self.namespaces)]
			else:
				pass
	
		#add more data
		for aConcept in self.skosConcepts:
			
			aConcept.triples = self.queryHelper.entityTriples(aConcept.uri)
			aConcept._buildGraph() # force construction of mini graph
			
			aConcept.queryHelper = self.queryHelper
			
			# attach to an ontology 
			for uri in aConcept.getValuesForProperty(rdflib.RDFS.isDefinedBy):
				onto = self.getOntology(str(uri))
				if onto:
					onto.skosConcepts += [aConcept]
					aConcept.ontology = onto
					
			# add direct Supers				
			directSupers = self.queryHelper.getSKOSDirectSupers(aConcept.uri)
			
			for x in directSupers:
				superclass = self.getSkosConcept(uri=x[0])
				if superclass: 
					aConcept._parents.append(superclass)
					
					# add inverse relationships (= direct subs for superclass)
					if aConcept not in superclass.children():
						 superclass._children.append(aConcept)	
					
					

	def getClass(self, id=None, uri=None, match=None):
		""" 
		get the saved-class with given ID or via other methods...
		
		Note: it tries to guess what is being passed..
	
		In [1]: g.getClass(uri='http://www.w3.org/2000/01/rdf-schema#Resource')
		Out[1]: <Class *http://www.w3.org/2000/01/rdf-schema#Resource*>
		
		In [2]: g.getClass(10)
		Out[2]: <Class *http://purl.org/ontology/bibo/AcademicArticle*> 

		In [3]: g.getClass(match="person")
		Out[3]: 
		[<Class *http://purl.org/ontology/bibo/PersonalCommunicationDocument*>,
		 <Class *http://purl.org/ontology/bibo/PersonalCommunication*>,
		 <Class *http://xmlns.com/foaf/0.1/Person*>]
		
		"""
		
		if not id and not uri and not match:
			return None
			
		if type(id) == type("string"):
			uri = id
			id = None
			if not uri.startswith("http://"):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match: # qname 
				for x in self.classes:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.classes:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.classes:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None


	def getProperty(self, id=None, uri=None, match=None):
		""" 
		get the saved-class with given ID or via other methods...
		
		Note: analogous to getClass method		
		"""
		
		if not id and not uri and not match:
			return None
			
		if type(id) == type("string"):
			uri = id
			id = None
			if not uri.startswith("http://"):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match: # qname 
				for x in self.properties:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.properties:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.properties:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None


	def getSkosConcept(self, id=None, uri=None, match=None):
		""" 
		get the saved skos concept with given ID or via other methods...
		
		Note: it tries to guess what is being passed as above		
		"""
		
		if not id and not uri and not match:
			return None
			
		if type(id) == type("string"):
			uri = id
			id = None
			if not uri.startswith("http://"):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match: # qname 
				for x in self.skosConcepts:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.skosConcepts:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.skosConcepts:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None


	def getEntity(self, id=None, uri=None, match=None):
		""" 
		get a generic entity with given ID or via other methods...
		"""
		
		if not id and not uri and not match:
			return None
			
		if type(id) == type("string"):
			uri = id
			id = None
			if not uri.startswith("http://"):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []			
			if ":" in match: # qname 
				for x in self.classes:
					if match.lower() in x.qname.lower():
						res += [x]
				for x in self.properties:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.classes:
					if match.lower() in x.uri.lower():
						res += [x]
				for x in self.properties:
					if match.lower() in x.uri.lower():
						res += [x]	
			return res
		else:
			for x in self.classes:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			for x in self.properties:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None
			
						

	def getOntology(self, id=None, uri=None, match=None):
		""" 
		get the saved-ontology with given ID or via other methods...	
		"""
		
		if not id and not uri and not match:
			return None
			
		if type(id) == type("string"):
			uri = id
			id = None
			if not uri.startswith("http://"):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			for x in self.ontologies:
				if match.lower() in x.uri.lower():
					res += [x]
			return res
		else:
			for x in self.ontologies:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None
			
	
	def nextClass(self, classuri):
		"""Returns the next class in the list of classes. If it's the last one, returns the first one."""
		if classuri == self.classes[-1].uri:
			return self.classes[0]
		flag = False
		for x in self.classes:
			if flag == True:
				return x
			if x.uri == classuri:
				flag = True
		return None


	def nextProperty(self, propuri):
		"""Returns the next property in the list of properties. If it's the last one, returns the first one."""
		if propuri == self.properties[-1].uri:
			return self.properties[0]
		flag = False
		for x in self.properties:
			if flag == True:
				return x
			if x.uri == propuri:
				flag = True
		return None
	
	def nextConcept(self, concepturi):
		"""Returns the next skos concept in the list of concepts. If it's the last one, returns the first one."""
		if concepturi == self.skosConcepts[-1].uri:
			return self.skosConcepts[0]
		flag = False
		for x in self.skosConcepts:
			if flag == True:
				return x
			if x.uri == concepturi:
				flag = True
		return None
			

	def __computeTopLayer(self):

		exit = []
		for c in self.classes:
			if not c.parents():
				exit += [c]
		self.toplayer = exit # sorted(exit, key=lambda x: x.id) # doesnt work

		# properties 
		exit = []
		for c in self.properties:
			if not c.parents():
				exit += [c]
		self.toplayerProperties = exit # sorted(exit, key=lambda x: x.id) # doesnt work

		# skos 
		exit = []
		for c in self.skosConcepts:
			if not c.parents():
				exit += [c]
		self.toplayerSkosConcepts = exit # sorted(exit, key=lambda x: x.id) # doesnt work
				

	def printClassTree(self, element = None, showids=True, labels=False):
		""" 
		Print nicely into stdout the class tree of an ontology 
		
		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		
		if not element:	 # first time
			for x in self.toplayer:
				printGenericTree(x, 0, showids, labels)
		
		else:
			printGenericTree(element, 0, showids, labels)		


	def printPropertyTree(self, element = None, showids=True, labels=False):
		""" 
		Print nicely into stdout the property tree of an ontology 
		
		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		
		if not element:	 # first time
			for x in self.toplayerProperties:
				printGenericTree(x, 0, showids, labels)
		
		else:
			printGenericTree(element, 0, showids, labels)
			

	def printSkosTree(self, element = None, showids=True, labels=False):
		""" 
		Print nicely into stdout the SKOS tree of an ontology 
		
		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		
		if not element:	 # first time
			for x in self.toplayerSkosConcepts:
				printGenericTree(x, 0, showids, labels)
		
		else:
			printGenericTree(element, 0, showids, labels)
						


	###########

	# METHODS for MANIPULATING RDFS/OWL PROPERTIES

	###########



	def __buildDomainRanges(self, aProp):			
		"""
		extract domain/range details and add to Python objects
		"""
		domains = aProp.rdfgraph.objects(None, rdflib.RDFS.domain)
		ranges =  aProp.rdfgraph.objects(None, rdflib.RDFS.range)
		
		for x in domains:
			if not isBlankNode(x):
				aClass = self.getClass(uri=str(x))
				if aClass:
					aProp.domains += [aClass]
					aClass.domain_of += [aProp]
				else:
					aProp.domains += [x]  # edge case: it's not an OntoClass instance?
				
		for x in ranges:
			if not isBlankNode(x):
				aClass = self.getClass(uri=str(x))
				if aClass:
					aProp.ranges += [aClass]
					aClass.range_of += [aProp]
				else:
					aProp.ranges += [x] 






class SparqlEndpoint(Graph):
	"""
	A remote graph accessible via a sparql endpoint
	"""
	
	def __init__(self, source):
		"""
		Init ontology object. Load the graph in memory, then setup all necessary attributes.
		"""
		super(SparqlEndpoint, self).__init__(source, text=False, endpoint=True, rdf_format=None)	



	

