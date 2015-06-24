#!/usr/bin/python
# -*- coding: utf-8 -*-

from util import *
import rdflib
from itertools import count
# http://stackoverflow.com/questions/8628123/counting-instances-of-a-class


class RDF_Entity(object):
	"""
	Pythonic representation of an RDF resource - normally not instantiated but used for 
	inheritance purposes 
	"""
	
	_ids = count(0)
			
	def __repr__(self):
		return "<OntoSPy: RDF_Entity object for uri *%s*>" % (self.uri)

	def __init__(self, uri, rdftype=None, namespaces = None):
		"""
		Init ontology object. Load the graph in memory, then setup all necessary attributes.
		"""
		self.id = self._ids.next()
		
		self.uri = uri # rdflib.Uriref
		self.qname = self.__buildQname(namespaces)	
		self.locale	 = inferURILocalSymbol(self.uri)[0]
		self.rdftype = rdftype	
		self.triples = None
		self.rdfgraph = rdflib.Graph()

		self._children = []
		self._parents = []
		# self.siblings = []
		
	def serialize(self, format="turtle"):
		if self.triples:
			if not self.rdfgraph:
				self._buildGraph()
			return self.rdfgraph.serialize(format=format)
		else:
			return None 

	def printSerialize(self, format="turtle"):
		printDebug(self.serialize(format))

	def printTriples(self):
		""" display triples """
		printDebug(bcolors.RED + unicode(self.uri) + bcolors.ENDC) 
		for x in self.triples:
			printDebug(bcolors.PINK + "=> " + unicode(x[1])) 
			printDebug(bcolors.BLUE + ".... " + unicode(x[2]) + bcolors.ENDC) 

	def __buildQname(self, namespaces):
		""" extracts a qualified name for a uri """
		return uri2niceString(self.uri, namespaces)

	def _buildGraph(self):
		""" 
		transforms the triples list into a proper rdflib graph 
		(which can be used later for querying)
		"""
		if self.triples:
			for terzetto in self.triples:
				self.rdfgraph.add(terzetto)

	# methods added to RDF_Entity even though they apply only to some subs
				
	def ancestors(self, cl=None, noduplicates=True):
		""" returns all ancestors in the taxonomy """
		if not cl:
			cl = self
		if cl.parents():
			bag = []
			for x in cl.parents():
				bag += [x] + self.ancestors(x, noduplicates)
			# finally:
			if noduplicates:
				return remove_duplicates(bag) 
			else:
				return bag
		else:
			return []	

		
	def descendants(self, cl=None, noduplicates=True):
		""" returns all descendants in the taxonomy """
		if not cl:
			cl = self
		if cl.children():
			bag = []
			for x in cl.children():
				bag += [x] + self.descendants(x, noduplicates)
			# finally:
			if noduplicates:
				return remove_duplicates(bag) 
			else:
				return bag
		else:
			return []


	def parents(self):
		"""wrapper around property"""
		return self._parents

	def children(self):
		"""wrapper around property"""
		return self._children

	def getValuesForProperty(self, aPropURIRef):
		""" 
		generic way to extract some prop value eg
			In [11]: c.getValuesForProperty(rdflib.RDF.type)
			Out[11]: 
			[rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#Class'),
			 rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#Class')]
		"""
		return list(self.rdfgraph.objects(None, aPropURIRef))
					

	def bestLabel(self, prefLanguage="en", qname_allowed=True):
		"""
		facility for extrating the best available label for an entity

		..This checks RFDS.label, SKOS.prefLabel and finally the qname local component
		"""

		test = self.getValuesForProperty(rdflib.RDFS.label)
		
		if test:
			return firstEnglishStringInList(test)
		else:
			test = self.getValuesForProperty(rdflib.namespace.SKOS.prefLabel)
			if test:
				return firstEnglishStringInList(test)
			else:
				if qname_allowed:
					return self.locale
				else:
					return ""

				


class Ontology(RDF_Entity):
	"""
	Pythonic representation of an OWL ontology
	"""
			
	def __repr__(self):
		return "<OntoSPy: Ontology object for uri *%s*>" % (self.uri)


	def __init__(self, uri, rdftype=None, namespaces=None, prefPrefix=""):
		"""
		Init ontology object. Load the graph in memory, then setup all necessary attributes.
		"""
		super(Ontology, self).__init__(uri, rdftype, namespaces)	
		# self.uri = uri # rdflib.Uriref
		self.annotations = self.triples
		self.prefix = prefPrefix

		self.classes = []			
		self.properties = [] 
		# self.annotationProperties = []
		# self.objectProperties = []
		# self.datatypeProperties = []


	def describe(self):
		""" shotcut to pull out useful info for interactive use """
		# self.printGenericTree()
		printDebug("Classes.....: %d" % len(self.classes))
		printDebug("Properties..: %d" % len(self.properties))
		self.printTriples()





class OntoClass(RDF_Entity):
	"""
	Python representation of a generic class within an ontology. 
	Includes methods for representing and querying RDFS/OWL classes
	"""

	def __init__(self, uri, rdftype=None, namespaces=None):
		"""
		...
		"""
		super(OntoClass, self).__init__(uri, rdftype, namespaces)

		self.domain_of = []
		self.range_of = []
		self.ontology = None
		self.queryHelper = None  # the original graph the class derives from
		
	def __repr__(self):
		return "<Class *%s*>" % ( self.uri)

	
	def instances(self):  # = all instances
		return self.all()
		
	def all(self):
		out = []
		if self.queryHelper:
			qres = self.queryHelper.getClassInstances(self.uri)
			out = list(qres)
		return out
		
	def count(self):
		if self.queryHelper:
			return self.queryHelper.getClassInstancesCount(self.uri)
		else:
			return 0

	def describe(self):
		""" shotcut to pull out useful info for interactive use """
		# self.printGenericTree()
		printDebug("Parents......: %d" % len(self.parents()))
		printDebug("Children.....: %d" % len(self.children()))
		printDebug("Ancestors....: %d" % len(self.ancestors()))
		printDebug("Descendants..: %d" % len(self.descendants()))
		printDebug("Domain of....: %d" % len(self.domain_of))
		printDebug("Range of.....: %d" % len(self.range_of))
		printDebug("Instances....: %d" % self.count())
		self.printTriples()

			
	def printGenericTree(self):
		printGenericTree(self)






class OntoProperty(RDF_Entity):
	"""
	Python representation of a generic RDF/OWL property.
	
	rdftype is one of:
	rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty')
	rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#DatatypeProperty')
	rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#AnnotationProperty')
	rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')
		
	"""

	def __init__(self, uri, rdftype=None, namespaces=None):
		"""
		...
		"""
		super(OntoProperty, self).__init__(uri, rdftype, namespaces)

		self.rdftype = inferMainPropertyType(rdftype)
		
		self.domains = []
		self.ranges = []
		self.ontology = None

	def __repr__(self):
		return "<Property *%s*>" % ( self.uri)

	
	def printPropertyTree(self):
		printGenericTree(self)


	def describe(self):
		""" shotcut to pull out useful info for interactive use """
		# self.printGenericTree()
		printDebug("Parents......: %d" % len(self.parents()))
		printDebug("Children.....: %d" % len(self.children()))
		printDebug("Ancestors....: %d" % len(self.ancestors()))
		printDebug("Descendants..: %d" % len(self.descendants()))
		printDebug("Has Domain...: %d" % len(self.domains))
		printDebug("Has Range....: %d" % len(self.ranges))		
		
		self.printTriples()
			
			
