#!/usr/bin/env python

# encoding: utf-8

"""
OntosPy
Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.
More info in the __init__.py file.


Run it from the command line and it shows info about the default ontology; alternatively pass it a URI as an argument for where to look for an ontology. Eg: 

>>> python OntosPy.py
>>> python OntosPy.py http://xmlns.com/foaf/0.1/
>>> python OntosPy.py http://purl.org/ontology/mo/

"""



# todo

# 1. change names of methods.. use camelcase and more intuitive division

# 2. # how to avoid "RuntimeError: maximum recursion depth exceeded while calling a Python object"  - for big ontologies ? 

# 3. load an ontology from a sparql endpoint, by querying for all classes



import sys, os, urllib2

import rdflib	 # so we have it available as a namespace

from rdflib import ConjunctiveGraph, Namespace, exceptions
from rdflib import URIRef, RDFS, RDF, BNode
from vocabs import OWL

from vocabs import DUBLINCORE as DC
from utils import *

from entities import *







##################
#
#  constants
#
##################

STANDARD_ANNOTATION_URIS = [ RDFS.comment, OWL.incompatibleWith, RDFS.isDefinedBy, RDFS.label, OWL.priorVersion, RDFS.seeAlso, OWL.versionInfo]

DC_ANNOTATION_URIS = [DC.contributor, DC.coverage, DC.creator, DC.date, DC.description, DC.format,
 DC.identifier, DC.language, DC.publisher, DC.relation, DC.rights, DC.source, DC.subject, DC.title, DC.type]


DEFAULT_SESSION_NAMESPACE = "http://www.OntosPy.org/session/resource#"





##################
#
# The main class
#
##################



class OntosPy(object):
	"""Class that includes methods for querying an RDFS/OWL ontology"""


	def __init__(self, uri=False):
		"""
		Sets up variables

		uri: ...
		language: owl:subclass or rdf:type ... Removed on 26/11 Todo: useful? 
		"""

		super(OntosPy, self).__init__()

		self.rdfGraph = ConjunctiveGraph()
		self.baseURI = None
		self.allclasses = None
		self.allobjproperties = None
		self.alldataproperties = None
		self.toplayer = None
		self.tree = None
		self.maxdepth = None
		self.sessionGraph = None
		self.sessionNS = None	
		self.testallclasses = None

		if uri:
			self.loadUri(uri)
		else:
			printDebug("OntosPy instance created. Use the <loadUri> method to load an ontology.")


	def loadUri(self, uri):
		"""
		Loads a graph from a URI

		At the moment we're only taking two input formats, Rdf/Xml and N3 - easily extended. 
			https://rdflib.readthedocs.org/en/latest/plugin_parsers.html	

		"""

		if uri.startswith("www."):
			uri = "http://%s" % str(uri)  #support for lazy people

		try:
			self.rdfGraph.parse(uri)  # defaults to rdf/xml
		except:
			try:
				self.rdfGraph.parse(uri, format="n3")
			except:
				print ("\n*OntosPy* Error Parsing File (follows rdflib Exception):\n")
				raise
		finally:
			self.baseURI = self.get_OntologyURI() or uri
			# let's cache some useful info for faster access
			self.allclasses = self.__getAllClasses()
			self.allobjproperties = self._getAllProperties(classPredicate = 'owl.objectproperty')
			self.alldataproperties = self._getAllProperties(classPredicate = 'owl.datatypeproperty')
			self.toplayer = self.__getTopclasses()
			self.tree = self.__getTree()
			self.maxdepth = self.__get_MAXTreeLevel()
			self.sessionGraph = ConjunctiveGraph()
			self.sessionNS = Namespace(DEFAULT_SESSION_NAMESPACE)
			
			# self.testallclasses = []
			
			# # TEST 2011-11-11 REMOVE IF IT CAUSES PROBLEMS
			# def myrepr(self):
			# 	return "Class %s%s" % (self.name, self.namespace)
			
			# for x in self.allclasses:
			# 	self.testallclasses.append(type(self.get_name_and_namespace(x)[0], (OntoClass,), 
			# 		{'namespace' : self.get_name_and_namespace(x)[1], 
			# 		'name' : self.get_name_and_namespace(x)[0],
			# 		'__repr__' : myrepr}))
			# 	# temp = OntoClass(name=self.get_name_and_namespace(x)[0],
			# 	#  	namespace=self.get_name_and_namespace(x)[1])
			# 	# self.testallclasses.append(temp)

			printDebug("...OntosPy instance succesfully created for <%s>" % str(self.baseURI))


	def __repr__(self):
		return "<OntosPy object [%d] for URI: %s>" % (id(self), self.baseURI)



	def get_OntologyURI(self, return_as_string=True):
		"""
		In [15]: [x for x in o.rdfGraph.triples((None, RDF.type, OWL.Ontology))]
		Out[15]:
		[(rdflib.URIRef('http://purl.com/net/sails'),
						rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
						rdflib.URIRef('http://www.w3.org/2002/07/owl#Ontology'))]

		Mind that this will work only for OWL ontologies.
		In other cases we just return None, and use the URI passed at loading time

		"""
		test = [x for x, y, z in self.rdfGraph.triples((None, RDF.type, OWL.Ontology))]
		if test:
			if return_as_string:
				return str(test[0])
			else:
				return test[0]
		else:
			return None

	def get_OntoAnnotations(self, return_as_string=True):
		"""
		Tries to get all the available annotations for an OWL ontology.
		Returns a list of annotations as triples, which can easily be transformed into strings
		for pretty display.

		In [4]: o.get_OntoAnnotations()
		Out[4]:
		[('http://www.w3.org/2000/01/rdf-schema#label',
						rdflib.Literal('Sails: ontology the models the WW1 naval history domain', language=None, datatype=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral'))),
				('http://www.w3.org/2002/07/owl#versionInfo',
						rdflib.Literal('0.4: refactored classes and added the inheritance info from CIDOC-CRM', language=None, datatype=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral')))]

		In [5]: [(str(x), str(y)) for x,y in o.get_OntoAnnotations()]
		Out[5]:
		[('http://www.w3.org/2000/01/rdf-schema#label',
						'Sails: ontology the models the WW1 naval history domain'),
				('http://www.w3.org/2002/07/owl#versionInfo',
						'0.4: refactored classes and added the inheritance info from CIDOC-CRM')]

		"""
		exit = []
		ontoURI = self.get_OntologyURI(return_as_string=False)
		if ontoURI:
			for annotationURI in STANDARD_ANNOTATION_URIS:
				test = [z for x, y, z in self.rdfGraph.triples((ontoURI, annotationURI, None))]
				if test:
					exit.append((str(annotationURI), z))
			for annotationURI in DC_ANNOTATION_URIS:
				test = [z for x, y, z in self.rdfGraph.triples((ontoURI, annotationURI, None))]
				if test:
					exit.append((str(annotationURI), z))
		if return_as_string:
			return [(self.uri2niceString(x), str(y)) for x,y in exit]
		else:
			return exit



	# NOTE: owl:Class is defined as a subclass of rdfs:Class. The rationale for having a separate OWL class construct lies in
	# the restrictions on OWL DL (and thus also on OWL Lite), which imply that not all RDFS classes are legal OWL DL classes.
	# In OWL Full these restrictions do not exist and therefore owl:Class and rdfs:Class are equivalent in OWL Full.
	# http://www.w3.org/TR/owl-ref/			, section 3.1


	def __getAllClasses(self, classPredicate = "", includeDomainRange=True, includeImplicit=True, removeBlankNodes = True):
		"""
		Extracts all the classes from a model

		We use the RDFS and OWL predicate by default; also, we extract non explicitly declared classes

		classPredicate: rdfs or owl
		removeBlankNodes: self-explanatory

		"""
		rdfGraph = self.rdfGraph
		exit = {}

		def addIfYouCan(x, mydict):
			if x not in mydict:
				mydict[x] = None
			return mydict

		if classPredicate == "rdfs":
			for s in rdfGraph.subjects(RDF.type , RDFS.Class):
				exit = addIfYouCan(s, exit)
		elif classPredicate == "owl":
			for s in rdfGraph.subjects(RDF.type , OWL.Class):
				exit = addIfYouCan(s, exit)
		else:
			for s in rdfGraph.subjects(RDF.type , RDFS.Class):
				exit = addIfYouCan(s, exit)
			for s in rdfGraph.subjects(RDF.type , OWL.Class):
				exit = addIfYouCan(s, exit)

		if includeDomainRange:  # todo: should I exclude XML literals? 
			for o in rdfGraph.objects(None, RDFS.domain):
				exit = addIfYouCan(o, exit)
			for o in rdfGraph.objects(None, RDFS.range):
				exit = addIfYouCan(o, exit)

		if includeImplicit:
			for s, v, o in rdfGraph.triples((None, RDFS.subClassOf , None)):
				exit = addIfYouCan(s, exit)
				exit = addIfYouCan(o, exit)
			for o in rdfGraph.objects(None, RDF.type):
				exit = addIfYouCan(o, exit)


		# exit = remove_duplicates(exit)

		# get a list
		
		exit = exit.keys()  
		if removeBlankNodes:
			exit = [x for x in exit if not isBlankNode(x)]
		return sort_uri_list_by_name(exit)


	def __getTopclasses(self, classPredicate = ''):
		""" Finds the topclass in an ontology (works also when we have more than on superclass)

		"""
		returnlist = []
		# gets all the classes:
		# 27/7: changed from:  for eachclass in self.__getAllClasses(classPredicate):
		for eachclass in self.allclasses:
			x = self.get_classDirectSupers(eachclass)
			if not x:
				returnlist.append(eachclass)
		return sort_uri_list_by_name(returnlist)


	def __getTree(self, father=None, out=None):
		""" Reconstructs the taxonomical tree of an ontology, from the 'topClasses' (= classes with no supers, see below)
				Returns a dictionary in which each class is a key, and its direct subs are the values.
				The top classes have key = 0

				Eg.
				{'0' : [class1, class2], class1: [class1-2, class1-3], class2: [class2-1, class2-2]}
		"""
		if not father:
			out = {}
			topclasses = self.toplayer
			out[0] = topclasses
			for top in topclasses:
				children = self.get_classDirectSubs(top)
				out[top] = children
				for potentialfather in children:
					self.__getTree(potentialfather, out)
			return out
		else:
			children = self.get_classDirectSubs(father)
			out[father] = children
			for ch in children:
				self.__getTree(ch, out)



	def get_allClassesFromTree(self, element = 0, out = None):
		""" methods that returns all the classes found, from the Tree representation.
			Useful for returning class list according to the tree, as it maintains the ordering of the tree.
			(needs "__getTree" to be run first)
				"""
		if not out:
			out = []
		# out += [x for x in self.tree[element] if x not in out]
		for each in self.tree[element]:
			if each not in out:
				out += [each]
			out += self.get_allClassesFromTree(each, out)
		return remove_duplicates(out)




	def get_classTreeLevel(self, aClass, level = 0, key = 0):
		""" basic function that returns the level of a class int he tree, by inspecting the tree dictionary.
				In some cases a class may have different levels, here we just return the first two..... for now.
				level = position_int, key=classkey_in_treedict
				"""
		for element in self.tree[key]:
			if element == aClass:
				return level
			test = self.get_classTreeLevel(aClass, level + 1, element)
			if test:
				return test
		# return 99 # fallback case..


	def __get_MAXTreeLevel(self):
		""" gets the max depth level of the ontology tree
				"""
		n = 0
		for aClass in self.allclasses:
			temp = self.get_classTreeLevel(aClass)
			if temp > n:
				n = temp
		return n




	def get_class_byname(self, name, exact = False):
		"""
		eg: ship = o.get_class_byname("http://purl.com/net/conflict#Ship", True)
		Gets that class in particular
		o.get_class_byname("http://purl.com/net/conflict#Ship")
		GETS a list of classes beginning like that..
		"""
		temp = []
		if name:
			for x in self.allclasses:
				if exact:
					if x.__str__().lower() == str(name).lower():
						return x
				else:
					if x.__str__().lower().find(str(name).lower()) >= 0:
						temp.append(x)
		return temp



# methods for getting ancestors and descendants of classes: by default, we do not include blank nodes

	def get_classDirectSupers(self, aClass, excludeBnodes = True):
		returnlist = []
		for s, v, o in self.rdfGraph.triples((aClass, RDFS.subClassOf , None)):
			if excludeBnodes:
				if not isBlankNode(o):
					returnlist.append(o)
			else:
				returnlist.append(o)
		return sort_uri_list_by_name(remove_duplicates(returnlist))


	def get_classAllSupers(self, aClass, returnlist = None, excludeBnodes = True ):
		if returnlist == None:  # trick to avoid mutable objs python prob...
			returnlist = []
		for ssuper in self.get_classDirectSupers(aClass, excludeBnodes):
			returnlist.append(ssuper)
			self.get_classAllSupers(ssuper, returnlist, excludeBnodes)
		return sort_uri_list_by_name(remove_duplicates(returnlist))


	def get_classDirectSubs(self, aClass, excludeBnodes = True):
		returnlist = []
		for s, v, o in self.rdfGraph.triples((None, RDFS.subClassOf , aClass)):
			if excludeBnodes:
				if not isBlankNode(s):
					returnlist.append(s)
			else:
				returnlist.append(s)
		return sort_uri_list_by_name(remove_duplicates(returnlist))


	def get_classAllSubs(self, aClass, returnlist = None, excludeBnodes = True):
		if returnlist == None:
			returnlist = []
		for sub in self.get_classDirectSubs(aClass, excludeBnodes):
			returnlist.append(sub)
			self.get_classAllSubs(sub, returnlist, excludeBnodes)
		return sort_uri_list_by_name(remove_duplicates(returnlist))


	def get_classSiblings(self, aClass, excludeBnodes = True):
		returnlist = []
		for father in self.get_classDirectSupers(aClass, excludeBnodes):
			for child in self.get_classDirectSubs(father, excludeBnodes):
				if child != aClass:
					returnlist.append(child)
		return sort_uri_list_by_name(remove_duplicates(returnlist))



	def mostSpecialized(self, classlist):
		"""
		From a list of classes, returns a list of the leafs only. 
		If the classes belong to different branches, or they are at the same depth level (= siblings), all of them are returned.
		"""
		returnlist = []
		superslistlists = [self.get_classAllSupers(aClass) for aClass in classlist if aClass in self.allclasses]
		for aClass in classlist:
			flag = False
			for superslist in superslistlists:
				if aClass in superslist:
					flag = True
			if flag == False:
				returnlist.append(aClass)
		return returnlist


	def mostGeneric(self, classlist):
		"""
		From a list of classes, returns a list of the most generic ones only. 
		If the classes belong to different branches, or both are at the same level, all are returned
		"""
		returnlist = []
		superslist = [self.get_classAllSubs(aClass) for aClass in classlist if aClass in self.allclasses]
		for aClass in classlist:
			flag = False
			for supers in superslist:
				if aClass in supers:
					flag = True
			if flag == False:
				returnlist.append(aClass)
		return returnlist
				

	def get_EntityLabel(self, anEntity, language = "default"):
		"""		Returns the rdfs.label (english) value of an entity (class or property), if existing:
		# temp = [x for x in g.triples((top,RDFS.label, None))]

		(rdflib.URIRef('file:///Users/mac/Documents/Ontologies/CIDOC-CMR/cidoc_crm_v5.0.2.rdfs#E1'),
				rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
				rdflib.Literal('\u039f\u03bd\u03c4\u03cc\u03c4\u03b7\u03c4\u03b1 CIDOC CRM', language=u'el', datatype=None))


		"""
		if language == 'default':
			lang = 'en'
		else:
			lang = language
		for s, p, o in self.rdfGraph.triples((anEntity, RDFS.label , None)):
			try:
				if o.language == lang:
					return o # we're returning the RDF.Literal
			except:
				continue
		# if no language specified, just returns the first label found....
		if language == 'default':
			for s, p, o in self.rdfGraph.triples((anEntity, RDFS.label , None)):
				return o
		return None
		

	# DEPRECATED : we should be using get_EntityLabel which is more generic
	def get_classLabel(self, aClass, language = "default"):
		"""		Returns the rdfs.label (english) value of a class, if existing:
		# temp = [x for x in g.triples((top,RDFS.label, None))]

		(rdflib.URIRef('file:///Users/mac/Documents/Ontologies/CIDOC-CMR/cidoc_crm_v5.0.2.rdfs#E1'),
				rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label'),
				rdflib.Literal('\u039f\u03bd\u03c4\u03cc\u03c4\u03b7\u03c4\u03b1 CIDOC CRM', language=u'el', datatype=None))


		"""
		if language == 'default':
			lang = 'en'
		else:
			lang = language
		for s, p, o in self.rdfGraph.triples((aClass, RDFS.label , None)):
			try:
				if o.language == lang:
					return o # we're returning the RDF.Literal
			except:
				continue
		# if no language specified, just returns the first label found....
		if language == 'default':
			for s, p, o in self.rdfGraph.triples((aClass, RDFS.label , None)):
				return o
		return None



	def get_classComment(self, aClass, language = "default"):
		"""		Returns the rdf.comment value of a class, if existing:

		[(rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#AIF-scheme_node'),
						rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#comment'),
						rdflib.Literal('In AIF, scheme nodes capture the application of schemes (= patterns of reasoning). In Cohere, this is equivalent to a typed link, where the type is the specific scheme used by the S-node in AIF. \nIt is important to remember that even in AIF we usually have the following structure conposing a graph, that is, an I-node --> edge --> S-node --> edge --> I-node, the translation into Cohere makes the edges instantiation superfluous. Namely, this is translated as follows: (connection (simple_idea --> link (type_S-node) --> simple_idea)).', language=None, datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema#string'))),

		"""
		if language == 'default':
			lang = 'en'
		else:
			lang = language
		for s, p, o in self.rdfGraph.triples((aClass, RDFS.comment , None)):
			try:
				if o.language == lang:
					return o # # note that we return the RDF literal, not the string (in theory, it can be examined further for lang or other attributes)
			except:
				continue
		# if no language specified, just returns the first label found....
		if language == 'default':
			for s, p, o in self.rdfGraph.triples((aClass, RDFS.comment , None)):
				return o
		return None



	def get_classRepresentation(self, aClass):
		"""		method that returns a dictionary with chosen attributes of a class
				Useful for creating arbitraty representation of a class, eg name + comments + label etc..
				Modify as needed.. this could be the basis for an ORM built on top of rdflib...
						"""
		temp = {}
		temp['class'] = aClass
		temp['classname'] = self.uri2niceString(aClass)
		temp['comment'] = self.get_classComment(aClass)
		temp['label'] = self.get_EntityLabel(aClass)
		temp['treelevel'] = self.get_classTreeLevel(aClass)
		return temp




	def get_namespaces(self, only_base = False):
		""" wrapper function: return either the base namespace only, or all of them

		Namespaces are given in this format:

		In [01]: for x in rdfGraph.namespaces():
				....:			print x
				....:
				....:
		('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
		('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
		(u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
		('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
		('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
		(u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))


				"""
		# we assume that a base namespace is implied by an empty prefix
		if only_base:
			ll = [x for x in self.rdfGraph.namespaces() if x[0] == '']
			if ll:
				return ll[0][1]
			else:
				return None
		else:
			out = []
			for x in self.rdfGraph.namespaces():
				if x[0]:
					out.append(x)
				else: # if the namespace is blank (== base)
					prefix = self.inferNamespacePrefix(x[1])
					if prefix:
						out.append((prefix, x[1]))
					else:
						out.append(('base', x[1]))
			return out




	###########
	# PROPERTY METHODS 
	###########


	def get_classProperties(self, aClass, class_role = "domain", prop_type = "", inherited = False):
		"""
		Gets all the properties for a class
		Defaults to properties that have that class in the domain space; pass 'range' to have the other ones.
		TODO: prop_type is meant to let us separate out ObjProps from DataTypeProps
		TODO: If 'inherited' is set to True, it returns ONLY the inherited properties.
		"""
		exit = []
		if aClass in self.allclasses:
			if not inherited:
				if class_role == "domain":
					for s, v, o in self.rdfGraph.triples((None, RDFS.domain , aClass)):
						if s not in exit:
							exit.append(s)
				elif class_role == "range":
					for s, v, o in self.rdfGraph.triples((None, RDFS.range , aClass)):
						if s not in exit:
							exit.append(s)
			else:
				pass # TODO
		return exit
		


	def get_propertyRange(self, prop):
		exit = []
		for s, v, o in self.rdfGraph.triples((prop, RDFS.range , None)):
			if o not in exit:
				exit.append(o)
		return exit
		
	def get_propertyDomain(self, prop):
		exit = []
		for s, v, o in self.rdfGraph.triples((prop, RDFS.domain , None)):
			if o not in exit:
				exit.append(o)
		return exit


	def _getAllProperties(self, classPredicate = ""):
		"""
		Extracts all the properties (OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property) declared in a model.
		The method is unprotected (single underscore) because we might want to call it from the OntosPy object directly, just to see if there is *any* property available.... 
		"""
		rdfGraph = self.rdfGraph
		exit = []
		if not classPredicate:
			for s, v, o in rdfGraph.triples((None, RDF.type , RDF.Property)):
				exit.append(s)
			for s, v, o in rdfGraph.triples((None, RDF.type , OWL.ObjectProperty)):
				exit.append(s)
			for s, v, o in rdfGraph.triples((None, RDF.type , OWL.DatatypeProperty)):
				exit.append(s)
		else:
			if classPredicate == "rdf.property":
				for s, v, o in rdfGraph.triples((None, RDF.type , RDF.Property)):
					exit.append(s)
			elif classPredicate == "owl.objectproperty":
				for s, v, o in rdfGraph.triples((None, RDF.type , OWL.ObjectProperty)):
					exit.append(s)
			elif classPredicate == "owl.datatypeproperty":
				for s, v, o in rdfGraph.triples((None, RDF.type , OWL.DatatypeProperty)):
					exit.append(s)
			else:
				raise exceptions.Error("ClassPredicate must be either 'rdf.property' or 'owl.objectproperty' or 'owl.datatypeproperty'")

		exit = remove_duplicates(exit)
		return sort_uri_list_by_name(exit)






	###########
	# INSTANCE METHODS and SESSION GRAPH
	###########


	def setSessionGraphNamespace(self, ns):
		if ns.startswith("http://"):
			self.sessionNS = ns
		else:
			raise exceptions.Error("Please provide a URI starting with 'http://'..")

	def serializeSessionGraph(self, format=""):
		""" Shortcut that outputs the session graph
			TODO: add format specs..
	   """
		if format:
			return self.sessionGraph.serialize(format=format)
		else:
			return self.sessionGraph.serialize()



	def get_instance_byname(self, name, exact = False):
		"""
		Not very fast: every time self.get_allInstances() is called.. 
		TODO: find a better solution, maybe load all instances at startup?
		"""
		temp = []
		if name:
			for x in self.get_allInstances():
				if exact:
					if x.__str__().lower() == str(name).lower():
						return x
				else:
					if x.__str__().lower().find(str(name).lower()) >= 0:
						temp.append(x)
		return temp
		

	def get_allInstances(self):
		returnlist = []
		for c in self.toplayer:
			returnlist.extend(self.get_classInstances(c, onlydirect = False))
		if returnlist:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return returnlist



	def get_classInstances(self, aClass, onlydirect = True):
		""" 
		Gets all the (direct by default) instances of a class
		"""
		if aClass in self.allclasses:
			returnlist = []
			for s, v, o in self.rdfGraph.triples((None , RDF.type , aClass)):
				returnlist.append(s)
			if not onlydirect:
				for sub in self.get_classAllSubs(aClass):
					for s, v, o in self.rdfGraph.triples((None , RDF.type , sub)):
						returnlist.append(s)
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			raise exceptions.Error("Class is not available in current ontology")


	def addInstance(self, aClass, anInstance, ns = None):
		""" 2011-07-26: 
			Adds or creates a class-instance to the session-graph (and returns the instance).
			If a URIRef object is passed, that's ok. Also, if a string is passed, we create a URI using the 
			default namespace for the Session graph.
			p.s. No need to check for duplicates: rdflib does that already!
	   """
		if aClass in self.allclasses:
			if type(anInstance) == URIRef:
				self.sessionGraph.add((anInstance, RDF.type, aClass))
				return anInstance
			elif type(anInstance) == type("string") or type(anInstance) == type(u"unicode"):
				ns = ns or self.sessionNS  # needed?
				self.sessionGraph.add((ns[anInstance], RDF.type, aClass))
				return ns[anInstance]
			else:
				raise exceptions.Error("Instance must be a URIRef object or a String")
		else:
			raise exceptions.Error("Class is not available in current ontology")


	def get_instanceFather(self, anInstance, most_specialized=True):
		""" Returns the class an instance is instantiating.
	
		We should try to return only the direct father!		
		"""
		returnlist = []
		for s, v, o in self.rdfGraph.triples((anInstance , RDF.type , None)):
			if o in self.allclasses:  # sometimes there could be other stuff...
				returnlist.append(o)
		if most_specialized:
			return sort_uri_list_by_name(remove_duplicates(self.mostSpecialized(returnlist)))
		else:
			return sort_uri_list_by_name(remove_duplicates(returnlist))

	def get_instanceSiblings(self, anInstance):
		""" Returns the siblings of an instance  """
		returnlist = []
		for aClass in self.get_instanceFather(anInstance):
			returnlist.extend(self.get_classInstances(aClass))
		return sort_uri_list_by_name(remove_duplicates(returnlist))








	###########
	# UTILITIES  
	###########



	def printTree(self):
		""" print directly to stdout the taxonomical tree of an ontology """

		def tree_inner(rdfGraph, aClass, level):
			for sub in self.get_classDirectSubs(aClass):
				printDebug("%s%s" % ("-" * 4 * level, self.uri2niceString(sub)))
				tree_inner(rdfGraph, sub, (level + 1))

		for top in self.toplayer:
			printDebug(self.uri2niceString(top))
			tree_inner(self.rdfGraph, top, 1)



	def get_HTMLTree(self, element = 0, treedict = None):
		""" outputs an html tree representation based on the dictionary one above
		NOTE: Copy and modify this function if you need some different type of html..

		EG:

		<ul id="example" class="filetree">
				<li><span class="folder">Folder 2</span>
						<ul>
								<li><span class="folder">Subfolder 2.1</span>
										<ul>
												<li><span class="file">File 2.1.1</span></li>
												<li><span class="file">File 2.1.2</span></li>
										</ul>
								</li>
								<li><span class="file">File 2.2</span></li>
						</ul>
				</li>
				<li class="closed"><span class="folder">Folder 3 (closed at start)</span></li>
				<li><span class="file">File 4</span></li>
		</ul>

		"""
		if not treedict:
			treedict = self.__getTree()
		stringa = "<ul>"
		for x in treedict[element]:
			# print x
			stringa += "<li>%s" % self.uri2niceString(x)
			stringa += self.get_HTMLTree(x, treedict)
			stringa += "</li>"
		stringa += "</ul>"
		return stringa




	def uri2niceString(self, aUri):
		""" from a URI, returns a nice string representation that uses also the namespace symbols
				Cuts the uri of the namespace, and replaces it with its shortcut (for base, attempts to infer it or
				leaves it blank)

				In [77]: for x in g.namespaces():
						....:	print x
						....:
						....:
				('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
				('', rdflib.URIRef('http://purl.org/ontology/bibo/'))	# <=== note it's blank for the base NS
				(u'ns', rdflib.URIRef('http://www.w3.org/2003/06/sw-vocab-status/ns#'))

		"""
		stringa = aUri.__str__()		#gets the string within a URI
		for aNamespaceTuple in self.rdfGraph.namespaces():
			try: # check if it matches the available NS
				if stringa.find(aNamespaceTuple[1].__str__()) == 0:
					if aNamespaceTuple[0]: # for base NS, it's empty
						stringa = aNamespaceTuple[0] + ":" + stringa[len(aNamespaceTuple[1].__str__()):]
					else:
						prefix = self.inferNamespacePrefix(aNamespaceTuple[1])
						if prefix:
							stringa = prefix + ":" + stringa[len(aNamespaceTuple[1].__str__()):]
						else:
							stringa = "base:" + stringa[len(aNamespaceTuple[1].__str__()):]
			except:
				stringa = "error"
		return stringa



	def inferNamespacePrefix(self, aUri):
		""" Method that from a URI returns the last bit, eg from <'http://www.w3.org/2008/05/skos#'> we extract
		the <skos> string and use it as a namespace prefix when rendering the ontology
		"""
		stringa = aUri.__str__()
		try:
			prefix = stringa.replace("#", "").split("/")[-1]
		except:
			prefix = ""
		return prefix



	def get_name_and_namespace(self, aUri):
		""" Method that from a URI returns the namespace + last bit
			eg from <'http://www.w3.org/2008/05/skos#something'> we extract
			the 'http://www.w3.org/2008/05/skos' and 'something'
			eg from <'http://www.w3.org/2003/01/geo/wgs84_pos'> we extract
			the 'http://www.w3.org/2003/01/geo/' and 'wgs84_pos'
		"""
		stringa = aUri.__str__()
		try:
			ns = stringa.split("#")[0]
			name = stringa.split("#")[1]
		except:
			ns = stringa.rsplit("/", 1)[0]
			name = stringa.rsplit("/", 1)[1]
		return (name, ns)


	def draw_ontograph(self, fileposition):
		"""visualize the graph using pyGraphViz
		Possible Layouts: http://rss.acs.unt.edu/Rdoc/library/Rgraphviz/html/GraphvizLayouts.html
		"""
		try:
			import pygraphviz as pgv
		except:
			return "You need to install pygraphviz for this operation."

		G = pgv.AGraph(rankdir="BT") # top bottom direction
		for s, v, o in rdfGraph.triples((None, RDFS.subClassOf , None)):
			G.add_edge(self.uri2niceString(s), self.uri2niceString(o))
		G.layout(prog='dot')	# eg dot, neato, twopi, circo, fdp
		G.draw(fileposition)
		printDebug("\n\n", "_" * 50, "\n\n")
		printDebug("Drawn graph at %s" % fileposition)





















##################
# Thu Mar 17 19:07:30 GMT 2011
# HOW TO USE THIS FILE IN STANDALONE MODE:
#
##################



DEFAULT_ONTO = "http://xmlns.com/foaf/0.1/"


def main(argv):
	"""
	If you run from the command line, it shows info about the default onto, or pass it a URI as an argument for where to look for an ontology

	>>> python OntosPy.py
	>>> python OntosPy.py http://xmlns.com/foaf/0.1/
	>>> python OntosPy.py http://purl.org/ontology/mo/


	"""
	if argv:
		onto = OntosPy(argv[0])
	else:
		onto = OntosPy(DEFAULT_ONTO)

	rdfGraph = onto.rdfGraph

	print "_" * 50
	print "\nGRAPH = %s" % onto.baseURI
	print "TRIPLES = %s" % len(rdfGraph)
	print "_" * 50
	
	for x, y in onto.get_OntoAnnotations():
		print "%s : %s" % (x, y)
	print "\nNAMESPACES:\n"
	for x in onto.get_namespaces():
		print "%s : %s" % (x[0], x[1])

	print "_" * 50, "\n"


	print "MAIN TAXONOMY:\n"
	onto.printTree()
	print "_" * 50, "\n"

	if False:  # TODO: show on demand depending on keyword

		print "\n\n", "_" * 50, "\n\n"
		print "Classes found: ", str(len(onto.allclasses)), " \n", str([onto.uri2niceString(x).upper() for x in onto.allclasses])
		print "_" * 20
		for s in onto.allclasses:
			# get the subject, treat it as string and strip the initial namespace
			print "Class : " , onto.uri2niceString(s).upper()
			print "direct_subclasses: ", str(len(onto.get_classDirectSubs(s))), " = ", 			str([onto.uri2niceString(x) for x in  onto.get_classDirectSubs(s)])
			print "all_subclasses : ", str(len(onto.get_classAllSubs(s, []))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_classAllSubs(s, [])])
			print "direct_supers : ", str(len(onto.get_classDirectSupers(s))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_classDirectSupers(s)])
			print "all_supers : ", str(len(onto.get_classAllSupers(s, []))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_classAllSupers(s, [])])
			print "Domain of : ", str(len(onto.get_classProperties(s, class_role = "domain"))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_classProperties(s, class_role = "domain")])
			print "Range of : ", str(len(onto.get_classProperties(s, class_role = "range"))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_classProperties(s, class_role = "range")])
			print "_" * 10, "\n"

		print "_" * 50, "\n\n", "_" * 50, "\n\n"
		print "Object Properties found: ", str(len(onto.allobjproperties)), " \n", str([onto.uri2niceString(x).upper() for x in onto.allobjproperties])
		print "\n\n"
		for s in onto.allobjproperties: 
			print "ObjProperty : " , onto.uri2niceString(s).upper()
			print "Domain : ", str(len(onto.get_propertyDomain(s))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_propertyDomain(s)])
			print "Range : ", str(len(onto.get_propertyRange(s))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_propertyRange(s)])
			print "_" * 10, "\n"
		
		
		print "_" * 50, "\n\n",
		print "Datatype Properties found: ", str(len(onto.alldataproperties)), " \n", str([onto.uri2niceString(x).upper() for x in onto.alldataproperties])
		print "\n\n"
		for s in onto.alldataproperties: 
			print "DataProperty : " , onto.uri2niceString(s).upper()
			print "Domain : ", str(len(onto.get_propertyDomain(s))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_propertyDomain(s)])
			print "Range : ", str(len(onto.get_propertyRange(s))), " = ", 		 	str([onto.uri2niceString(x) for x in  onto.get_propertyRange(s)])
			print "_" * 10, "\n"
	
	if False:
		onto.draw_ontograph(rdfGraph, '/tmp/graph.png')










if __name__ == '__main__':
	main(sys.argv[1:])
