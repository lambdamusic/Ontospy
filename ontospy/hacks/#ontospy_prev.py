# !/usr/bin/env python
#  -*- coding: UTF-8 -*-




"""
ONTOSPY
Copyright (c) 2013-2016 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

Run it from the command line by passing it an ontology URI as an argument in order to 
show basic info about that ontology (FOAF). 

>>> python ontospy.py http://xmlns.com/foaf/0.1/

More info in the README file.

"""


import sys, os, urllib2, optparse

import rdflib	 # so we have it available as a namespace
from rdflib import Namespace, exceptions, URIRef, RDFS, RDF, BNode


from libs.utils import *
import libs.OWL
import libs.DUBLINCORE as DC
import libs.famous as FAMOUS_ONTOLOGIES

from _version import *





##################
#
#  constants
#
##################



DEFAULT_SESSION_NAMESPACE = "http://www.example.org/session/resource#"
DEFAULT_ONTO = "http://xmlns.com/foaf/0.1/"





##################
#
# The main class
#
##################



class Ontology(object):
	"""
	Class that includes methods for manipulating an RDF/RDFS/OWL graph at the ontological level
	"""


	def __init__(self, uri=False, aformat=""):
		"""
		Class that includes methods for manipulating an RDF/RDFS/OWL graph at the ontological level

		uri: a valid ontology uri (could be a local file path too)

		"""

		super(Ontology, self).__init__()

		self.rdfGraph = rdflib.Graph()
		self.ontologyURI = None
		self.ontologyPrettyURI = None
		self.ontologyPhysicalLocation = None
		self.ontologyNamespaces = None

		self.allclasses = None		
		self.allinstances = None
		self.allrdfproperties = None
		self.allobjproperties = None
		self.alldataproperties = None
		self.allannotationproperties = None
		self.allinferredproperties = None
		self.allproperties = None

		self.toplayer = None
		self.classTreeMaxDepth = None
		self.sessionGraph = None
		self.sessionNS = None	
		# self.testallclasses = None	
		self.topObjProperties = None
		self.topDataProperties = None
		self.ontologyClassTree = None

		if uri:
			self.loadUri(uri, aformat)
		else:
			printDebug("Ontology instance created. Use the <loadUri> method to load an ontology.")

	def __repr__(self):
		return "<Ontology object for URI: %s - %d triples>" % (self.ontologyPrettyURI, len(self.rdfGraph))



	def __setup(self, uri):
		"""
		After a URI/graph has been loaded successfully, set up all the object params
		"""
		#first make sure we have a uri-string
		if type(uri) != type("string"):
			try:
				uri = uri.name # assuming it's a file
			except:
				uri = str(uri)
		else:
			if not uri.startswith("http:"):
				uri = "file://%s#" % os.path.realpath(uri) 
			
				
		self.ontologyPhysicalLocation = uri
		self.ontologyURI = self.__getOntologyURI(return_as_string=False, tryDC_metadata=True) or uri
		self.ontologyPrettyURI = self.__getOntologyURI(return_as_string=True, tryDC_metadata=True) or uri
		
		self.ontologyNamespaces = self.__getOntologyNamespaces()

		# let's cache some useful info for faster access		
		self.allclasses = self.__getAllClasses()		
		self.toplayer = self.__getTopclasses()
		self.allinstances = self.__getAllInstances()

		self.allrdfproperties = self.__getAllProperties(classPredicate = 'rdf.property')
		self.allobjproperties = self.__getAllProperties(classPredicate = 'owl.objectproperty')
		self.alldataproperties = self.__getAllProperties(classPredicate = 'owl.datatypeproperty')
		self.allannotationproperties = self.__getAllProperties(classPredicate = 'owl.annotationproperty')
		
		self.allinferredproperties = self.__getAllProperties(classPredicate = 'rdf.property', includeImplicit=True)
		# add together only the OWL properties
		self.allproperties = sort_uri_list_by_name(self.allobjproperties + self.alldataproperties + self.allannotationproperties)
	
		self.ontologyClassTree = self.__buildClassTree()
		self.classTreeMaxDepth = self.__ontoMaxTreeLevel()
		
		self.topObjProperties = self.__getTopProps(classPredicate="owl.objectproperty")
		self.topDataProperties = self.__getTopProps(classPredicate="owl.datatypeproperty")
		self.topAnnotationProperties = self.__getTopProps(classPredicate="owl.annotationproperty")
		self.ontologyObjPropertyTree = self.__buildPropTree(classPredicate="owl.objectproperty")
		self.ontologyDataPropertyTree = self.__buildPropTree(classPredicate="owl.datatypeproperty")
		self.ontologyAnnotationPropertyTree = self.__buildPropTree(classPredicate="owl.annotationproperty")
		
		self.sessionGraph = rdflib.Graph()
		self.sessionNS = Namespace(DEFAULT_SESSION_NAMESPACE)

		# printDebug("...Ontology instance succesfully created for <%s>" % str(self.ontologyPrettyURI))			
			
			
	def loadUri(self, uri, aformat=""):
		"""
		Loads a schema from a URI (or a python file object containing triples)
		"""
			
		try:
			if uri.startswith("www."): #support for lazy people
				uri = "http://%s" % str(uri)  
		except:
			pass # handles exception when loading triples from file or StringIO

		if aformat:
			rdf_format = aformat
		else:
			try:
				rdf_format = guess_fileformat(uri)
			except:
				# in this case it's a python file object
				rdf_format = 'xml'	


		try:
			self.rdfGraph.parse(uri, format=rdf_format)
		except:
			print ("\nError Parsing file URI (I thought it was *%s*) (follows rdflib Exception):\n" % rdf_format)  
			raise

		finally:
			self.__setup(uri=uri)
			


	##################
	#  
	#  METHODS for ONTOLOGIES
	#
	##################




	def __getOntologyURI(self, return_as_string=False, excludeBNodes = False, tryDC_metadata = False):
		"""
		Returns the ontology URI  
		
		Ideally defined using the pattern
		<uri> a http://www.w3.org/2002/07/owl#Ontology
		
		If it's expressed using a nested triple via a blank node, the DC metadata properties are tested.
		You can exclude blank nodes if needed (eg for pretty printing)
		
		If nothing is found, the graph URI is taken as the defaul ontology URI

		"""
		ontoMetadata = [x for x in self.rdfGraph.subjects(RDF.type, OWL.Ontology)]

		if not ontoMetadata:
			return None
		else:			 
			if isBlankNode(ontoMetadata[0]):
				if excludeBNodes:
					return None
				if tryDC_metadata:
					checkDC_ID = [x for x in self.rdfGraph.objects(ontoMetadata[0], DC.identifier)]
					if checkDC_ID:
						return str(checkDC_ID[0]) if return_as_string else checkDC_ID[0]
						
			return str(ontoMetadata[0]) if return_as_string else ontoMetadata[0]
			
			
		

	def __getOntologyNamespaces(self, only_base = False):
		""" 
		Extract ontology namespaces. wrapper function: return either the base namespace only, or all of them

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
				else: 
					# if the namespace is blank (== we have a base namespace)
					prefix = inferNamespacePrefix(x[1])
					if prefix:
						out.append((prefix, x[1]))
					else:
						out.append(('base', x[1]))
			if self.ontologyURI not in [y for x,y in self.rdfGraph.namespaces()]:
				# if not base namespace is set, try to simulate one
				out.append(('this', self.ontologyURI))
		
			return sorted(out)




	def ontologyAnnotations(self, niceURI=False, excludeProps=False, excludeBNodes = False, ):
		"""
		Method that tries to get *all* the available annotations for an OWL ontology.
		Returns a list of 2-elements tuples (annotation-uri, annotation-values (as list))
		"""		
		if self.ontologyURI:
			# return entityTriples(self, self.ontologyURI, niceURI=niceURI, excludeProps=excludeProps, excludeBNodes = excludeBNodes)
			
			return [(uri2niceString(y, self.ontologyNamespaces), uri2niceString(z, self.ontologyNamespaces)) for y,z in entityTriples(self.rdfGraph, self.ontologyURI, excludeProps=excludeProps, excludeBNodes = excludeBNodes)]
		


	def ontologyStats(self):
		"""
		Returns a list of tuples containining interesting stats about the ontology
		"""
		out = []
		out += [("Triples", len(self.rdfGraph))]
		out += [("Classes", len(self.allclasses))]
		out += [("Object Properties", len(self.allobjproperties))]
		out += [("Datatype Properties", len(self.alldataproperties))]
		out += [("Individuals", len(self.allinstances))]
		return out



	def serializeOntologyGraph(self, format=""):
		""" Shortcut that outputs the ontology graph
			TODO: add format specs..
	   """
		if format:
			return self.rdfGraph.serialize(format=format)
		else:
			return self.rdfGraph.serialize()
			






	###########
	#
	# SESSION GRAPH
	#
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





	##################
	#  
	#  METHODS for MANIPULATING RDFS/OWL CLASSES 
	# 
	#  RDFS:class vs OWL:class cf. http://www.w3.org/TR/owl-ref/ section 3.1
	#
	##################



	def __getAllClasses(self, classPredicate = "", includeDomainRange=False, includeImplicit=False, removeBlankNodes = True, addOWLThing = True, excludeRDF_OWL=True):
		"""
		Extracts all the classes from an rdf graph.

		It uses RDFS and OWL predicate by default; also, we extract non explicitly declared classes.
		
		OWL:Thing is added by default as the class of all OWL classes.

		classPredicate: 'rdfs' or 'owl' (defaults to "" = both)
		includeDomainRange: boolean (defaults to False)
		includeImplicit: boolean (defaults to False)
		removeBlankNodes: boolean (defaults to True)
		addOWLThing: boolean (defaults to True)
		excludeRDF_OWL: exclude all classes from RDF/RDFS/OWL vocabs that have been redefined.

		"""
		rdfGraph = self.rdfGraph
		exit = {}

		def addIfYouCan(x, mydict):
			if excludeRDF_OWL:
				if x.startswith('http://www.w3.org/2002/07/owl#') or  \
				   x.startswith("http://www.w3.org/1999/02/22-rdf-syntax-ns#") or \
				   x.startswith("http://www.w3.org/2000/01/rdf-schema#"):
					return mydict
			if x not in mydict:
				mydict[x] = None
			return mydict

		if addOWLThing:
			exit = addIfYouCan(OWL.Thing, exit)

		if classPredicate == "rdfs" or classPredicate == "":
			for s in rdfGraph.subjects(RDF.type , RDFS.Class):
				exit = addIfYouCan(s, exit)
		if classPredicate == "owl" or classPredicate == "":
			for s in rdfGraph.subjects(RDF.type , OWL.Class):
				exit = addIfYouCan(s, exit)

		if includeDomainRange:	# todo: should I exclude XML literals? 
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


		# get a list	
		exit = exit.keys()	
		if removeBlankNodes:
			exit = [x for x in exit if not isBlankNode(x)]
		return sort_uri_list_by_name(exit)


	def __getTopclasses(self, classPredicate = '', ignoreOWLThing = True):
		""" 
		Finds the topclass in an ontology (works also with multiple inheritance)

		"""
		returnlist = []

		for eachclass in self.allclasses:
			if ignoreOWLThing and (eachclass == OWL.Thing):
				continue
			else:
				x = self.classDirectSupers(eachclass)
				if not x:
					returnlist.append(eachclass)

		return sort_uri_list_by_name(returnlist)



	def __buildClassTree(self, father=None, out=None):
		""" 
		Reconstructs the taxonomical tree of an ontology, from the 'topClasses' 
		(= classes with no supers, see below)
		
		Returns a dictionary in which each class is a key, and its direct subs are the values.
		The top classes have key = 0

			Eg.
			{	'0':	[class1, class2], 
				class1: [class1-2, class1-3], 
				class2: [class2-1, class2-2]}
		"""
		if not father:
			out = {}
			topclasses = self.toplayer
			out[0] = [OWL.Thing]
			out[OWL.Thing] = sort_uri_list_by_name(topclasses)
			for top in topclasses:
				children = self.classDirectSubs(top)
				out[top] = sort_uri_list_by_name(children)
				for potentialfather in children:
					self.__buildClassTree(potentialfather, out)
			return out
		else:
			children = self.classDirectSubs(father)
			out[father] = sort_uri_list_by_name(children)
			for ch in children:
				self.__buildClassTree(ch, out)


				

	def __getAllClassesFromTree(self, element = 0, out = None):
		""" 
		Method that returns all the classes available, in the order given by the Tree representation.

		ps: needs "__buildClassTree" to be run first
		"""
		if not out:
			out = []

		for each in self.ontologyClassTree[element]:
			if each not in out:
				out += [each]
			out += self.__getAllClassesFromTree(each, out)
		return remove_duplicates(out)




	def __printClassTreeLevel(self, aClass, level = 0, key = 0):
		""" 
		Returns the depth level (a number) of a class in the class tree, by inspecting the tree dictionary.

		When using a multi-inheritance tree a class may have different levels. This is not supported currently. 
		So the first appearance of a class in a tree determines its level. [TODO: extend]
		
		ARGS:
		level = position in tree, used for recursion
		key	  = class name, used for recursion so to navigate the dict-representation of the class tree 
		"""
		for element in self.ontologyClassTree[key]:
			if element == aClass:
				return level
			test = self.__printClassTreeLevel(aClass, level + 1, element)
			if test:
				return test



	def __ontoMaxTreeLevel(self):
		"""
		Returns the max depth of the ontology class tree
		"""
		n = 0
		for aClass in self.allclasses:
			temp = self.__printClassTreeLevel(aClass)
			if temp > n:
				n = temp
		return n




	def classRepresentation(self, aClass):
		"""		
		Method that returns a dictionary with chosen attributes of a class
		
		Useful for creating arbitraty representation of a class, eg name + comments + label etc..
		
		TODO: refactor as needed.. this could be the basis for an ORM built on top of rdflib...
		"""
		
		temp = {}
		namespaces = self.ontologyNamespaces
		temp['class'] = aClass
		temp['classname'] = uri2niceString(aClass, namespaces)
		# temp['alltriples'] = entityTriples(self, aClass, niceURI=True)
		temp['alltriples'] = [(uri2niceString(y, namespaces), uri2niceString(z, namespaces)) for y,z in entityTriples(self.rdfGraph, aClass)] 
		temp['comment'] = entityComment(self.rdfGraph, aClass)
		temp['label'] = entityLabel(self.rdfGraph, aClass)
		temp['treelevel'] = self.__printClassTreeLevel(aClass)
		temp['isdomainfor'] = self.classDomainFor(aClass)
		
		if aClass != OWL.Thing and aClass in self.allclasses:
			temp['isdefined'] = True
			

		return temp


	def classFind(self, name, exact = False):
		"""
		Find a class from its name (string representation of URI or part of it) within an ontology graph.

		Returns a list that in the 'exact' case will have one element only

		Args:
		exact: boolean (=exact string matching)

		EG: 
		ship = o.classFind("http://purl.com/net/conflict#Ship", True)
		Attempts to match classes with extract name.

		"""
		temp = []
		if name:
			for x in self.allclasses:
				if exact:
					if x.__str__().lower() == str(name).lower():
						return [x]
				else:
					if x.__str__().lower().find(str(name).lower()) >= 0:
						temp.append(x)
		return temp


	# SECTION: 
	# methods for getting ancestors and descendants of classes: by default, we do not include blank nodes


	def classDirectSupers(self, aClass, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of direct superclasses
		Note: it always avoid returning OWL:Thing as that is the implicit superclass of all classes
		"""
		returnlist = []
		for o in self.rdfGraph.objects(aClass, RDFS.subClassOf):
			if not (o == OWL.Thing):
				if excludeBnodes:
					if not isBlankNode(o):
						returnlist.append(o)
				else:
					returnlist.append(o)
		if sortUriName:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return remove_duplicates(returnlist)


	def classDirectSubs(self, aClass, excludeBnodes = True, sortUriName = False ):
		"""
		Return a list of direct subclasses
		"""
		returnlist = []
		for s, v, o in self.rdfGraph.triples((None, RDFS.subClassOf , aClass)):
			if excludeBnodes:
				if not isBlankNode(s):
					returnlist.append(s)
			else:
				returnlist.append(s)
		if sortUriName:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return remove_duplicates(returnlist)


	def classAllSupers(self, aClass, excludeBnodes = True, sortUriName = False ):
		"""
		Return a list of all superclasses >> wrapper with ordering etc..
		"""
		returnlist = self.__classAllSupers(aClass, None, excludeBnodes, sortUriName)
		if sortUriName:			 
			return sort_uri_list_by_name(returnlist)
		else:
			if returnlist:
				returnlist.reverse()
		return returnlist
			
	def __classAllSupers(self, aClass, returnlist = None, excludeBnodes = True, sortUriName = False ):
		"""
		Return a list of all superclasses >> Inner recursive method
		"""
		if returnlist == None:	# trick to avoid mutable objs python prob...
			returnlist = []
		for ssuper in self.classDirectSupers(aClass, excludeBnodes, sortUriName):
			returnlist.append(ssuper)
			self.__classAllSupers(ssuper, returnlist, excludeBnodes, sortUriName)
		return remove_duplicates(returnlist)

			

	def classAllSubs(self, aClass, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of all subclasses
		"""
		returnlist = self.__classAllSubs(aClass, None, excludeBnodes, sortUriName)
		if sortUriName:			 
			return sort_uri_list_by_name(returnlist)
		else:
			if returnlist:
				returnlist.reverse()
		return returnlist

			
	def __classAllSubs(self, aClass, returnlist = None, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of all subclasses >> Inner Recursive Method
		"""
		if returnlist == None:
			returnlist = []
		for sub in self.classDirectSubs(aClass, excludeBnodes):
			returnlist.append(sub)
			self.__classAllSubs(sub, returnlist, excludeBnodes)
		return remove_duplicates(returnlist)



	def classSiblings(self, aClass, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of siblings for a given class (= direct children of the same parent(s))
		"""
		returnlist = []
		for father in self.classDirectSupers(aClass, excludeBnodes):
			for child in self.classDirectSubs(father, excludeBnodes):
				if child != aClass:
					returnlist.append(child)
		if sortUriName:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return remove_duplicates(returnlist)



	def classMostSpecialized(self, classlist):
		"""
		From a list of classes, returns a list of the leafs only. 
		If the classes belong to different branches, or they are at the same depth level (= siblings), all of them are returned.
		"""
		returnlist = []
		superslistlists = [self.classAllSupers(aClass) for aClass in classlist if aClass in self.allclasses]
		for aClass in classlist:
			flag = False
			for superslist in superslistlists:
				# DIRTY hack to make sure all trees originate from OWL.Thing...
				if aClass in superslist + [OWL.Thing]:
					flag = True
			if flag == False:
				returnlist.append(aClass)
		return returnlist


	def classMostGeneric(self, classlist):
		"""
		From a list of classes, returns a list of the most generic ones only. 
		If the classes belong to different branches, or both are at the same level, all are returned
		"""
		returnlist = []
		superslist = [self.classAllSubs(aClass) for aClass in classlist if aClass in self.allclasses]
		for aClass in classlist:
			flag = False
			for supers in superslist:
				if aClass in supers:
					flag = True
			if flag == False:
				returnlist.append(aClass)
		return returnlist
				

	def classDomainFor(self, aClass, inherited = False ):
		"""
		Gets all the properties that declare this class as domain.
		
		Returns a list of tuples which can contain more than one tuple if inherited=True
		
		Eg [(superClass, [properties]), (superClass, [properties]), (class, [properties])] 
		
		"""
		exit = []
		if not inherited:
			for s, v, o in self.rdfGraph.triples((None, RDFS.domain , aClass)):
				if s not in exit:
					exit.append(s)
			return [(aClass, sort_uri_list_by_name(exit))]
		else:
			tree =	self.classAllSupers(aClass) + [aClass]
			for cl in tree:
				temp = []
				for s, v, o in self.rdfGraph.triples((None, RDFS.domain , cl)):
					if s not in temp:
						temp.append(s)
				if temp:
					exit.append((cl, sort_uri_list_by_name(temp)))
					
			return exit


	def classRangeFor(self, aClass, inherited = False ):
		"""
		Gets all the properties that have this class as domain.
		TODO: prop_type is meant to let us separate out ObjProps from DataTypeProps
		TODO: If 'inherited' is set to True, it returns ONLY the inherited properties.
		"""
		exit = []
		if not inherited:
			for s, v, o in self.rdfGraph.triples((None, RDFS.range , aClass)):
				if s not in exit:
					exit.append(s)

		else:
			tree =	self.classAllSupers(aClass) + [aClass]
			for cl in tree:
				for s, v, o in self.rdfGraph.triples((None, RDFS.range , cl)):
					if s not in exit:
						exit.append(s)	
		return exit
		
		

	def classProperties(self, aClass):
		"""
		Gets all the properties defined for a class, and their values (= the triples)
		"""
		exit = []
		for s, v, o in self.rdfGraph.triples((aClass, None , None)):
			exit.append((v,o))
		return exit



	def classInstances(self, aClass, onlydirect = True):
		""" 
		Gets all the (direct by default) instances of a class
		"""
		if aClass in self.allclasses:
			returnlist = []
			for s, v, o in self.rdfGraph.triples((None , RDF.type , aClass)):
				returnlist.append(s)
			if not onlydirect:
				for sub in self.classAllSubs(aClass):
					for s, v, o in self.rdfGraph.triples((None , RDF.type , sub)):
						returnlist.append(s)
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			raise exceptions.Error("Class is not available in current ontology")





	###########

	# METHODS for MANIPULATING RDFS/OWL PROPERTIES

	###########


	def __getAllProperties(self, classPredicate = "", includeImplicit=False):
		"""
		Extracts all the properties declared in a model.
		
		Args:
		> classPredicate: a mapping to one of the allowed OWL props
		
		> includeImplicit: gets all predicates from triples and infers that they are all RDF properties (even if not explicitly declared)
		
		Corresponding RDF predicates: 
		OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty, RDF.Property 

		"""
		rdfGraph = self.rdfGraph
		exit = {}

		if classPredicate not in ["", 'rdf.property', 'owl.objectproperty','owl.datatypeproperty', 'owl.annotationproperty']:
			raise exceptions.Error("ClassPredicate must be either 'rdf.property' or 'owl.objectproperty' or 'owl.datatypeproperty' or 'owl.annotationproperty' ")

		def addIfYouCan(x, mydict):
			if x not in mydict:
				mydict[x] = None
			return mydict

		if classPredicate == "rdf.property" or "":
			for s in rdfGraph.subjects(RDF.type , RDF.Property):
				exit = addIfYouCan(s, exit)
			if includeImplicit:
				# includes everything that appears as a predicate; 
				# below we add also owl properties due to inheritance: they are instances of of rdf:property subclasses
				for s in rdfGraph.predicates(None, None):
					exit = addIfYouCan(s, exit)

		if classPredicate == "owl.objectproperty" or classPredicate == "" or includeImplicit:
			for s in rdfGraph.subjects(RDF.type , OWL.ObjectProperty):
				exit = addIfYouCan(s, exit)
		if classPredicate == "owl.datatypeproperty" or classPredicate == "" or includeImplicit: 
			for s in rdfGraph.subjects(RDF.type , OWL.DatatypeProperty):
				exit = addIfYouCan(s, exit)

		if classPredicate == "owl.annotationproperty" or classPredicate == "" or includeImplicit: 
			for s in rdfGraph.subjects(RDF.type , OWL.AnnotationProperty):
				exit = addIfYouCan(s, exit)


		# get a list	
		exit = exit.keys() 
		return sort_uri_list_by_name(exit)


	def __getTopProps(self, classPredicate = '', includeImplicit=False):
		""" 
		Finds the topclass in an ontology (works also with multiple inheritance)

		"""
		returnlist = []
		searchspace = []
				
		if classPredicate not in ["", 'rdf.property', 'owl.objectproperty','owl.datatypeproperty', 'owl.annotationproperty']:
			raise exceptions.Error("ClassPredicate must be blank or either 'rdf.property' or 'owl.objectproperty' or 'owl.datatypeproperty' or 'owl.annotationproperty'")

		if classPredicate == "rdf.property" or classPredicate == "":
			searchspace += self.allrdfproperties
		if classPredicate == "owl.objectproperty" or classPredicate == "":
			searchspace += self.allobjproperties
		if classPredicate == "owl.datatypeproperty" or classPredicate == "": 
			searchspace += self.alldataproperties
		if classPredicate == "owl.annotationproperty" or classPredicate == "": 
			searchspace += self.allannotationproperties			
			
		if includeImplicit:
			searchspace += self.allinferredproperties
			
		for eachprop in searchspace:
			x = self.propertyDirectSupers(eachprop)
			if not x:
				returnlist.append(eachprop)

		return sort_uri_list_by_name(returnlist)
		

	def __buildPropTree(self, classPredicate, father=None, out=None,):
		""" 
		Reconstructs the taxonomical property tree of an ontology
		
		Returns a dictionary in which each proeprty is a key, and its direct subs are the values.
		The top properties have key = 0
		"""
		if not father:
			out = {}
			if classPredicate == "owl.datatypeproperty":
				topprops = self.topDataProperties
			elif classPredicate == "owl.annotationproperty":
				topprops = self.topAnnotationProperties
			else:
				topprops = self.topObjProperties
 
			out[0] = sort_uri_list_by_name(topprops)
			for top in topprops:
				children = self.propertyDirectSubs(top)
				out[top] = sort_uri_list_by_name(children)
				for potentialfather in children:
					self.__buildPropTree(classPredicate, potentialfather, out)
			return out
		else:
			children = self.propertyDirectSubs(father)
			out[father] = sort_uri_list_by_name(children)
			for ch in children:
				self.__buildPropTree(classPredicate, ch, out)
		

	def propertyRepresentation(self, aProp):
		"""		
		Similar to the class representation: could be a stub for an OO version of this..
		"""		
		temp = {}
		namespaces = self.ontologyNamespaces
		temp['prop'] = aProp
		temp['propname'] = uri2niceString(aProp, namespaces)
		# temp['alltriples'] = entityTriples(self, aProp, niceURI=True)
		temp['alltriples'] = [(uri2niceString(y, namespaces), uri2niceString(z, namespaces)) for y,z in entityTriples(self.rdfGraph, aProp)] 
		temp['comment'] = entityComment(self.rdfGraph, aProp)
		temp['label'] = entityLabel(self.rdfGraph, aProp)
		temp['domain'] = [self.classRepresentation(clas) for clas in self.propertyDomain(aProp)]
		temp['range'] = [self.classRepresentation(clas) for clas in self.propertyRange(aProp)]

		if aProp in self.allproperties:
			temp['isdefined'] = True
				
		return temp


	def propertyFind(self, name, exact = False, classPredicate = "", includeImplicit=False):
		"""
		Find a property from its name (string representation of URI or part of it) within an ontology graph.

		Returns a list that in the 'exact' case will have one element only

		classPredicate: one of "rdf.property", "owl.objectproperty", "owl.datatypeproperty"
		
		EG:
		> onto.propertyFind("purl.org", classPredicate="owl.objectproperty")
		"""
		temp = []
		searchspace = []
				
		if classPredicate not in ["", 'rdf.property', 'owl.objectproperty','owl.datatypeproperty']:
			raise exceptions.Error("ClassPredicate must be blank or either 'rdf.property' or 'owl.objectproperty' or 'owl.datatypeproperty'")

		if classPredicate == "rdf.property" or classPredicate == "":
			searchspace += self.allrdfproperties
		if classPredicate == "owl.objectproperty" or classPredicate == "":
			searchspace += self.allobjproperties
		if classPredicate == "owl.datatypeproperty" or classPredicate == "": 
			searchspace += self.alldataproperties
		if includeImplicit:
			searchspace += self.allinferredproperties				   
		
		if name:
			for x in searchspace:
				if exact:
					if x.__str__().lower() == str(name).lower():
						return [x]
				else:
					if x.__str__().lower().find(str(name).lower()) >= 0:
						temp.append(x)
		return temp


	def propertyRange(self, prop):
		exit = []
		for s, v, o in self.rdfGraph.triples((prop, RDFS.range , None)):
			if o not in exit:
				exit.append(o)
		return sort_uri_list_by_name(exit)
		
	def propertyDomain(self, prop):
		exit = []
		for s, v, o in self.rdfGraph.triples((prop, RDFS.domain , None)):
			if o not in exit:
				exit.append(o)
		return sort_uri_list_by_name(exit)



	# SECTION: 
	# methods for getting property hiearchies: by default, we do not include blank nodes


	def propertyDirectSupers(self, aProp, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of direct superclasses
		Note: it always avoid returning OWL:Thing as that is the implicit superclass of all classes
		"""
		returnlist = []
		for o in self.rdfGraph.objects(aProp, RDFS.subPropertyOf):
			if excludeBnodes:
				if not isBlankNode(o):
					returnlist.append(o)
			else:
				returnlist.append(o)
		if sortUriName:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return remove_duplicates(returnlist)


	def propertyDirectSubs(self, aProp, excludeBnodes = True, sortUriName = False ):
		"""
		Return a list of direct subproperties
		"""
		returnlist = []
		for x in self.rdfGraph.subjects(RDFS.subPropertyOf, aProp):
			if excludeBnodes:
				if not isBlankNode(x):
					returnlist.append(x)
			else:
				returnlist.append(x)
		if sortUriName:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return remove_duplicates(returnlist)


	def propertyAllSupers(self, aProp, excludeBnodes = True, sortUriName = False ):
		"""
		Return a list of all superprops >> wrapper with ordering etc..
		"""
		returnlist = self.__propAllSupers(aProp, None, excludeBnodes, sortUriName)
		if sortUriName:			 
			return sort_uri_list_by_name(returnlist)
		else:
			if returnlist:
				returnlist.reverse()
		return returnlist
			
	def __propAllSupers(self, aProp, returnlist = None, excludeBnodes = True, sortUriName = False ):
		"""
		Return a list of all superprops >> Inner recursive method
		"""
		if returnlist == None:	# trick to avoid mutable objs python prob...
			returnlist = []
		for ssuper in self.propertyDirectSupers(aProp, excludeBnodes, sortUriName):
			returnlist.append(ssuper)
			self.__propAllSupers(ssuper, returnlist, excludeBnodes, sortUriName)
		return remove_duplicates(returnlist)		


	def propertyAllSubs(self, aProp, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of all subproperties
		"""
		returnlist = self.__propAllSubs(aProp, None, excludeBnodes, sortUriName)
		if sortUriName:			 
			return sort_uri_list_by_name(returnlist)
		else:
			if returnlist:
				returnlist.reverse()
		return returnlist
			
	def __propAllSubs(self, aProp, returnlist = None, excludeBnodes = True, sortUriName = False):
		"""
		Return a list of all subproperties >> Inner Recursive Method
		"""
		if returnlist == None:
			returnlist = []
		for sub in self.propertyDirectSubs(aProp, excludeBnodes):
			returnlist.append(sub)
			self.__propAllSubs(sub, returnlist, excludeBnodes)
		return remove_duplicates(returnlist)




	###########

	# METHODS for MANIPULATING RDFS/OWL INSTANCES

	###########


	def __getAllInstances(self):
		returnlist = []
		for c in self.toplayer:
			returnlist.extend(self.classInstances(c, onlydirect = False))
		if returnlist:
			return sort_uri_list_by_name(remove_duplicates(returnlist))
		else:
			return returnlist


	def instanceRepresentation(self, instance):
		"""		
		Similar to the class representation: could be a stub for an OO version of this..
		"""		
		temp = {}
		namespaces = self.ontologyNamespaces
		temp['instance'] = instance
		temp['instancename'] = uri2niceString(instance, namespaces)
		# temp['alltriples'] = entityTriples(self, instance, niceURI=True)
		temp['alltriples'] = [(uri2niceString(y, namespaces), uri2niceString(z, namespaces)) for y,z in entityTriples(self.rdfGraph, instance)]
		temp['comment'] = entityComment(self.rdfGraph, instance)
		temp['label'] = entityLabel(self.rdfGraph, instance)
		fathers = self.instanceFather(instance)
		if fathers:
			temp['types'] = [self.classRepresentation(f) for f in fathers]
				
		return temp


	def instanceFind(self, name, exact = False):
		"""
		Not very fast: every time self.__getAllInstances() is called.. 

		"""
		temp = []
		if name:
			for x in self.allinstances:
				if exact:
					if x.__str__().lower() == str(name).lower():
						return x
				else:
					if x.__str__().lower().find(str(name).lower()) >= 0:
						temp.append(x)
		return temp
		



	def instanceAddForClass(self, aClass, anInstance, ns = None):
		""" 
		2011-07-26: 
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


	def instanceFather(self, anInstance, most_specialized=True):
		""" 
		Returns the class an instance is instantiating.
	
		We should try to return only the direct father!		
		"""
		returnlist = []
		for s, v, o in self.rdfGraph.triples((anInstance , RDF.type , None)):
			if o in self.allclasses:  # sometimes there could be other stuff...
				returnlist.append(o)
		if most_specialized:
			return sort_uri_list_by_name(remove_duplicates(self.classMostSpecialized(returnlist)))
		else:
			return sort_uri_list_by_name(remove_duplicates(returnlist))


	def instanceSiblings(self, anInstance):
		""" 
		Returns the siblings of an instance	 
		"""
		
		returnlist = []
		for aClass in self.instanceFather(anInstance):
			returnlist.extend(self.classInstances(aClass))
		return sort_uri_list_by_name(remove_duplicates(returnlist))





	###########

	# UTILITIES	 

	###########



	def printClassTree(self, element = 0, treedict = None, level=0):
		""" 
		Print nicely into stdout the taxonomical tree of an ontology 
		"""
		if not treedict:
			treedict = self.ontologyClassTree
		for x in treedict[element]:
			printDebug("%s%s" % ("-" * 4 * level, uri2niceString(x, self.ontologyNamespaces)))
			self.printClassTree(x, treedict, (level + 1))

	def printObjPropTree(self, element = 0, treedict = None, level=0):
		""" 
		Print nicely into stdout the taxonomical tree of an ontology 
		"""
		if not treedict:
			treedict = self.ontologyObjPropertyTree
		for x in treedict[element]:
			printDebug("%s%s" % ("-" * 4 * level, uri2niceString(x, self.ontologyNamespaces)))
			self.printObjPropTree(x, treedict, (level + 1))

	def printDataPropTree(self, element = 0, treedict = None, level=0):
		""" 
		Print nicely into stdout the taxonomical tree of an ontology 
		"""
		if not treedict:
			treedict = self.ontologyDataPropertyTree
		for x in treedict[element]:
			printDebug("%s%s" % ("-" * 4 * level, uri2niceString(x, self.ontologyNamespaces)))
			self.printDataPropTree(x, treedict, (level + 1))
			

	def ontologyHtmlTree(self, element = 0, treedict = None):
		""" 
		Builds an html tree representation based on the internal tree-dictionary representation

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
			treedict = self.ontologyClassTree
		stringa = "<ul>"
		for x in treedict[element]:
			# print x
			stringa += "<li>%s" % uri2niceString(x, self.ontologyNamespaces)
			stringa += self.ontologyHtmlTree(x, treedict)
			stringa += "</li>"
		stringa += "</ul>"
		return stringa




	def drawOntograph(self, fileposition):
		"""
		Visualize the graph using pyGraphViz (which needs to be preinstalled)

		More info on Layouts: http://rss.acs.unt.edu/Rdoc/library/Rgraphviz/html/GraphvizLayouts.html
		"""

		try:
			import pygraphviz as pgv
		except:
			return "You need to install pygraphviz for this operation."

		G = pgv.AGraph(rankdir="BT") # top bottom direction
		for s, v, o in self.rdfGraph.triples((None, RDFS.subClassOf , None)):
			G.add_edge(uri2niceString(s, self.ontologyNamespaces), uri2niceString(o, self.ontologyNamespaces))
		G.layout(prog='dot')	# eg dot, neato, twopi, circo, fdp
		G.draw(fileposition)
		print("\n\n", "_" * 50, "\n\n")
		print("Generated graph at %s" % fileposition)


	def webViz(self):
		"""
			July 10, 2014
			Visualize the graph using d3  @todo
		"""

		try:
			import webbrowser
		except:
			return "You need the webbrowser module for this operation."

		filename = 'test.html'
		
		if False:		
			# the simeplest test ever
			f = open("test.html", "w")
			f.write("<html><body><h2>It WOrks</h2><p>%s</p></body></html>" % " ".join(["<li>"+str(x)+"</li>" for x in self.allclasses]))
			f.close()
			print("\n\n", "_" * 50, "\n\n")
			print("Generated graph at %s" % os.path.realpath(filename))
			webbrowser.open('file://'+os.path.realpath("test.html"))


			
			
		if False:
			# just opens a d3 file
			thisdir = os.path.dirname(os.path.realpath(__file__))		
			print thisdir
			webbrowser.open('file://'+thisdir+"/data/templates/forcedirected.html")
			
					
		if True:
			# uses a string template with d3
			from string import Template
			ss = ""		
			for x in self.allclasses:
				if self.classDirectSupers(x):
					for directSuper in self.classDirectSupers(x):
						ss += """{source: "%s", target: "%s", type: "test"},\n""" % (uri2niceString(x, self.ontologyNamespaces), uri2niceString(directSuper, self.ontologyNamespaces))
				else:
					ss += """{source: "%s", target: "ROOT", type: "test"},\n""" % (uri2niceString(x, self.ontologyNamespaces))		
			thisdir = os.path.dirname(os.path.realpath(__file__))
			
			#open the file
			filein = open(thisdir + '/data/templates/forceDirectedTemplate.html' )
			#read it
			src = Template( filein.read() )
			#do the substitution called $graphedges in html file

			from os.path import expanduser
			home = expanduser("~")
			location = home + "/ontospy-viz.html"
			
			
			fileout = open(location, "w")
			fileout.write(src.substitute({'graphedges' : ss}))
			fileout.close()
			# webbrowser.open('file://'+os.path.realpath("ontospy-viz.html"))
			webbrowser.open('file://'+location) # note: requires 2 forwards slashes + 1 for path









##################
# 
#  STANDALONE MODE:
#
##################




def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	
	parser.add_option("-e", "--entities",
			action="store_true", default=False, dest="entities",
			help="Print out detailed information for all entities in the ontology.")

	opts, args = parser.parse_args()

	if len(args) < 1:
		parser.print_help()
		raise SystemExit, 1

	return opts, args




	
def main ():
	""" command line script """
	
	opts, args = parse_options()
	entities = opts.entities 

	try:
		onto = Ontology(args[0])
	except:
		# print "Please specify a valid endpoint. Use -h for more info."
		raise SystemExit, 1	
	
	if entities:
		printEntitiesInformation(onto)
	else:
		printBasicInfo(onto)
		




 
	
if __name__ == '__main__':
	import sys
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e

