# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.
"""

from __future__ import print_function
from itertools import chain

import rdflib

from .utils import *
from .rdf_loader import RDFLoader
from .entities import *
from .sparql_helper import SparqlHelper


class Ontospy(object):
	"""
	Object that extracts schema definitions (aka 'ontologies') from an rdf graph.

	In [3]: import ontospy

	In [5]: o = ontospy.Ontospy()

	In [7]: o.load_rdf("foaf.rdf")

	In [11]: o.build_all()

	In [13]: o.stats()
	Out[13]:
	[('Ontologies', 1),
	 ('Triples', 630),
	 ('Classes', 15),
	 ('Properties', 67),
	 ('Annotation Properties', 7),
	 ('Object Properties', 34),
	 ('Datatype Properties', 26),
	 ('Skos Concepts', 0),
	 ('Data Sources', 1)]

	"""

	def __init__(self,
				 uri_or_path=None,
				 data=None,
				 file_obj=None,
				 rdf_format="",
				 verbose=False,
				 hide_base_schemas=True,
				 hide_implicit_types=True,
				 hide_implicit_preds=True,
				 hide_individuals=True,
				 sparql_endpoint=None,
				 credentials=None,
				 build_all=True,
				 pref_title="qname",
				 pref_lang="en",
				 ):
		"""Load the graph in memory, then setup all necessary attributes.

		Parameters
		----------
		uri_or_path : [type], optional
			[description], by default None
		data : [type], optional
			[description], by default None
		file_obj : [type], optional
			[description], by default None
		rdf_format : str, optional
			[description], by default ""
		verbose : bool, optional
			[description], by default False
		hide_base_schemas : bool, optional
			[description], by default True
		hide_implicit_types : bool, optional
			[description], by default True
		hide_implicit_preds : bool, optional
			[description], by default True
		hide_individuals: bool, opt
			Extract class instances or not, by default True
		sparql_endpoint : [type], optional
			[description], by default None
		credentials : [type], optional
			[description], by default None
		build_all : bool, optional
			[description], by default True
		pref_title : str, optional
			How to display entities by default. Two options accepted: "qname" (default) or "label" for rdfs:label. 
		pref_lang : str, optional
			Default: 'en'
		"""
		
		super(Ontospy, self).__init__()

		self.rdflib_graph = None
		self.sparql_endpoint = None
		self.credentials = None  # tuple: auth credentials for endpoint if needed
		self.sources = None
		self.sparqlHelper = None
		self.pref_title = pref_title
		self.pref_lang = pref_lang
		self.hide_individuals = hide_individuals
		self.namespaces = []
		# entities buckets start with 'all_'
		self.all_ontologies = []
		self.all_classes = []
		self.all_properties = []
		self.all_properties_annotation = []
		self.all_properties_object = []
		self.all_properties_datatype = []
		self.all_skos_concepts = []
		self.all_shapes = []
		self.all_individuals = []
		self.toplayer_classes = []
		self.toplayer_properties = []
		self.toplayer_skos = []
		self.toplayer_shapes = []
		self.OWLTHING = OntoClass(rdflib.OWL.Thing, 
									rdflib.OWL.Class, 
									self.namespaces,
									False, 
									self.pref_title, 
									self.pref_lang)

		# finally:
		if uri_or_path or data or file_obj:
			self.load_rdf(uri_or_path, data, file_obj, rdf_format, verbose)
			if build_all:
				self.build_all(
					verbose=verbose,
					hide_base_schemas=hide_base_schemas,
					hide_implicit_types=hide_implicit_types,
					hide_implicit_preds=hide_implicit_preds,
					hide_individuals=hide_individuals,
					)
		elif sparql_endpoint:  # by default entities are not extracted
			self.load_sparql(sparql_endpoint, verbose, credentials)
		else:
			pass

	def __repr__(self):
		"""
		Return some info for the ontospy instance.

		note: if it's a sparql backend, limit the info returned to avoid long queries (tip: a statement like `if self.rdflib_graph` on a sparql endpoint is enough to cause a long query!)

		"""
		if self.sparql_endpoint and self.rdflib_graph != None:
			return "<Ontospy Graph (sparql endpoint = <%s>)>" % self.sparql_endpoint
		elif self.rdflib_graph != None:
			return "<Ontospy Graph (%d triples)>" % (len(self.rdflib_graph))
		else:
			return "<Ontospy object created but not initialized (use the `load_rdf` method to load an rdf schema)>"

	def load_rdf(self,
				 uri_or_path=None,
				 data=None,
				 file_obj=None,
				 rdf_format="",
				 verbose=False):
		"""Load an RDF source into an ontospy/rdflib graph"""
		loader = RDFLoader(verbose=verbose)
		loader.load(uri_or_path, data, file_obj, rdf_format)
		self.rdflib_graph = loader.rdflib_graph
		self.sources = loader.sources_valid
		self.sparqlHelper = SparqlHelper(self.rdflib_graph)
		self.namespaces = sorted(self.rdflib_graph.namespaces())

	def load_sparql(self,
					sparql_endpoint,
					verbose=False,
					credentials=None):
		"""
		Set up a SPARQLStore backend as a virtual ontospy graph

		Note: we're using a 'SPARQLUpdateStore' backend instead of 'SPARQLStore' cause otherwise authentication fails (https://github.com/RDFLib/rdflib/issues/755)

		@TODO this error seems to be fixed in upcoming rdflib versions
		https://github.com/RDFLib/rdflib/pull/744

		"""
		try:
			# graph = rdflib.Graph('SPARQLStore')
			# graph = rdflib.ConjunctiveGraph('SPARQLStore')
			graph = rdflib.ConjunctiveGraph('SPARQLUpdateStore')

			if credentials and type(credentials) == tuple:
				# https://github.com/RDFLib/rdflib/issues/343
				graph.store.setCredentials(credentials[0], credentials[1])
				# graph.store.setHTTPAuth('BASIC') # graph.store.setHTTPAuth('DIGEST')

			graph.open(sparql_endpoint)
			self.rdflib_graph = graph
			self.sparql_endpoint = sparql_endpoint
			self.sources = [sparql_endpoint]
			self.sparqlHelper = SparqlHelper(self.rdflib_graph, self.sparql_endpoint)
			self.namespaces = sorted(self.rdflib_graph.namespaces())
		except:
			printDebug("Error trying to connect to Endpoint.")
			raise
		# don't extract entities by default..


	# ------------
	# === methods to build python objects === #
	# ------------

	def build_all(self,
				  verbose=False,
				  hide_base_schemas=True,
				  hide_implicit_types=True,
				  hide_implicit_preds=True,
				  hide_individuals=True,
				  ):
		"""
		Extract all ontology entities from an RDF graph and construct Python representations of them.
		"""
		if verbose:
			printInfo("Scanning entities...", "green")
			printInfo("----------", "comment")

		self.build_ontologies()
		if verbose:
			printInfo("Ontologies.........: %d" % len(self.all_ontologies), "comment")

		self.build_classes(hide_base_schemas, hide_implicit_types)
		if verbose:
			printInfo("Classes............: %d" % len(self.all_classes), "comment")

		self.build_properties(hide_implicit_preds)
		if verbose:
			printInfo("Properties.........: %d" % len(self.all_properties), "comment")
		if verbose:
			printInfo("..annotation.......: %d" % len(self.all_properties_annotation), "comment")
		if verbose:
			printInfo("..datatype.........: %d" % len(self.all_properties_datatype), "comment")
		if verbose:
			printInfo("..object...........: %d" % len(self.all_properties_object), "comment")

		self.build_skos_concepts()
		if verbose:
			printInfo("Concepts (SKOS)....: %d" % len(self.all_skos_concepts), "comment")

		self.build_shapes()
		if verbose:
			printInfo("Shapes (SHACL).....: %d" % len(self.all_shapes), "comment")

		if not hide_individuals:
			self.build_individuals()
			if verbose:
				printInfo("Individuals........: %d" % len(self.all_individuals), "comment")			

		# self.__computeTopLayer()

		self.__computeInferredProperties()

		if verbose:
			printInfo("----------", "comment")

	def build_ontologies(self, exclude_BNodes=False, return_string=False):
		"""
		Extract ontology instances info from the graph, then creates python objects for them.

		Note: often ontology info is nested in structures like this:

		[ a owl:Ontology ;
			vann:preferredNamespacePrefix "bsym" ;
			vann:preferredNamespaceUri "http://bsym.bloomberg.com/sym/" ]

		Hence there is some logic to deal with these edge cases.
		"""
		out = []

		qres = self.sparqlHelper.getOntology()

		if qres:
			# NOTE: SPARQL returns a list of rdflib.query.ResultRow (~ tuples..)

			for candidate in qres:
				if isBlankNode(candidate[0]):
					if exclude_BNodes:
						continue
					else:
						checkDC_ID = [x for x in self.rdflib_graph.objects(
							candidate[0], rdflib.namespace.DC.identifier)]
						if checkDC_ID:
							out += [Ontology(checkDC_ID[0], 
									namespaces=self.namespaces, 
									pref_title=self.pref_title), 
									]
						else:
							vannprop = rdflib.URIRef(
								"http://purl.org/vocab/vann/preferredNamespaceUri")
							vannpref = rdflib.URIRef(
								"http://purl.org/vocab/vann/preferredNamespacePrefix")
							checkDC_ID = [x for x in self.rdflib_graph.objects(
								candidate[0], vannprop)]
							if checkDC_ID:
								checkDC_prefix = [
									x for x in self.rdflib_graph.objects(candidate[0], vannpref)]
								if checkDC_prefix:
									out += [Ontology(checkDC_ID[0],
													 namespaces=self.namespaces,
													 pref_prefix=checkDC_prefix[0],
													 pref_title=self.pref_title,
													 pref_lang=self.pref_lang,
													 )
													 ]
								else:
									out += [Ontology(checkDC_ID[0], 
											namespaces=self.namespaces, 
											pref_title=self.pref_title,
											pref_lang=self.pref_lang,
											)]

				else:
					out += [Ontology(candidate[0], 
								namespaces=self.namespaces, 
								pref_title=self.pref_title,
								pref_lang=self.pref_lang,
								)]

		else:
			pass
			# printInfo("No owl:Ontologies found")

		# finally... add all annotations/triples
		self.all_ontologies = out
		for onto in self.all_ontologies:
			onto.triples = self.sparqlHelper.entityTriples(onto.uri)
			onto._buildGraph()  # force construction of mini graph

		# sort alphabetically
		self.all_ontologies = sorted(self.all_ontologies, key=lambda x: x.uri)


	#
	#  RDFS:class vs OWL:class cf. http://www.w3.org/TR/owl-ref/ section 3.1
	#

	def build_classes(self, hide_base_schemas=True, hide_implicit_types=True):
		"""
		2015-06-04: removed sparql 1.1 queries
		2015-05-25: optimized via sparql queries in order to remove BNodes
		2015-05-09: new attempt

		Note: sparqlHelper.getAllClasses() returns a list of tuples,
		(class, classRDFtype)
		so in some cases there are duplicates if a class is both RDFS.CLass and OWL.Class
		In this case we keep only OWL.Class as it is more informative.
		"""

		self.all_classes = []  # @todo: keep adding?

		qres = self.sparqlHelper.getAllClasses(hide_base_schemas,
											   hide_implicit_types)

		for class_tuple in qres:

			_uri = class_tuple[0]
			try:
				_type = class_tuple[1]
			except:
				_type = ""

			test_existing_cl = self.get_class(uri=_uri)
			if not test_existing_cl:
				# create it
				ontoclass = OntoClass(_uri, _type, 
									 self.namespaces, 
									 False,
									 self.pref_title, 
									 self.pref_lang)
				self.all_classes += [ontoclass]
			else:
				# if OWL.Class over RDFS.Class - update it
				if _type == rdflib.OWL.Class:
					test_existing_cl.rdftype = rdflib.OWL.Class


		# add more data
		for aClass in self.all_classes:
			# print("enriching class", aClass)
			aClass.triples = self.sparqlHelper.entityTriples(aClass.uri)
			aClass._buildGraph()  # force construction of mini graph

			aClass.sparqlHelper = self.sparqlHelper

			# attach to an ontology
			for uri in aClass.getValuesForProperty(rdflib.RDFS.isDefinedBy):
				onto = self.get_ontology(uri=str(uri))
				if onto:
					onto.all_classes += [aClass]
					aClass.ontology = onto

			# add direct Supers
			directSupers = self.sparqlHelper.getClassDirectSupers(aClass.uri)

			for x in directSupers:
				superclass = self.get_class(uri=x[0])
				# note: extra condition to avoid recursive structures
				if superclass and superclass.uri != aClass.uri:
					aClass._parents.append(superclass)

					# add inverse relationships (= direct subs for superclass)
					if aClass not in superclass.children():
						superclass._children.append(aClass)

		# sort alphabetically
		self.all_classes = sorted(self.all_classes, key=lambda x: x.qname)

		# compute top layer
		# print("calc toplayer")
		exit = []
		for c in self.all_classes:
			if not c.parents():
				exit += [c]
		self.toplayer_classes = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

	def build_properties(self, hide_implicit_preds=True):
		"""
		2015-06-04: removed sparql 1.1 queries
		2015-06-03: analogous to get classes

		# instantiate properties making sure duplicates are pruned
		# but the most specific rdftype is kept
		# eg OWL:ObjectProperty over RDF:property

		"""
		self.all_properties = []  # @todo: keep adding?
		self.all_properties_annotation = []
		self.all_properties_object = []
		self.all_properties_datatype = []

		qres = self.sparqlHelper.getAllProperties(hide_implicit_preds)
		# print("rdflib query done")

		for candidate in qres:

			test_existing_prop = self.get_property(uri=candidate[0])
			if not test_existing_prop:
				# create it
				self.all_properties += [OntoProperty(candidate[0], candidate[1], 
											self.namespaces, 
											False,
											self.pref_title,
											self.pref_lang,
											)]
			else:
				# update it
				if candidate[1] and (test_existing_prop.rdftype == rdflib.RDF.Property):
					test_existing_prop.rdftype = inferMainPropertyType(candidate[1])
		# print("properties created")

		# add more data
		for aProp in self.all_properties:
			# print("enriching prop..", aProp)
			if aProp.rdftype == rdflib.OWL.DatatypeProperty:
				self.all_properties_datatype += [aProp]
			elif aProp.rdftype == rdflib.OWL.AnnotationProperty:
				self.all_properties_annotation += [aProp]
			elif aProp.rdftype == rdflib.OWL.ObjectProperty:
				self.all_properties_object += [aProp]
			else:
				pass

			aProp.triples = self.sparqlHelper.entityTriples(aProp.uri)
			aProp._buildGraph()  # force construction of mini graph

			# attach to an ontology [2015-06-15: no property type distinction yet]
			for uri in aProp.getValuesForProperty(rdflib.RDFS.isDefinedBy):
				onto = self.get_ontology(uri=str(uri))
				if onto:
					onto.all_properties += [aProp]
					aProp.ontology = onto

			self.__buildDomainRanges(aProp)

			# add direct Supers
			directSupers = self.sparqlHelper.getPropDirectSupers(aProp.uri)

			for x in directSupers:
				superprop = self.get_property(uri=x[0])
				# note: extra condition to avoid recursive structures
				if superprop and superprop.uri != aProp.uri:
					aProp._parents.append(superprop)

					# add inverse relationships (= direct subs for superprop)
					if aProp not in superprop.children():
						superprop._children.append(aProp)

		# sort alphabetically
		self.all_properties = sorted(self.all_properties, key=lambda x: x.qname)

		# computer top layer for properties
		# print("calc toplayer")
		exit = []
		for c in self.all_properties:
			if not c.parents():
				exit += [c]
		self.toplayer_properties = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

	def build_skos_concepts(self):
		"""
		2015-08-19: first draft
		"""
		self.all_skos_concepts = []  # @todo: keep adding?

		qres = self.sparqlHelper.getSKOSInstances()
		# print("rdflib query done")

		for candidate in qres:

			test_existing_cl = self.get_skos(uri=candidate[0])
			if not test_existing_cl:
				# create it
				self.all_skos_concepts += [OntoSKOSConcept(candidate[0], None, 
											self.namespaces, 
											None, 
											self.pref_title, 
											self.pref_lang,)
											]
			else:
				pass
		# print("concepts created")
		# add more data
		skos = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')

		for aConcept in self.all_skos_concepts:
			# print("enriching concept...", aConcept)
			aConcept.rdftype = skos['Concept']
			aConcept.triples = self.sparqlHelper.entityTriples(aConcept.uri)
			aConcept._buildGraph()  # force construction of mini graph

			aConcept.sparqlHelper = self.sparqlHelper

			# attach to an ontology
			for uri in aConcept.getValuesForProperty(rdflib.RDFS.isDefinedBy):
				onto = self.get_ontology(uri=str(uri))
				if onto:
					onto.all_skos_concepts += [aConcept]
					aConcept.ontology = onto

			# add direct Supers
			directSupers = self.sparqlHelper.getSKOSDirectSupers(aConcept.uri)

			for x in directSupers:
				superclass = self.get_skos(uri=x[0])
				# note: extra condition to avoid recursive structures
				if superclass and superclass.uri != aConcept.uri:
					aConcept._parents.append(superclass)

					# add inverse relationships (= direct subs for superclass)
					if aConcept not in superclass.children():
						superclass._children.append(aConcept)

		# sort alphabetically
		self.all_skos_concepts = sorted(self.all_skos_concepts, key=lambda x: x.qname)

		# compute top layer for skos
		exit = []
		for c in self.all_skos_concepts:
			if not c.parents():
				exit += [c]
		self.toplayer_skos = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

	def build_shapes(self):
		"""
		Extract SHACL data shapes from the rdf graph.
		<http://www.w3.org/ns/shacl#>

		Instatiate the Shape Python objects and relate it to existing classes,
		if available.
		"""
		self.all_shapes = []  # @todo: keep adding?

		qres = self.sparqlHelper.getShapes()

		for candidate in qres:

			test_existing_cl = self.get_any_entity(uri=candidate[0])
			if not test_existing_cl:
				# create it
				self.all_shapes += [OntoShape(candidate[0], None, 
									self.namespaces, 
									None, 
									self.pref_title, 
									self.pref_lang,)
									]
			else:
				pass

		# add more data
		shacl = rdflib.Namespace('http://www.w3.org/ns/shacl#')

		for aShape in self.all_shapes:

			aShape.rdftype = shacl['Shape']
			aShape.triples = self.sparqlHelper.entityTriples(aShape.uri)
			aShape._buildGraph()  # force construction of mini graph

			aShape.sparqlHelper = self.sparqlHelper

			# attach to a class
			for uri in aShape.getValuesForProperty(shacl['targetClass']):
				aclass = self.get_class(str(uri))
				if aclass:
					aShape.targetClasses += [aclass]
					aclass.all_shapes += [aShape]
					for propertyUri in aShape.getValuesForProperty(shacl['path']): #add shaped properties of this class. later can be used for ontodocs
						propType = self.get_property(str(propertyUri))
						if propType:
							aclass.shapedProperties += [{'shape': aShape, 'property': propType}]



		# sort alphabetically
		self.all_shapes = sorted(self.all_shapes, key=lambda x: x.qname)

		# compute top layer
		exit = []
		for c in self.all_shapes:
			if not c.parents():
				exit += [c]
		self.toplayer_shapes = exit  # sorted(exit, key=lambda x: x.id) # doesnt work


	def build_individuals(self):
		"""
		By default, only add individuals of classes that have been previously extracted.
		"""
		self.all_individuals = []  

		for c in self.all_classes:
			c._instances = []
			qres = self.sparqlHelper.getClassInstances(c.uri)
            
			for uri in [x[0] for x in qres]:

				test_existing_indiv = self.get_individual(uri=uri)

				if not test_existing_indiv:
					instance = RdfEntity(uri, c.uri, c.namespaces)
					instance.triples = self.sparqlHelper.entityTriples(
						instance.uri)
					instance._buildGraph()  # force construction of mini graph
				else:
					instance = test_existing_indiv
				
				c._instances += [instance]
				instance._instance_of += [c]

				if not test_existing_indiv:
					self.all_individuals += [instance]

		# sort alphabetically
		self.all_individuals = sorted(self.all_individuals, key=lambda x: x.qname)


	def build_entity_from_uri(self, uri, ontospyClass=None):
		"""
		Extract RDF statements having a URI as subject, then instantiate the RdfEntity Python object so that it can be queried further.

		Passing <ontospyClass> allows to instantiate a user-defined RdfEntity subclass.

		NOTE: the entity is not attached to any index. In future version we may create an index for these (individuals?) keeping into account that any existing model entity could be (re)created this way.
		"""
		if not ontospyClass:
			ontospyClass = RdfEntity
		elif not issubclass(ontospyClass, RdfEntity):
			printDebug("Error: <%s> is not a subclass of ontospy.RdfEntity" % str(ontospyClass))
			return None
		else:
			pass
		qres = self.sparqlHelper.entityTriples(uri)
		if qres:
			entity = ontospyClass(rdflib.URIRef(uri), 
							None, 
							self.namespaces, 
							None, 
							self.pref_title, 
							self.pref_lang,)
			entity.triples = qres
			entity._buildGraph()  # force construction of mini graph
			# try to add class info
			test = entity.getValuesForProperty(rdflib.RDF.type)
			if test:
				entity.rdftype = test
				entity.rdftype_qname = [entity._build_qname(x) for x in test]
			return entity
		else:
			return None

	# ------------
	# === methods to refine the ontology structure  === #
	# ------------

	def __buildDomainRanges(self, aProp):
		"""
		extract domain/range details and add to Python objects
		"""

		domains = chain(aProp.rdflib_graph.objects(
			None, rdflib.term.URIRef(u'http://schema.org/domainIncludes')), aProp.rdflib_graph.objects(
			None, rdflib.RDFS.domain))

		ranges = chain(aProp.rdflib_graph.objects(
			None, rdflib.term.URIRef(u'http://schema.org/rangeIncludes')), aProp.rdflib_graph.objects(
			None, rdflib.RDFS.range))

		for x in domains:
			if isBlankNode(x):
				aProp.domains += [RdfEntity(x, None, self.namespaces, is_Bnode=True)]
			else:
				aClass = self.get_class(uri=str(x))
				if aClass:
					aProp.domains += [aClass]
					aClass.domain_of += [aProp]
				else:
					# edge case: it's not an OntoClass instance
					aProp.domains += [OntoClass(x, None, 
										self.namespaces, 
										True,  # ext_model arg
										self.pref_title, 
										self.pref_lang,)]

		for x in ranges:
			if isBlankNode(x):
				aProp.domains += [RdfEntity(x, None, self.namespaces, is_Bnode=True)]
			else:
				aClass = self.get_class(uri=str(x))
				if aClass:
					aProp.ranges += [aClass]
					aClass.range_of += [aProp]
				else:
					# eg a DataType property has xsd:STRING
					# here we're storing an ontospy entities but not adding it to
					# the main index
					aProp.ranges += [OntoClass(x, None, 
									self.namespaces, 
									True, 
									self.pref_title,
									self.pref_lang,)]

	def __computeTopLayer(self):
		"""
		deprecated: now this is calculated when entities get extracted
		"""

		exit = []
		for c in self.all_classes:
			if not c.parents():
				exit += [c]
		self.toplayer_classes = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

		# properties
		exit = []
		for c in self.all_properties:
			if not c.parents():
				exit += [c]
		self.toplayer_properties = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

		# skos
		exit = []
		for c in self.all_skos_concepts:
			if not c.parents():
				exit += [c]
		self.toplayer_skos = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

	def __computeInferredProperties(self):
		"""

		:return: attach a list of dicts to each class, detailing valid props up the subsumption tree
		"""
		exit = []
		for c in self.all_classes:
			c.domain_of_inferred = self.getInferredPropertiesForClass(c, "domain_of")
			c.range_of_inferred = self.getInferredPropertiesForClass(c, "range_of")

	def getInferredPropertiesForClass(self, aClass, rel="domain_of"):
		"""
		returns all properties valid for a class (as they have it in their domain)
		recursively ie traveling up the descendants tree
		Note: results in a list of dicts including itself
		Note [2]: all properties with no domain info are added at the top as [None, props]

		:return:
		[{<Class *http://xmlns.com/foaf/0.1/Person*>:
			[<Property *http://xmlns.com/foaf/0.1/currentProject*>,<Property *http://xmlns.com/foaf/0.1/familyName*>,
				etc....]},
		{<Class *http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing*>:
			[<Property *http://xmlns.com/foaf/0.1/based_near*>, etc...]},
			]
		"""
		_list = []

		if rel == "domain_of":
			_list.append({aClass: aClass.domain_of})
			for x in aClass.ancestors():
				if x.domain_of:
					_list.append({x: x.domain_of})

			# add properties from Owl:Thing ie the inference layer

			topLevelProps = [p for p in self.all_properties if p.domains == []]
			if topLevelProps:
				_list.append({self.OWLTHING: topLevelProps})

		elif rel == "range_of":
			_list.append({aClass: aClass.range_of})
			for x in aClass.ancestors():
				if x.domain_of:
					_list.append({x: x.range_of})

			# add properties from Owl:Thing ie the inference layer

			topLevelProps = [p for p in self.all_properties if p.ranges == []]
			if topLevelProps:
				_list.append({self.OWLTHING: topLevelProps})

		return _list



	# ===============
	# methods for retrieving objects
	# ================

	def get_class(self, id=None, uri=None, match=None):
		"""
		get the saved-class with given ID or via other methods...

		Note: it tries to guess what is being passed..

		In [1]: g.get_class(uri='http://www.w3.org/2000/01/rdf-schema#Resource')
		Out[1]: <Class *http://www.w3.org/2000/01/rdf-schema#Resource*>

		In [2]: g.get_class(10)
		Out[2]: <Class *http://purl.org/ontology/bibo/AcademicArticle*>

		In [3]: g.get_class(match="person")
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
			if not is_http(uri):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match:  # qname
				for x in self.all_classes:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.all_classes:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.all_classes:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None

	def get_property(self, id=None, uri=None, match=None):
		"""
		get the saved-class with given ID or via other methods...

		Note: analogous to getClass method
		"""

		if not id and not uri and not match:
			return None

		if type(id) == type("string"):
			uri = id
			id = None
			if not is_http(uri):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match:  # qname
				for x in self.all_properties:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.all_properties:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.all_properties:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None

	def get_individual(self, id=None, uri=None, match=None):
		"""
		get the saved-individual with given ID or via other methods...

		Note: analogous to getClass method
		"""

		if not id and not uri and not match:
			return None

		if type(id) == type("string"):
			uri = id
			id = None
			if not is_http(uri):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match:  # qname
				for x in self.all_individuals:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.all_individuals:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.all_individuals:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None


	def get_skos(self, id=None, uri=None, match=None):
		"""
		get the saved skos concept with given ID or via other methods...

		Note: it tries to guess what is being passed as above
		"""

		if not id and not uri and not match:
			return None

		if type(id) == type("string"):
			uri = id
			id = None
			if not is_http(uri):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match:  # qname
				for x in self.all_skos_concepts:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.all_skos_concepts:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.all_skos_concepts:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None

	def get_any_entity(self, id=None, uri=None, match=None):
		"""
		get a generic entity with given ID or via other methods...
		"""

		if not id and not uri and not match:
			return None

		if type(id) == type("string"):
			uri = id
			id = None
			if not is_http(uri):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			if ":" in match:  # qname
				for x in self.all_classes:
					if match.lower() in x.qname.lower():
						res += [x]
				for x in self.all_properties:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in self.all_classes:
					if match.lower() in x.uri.lower():
						res += [x]
				for x in self.all_properties:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in self.all_classes:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			for x in self.all_properties:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None

	def get_ontology(self, id=None, uri=None, match=None):
		"""
		get the saved-ontology with given ID or via other methods...
		"""

		if not id and not uri and not match:
			return None

		if type(id) == type("string"):
			uri = id
			id = None
			if not is_http(uri):
				match = uri
				uri = None
		if match:
			if type(match) != type("string"):
				return []
			res = []
			for x in self.all_ontologies:
				if match.lower() in x.uri.lower():
					res += [x]
			return res
		else:
			for x in self.all_ontologies:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None

	def nextClass(self, classuri):
		"""Returns the next class in the list of classes. If it's the last one, returns the first one."""
		if classuri == self.all_classes[-1].uri:
			return self.all_classes[0]
		flag = False
		for x in self.all_classes:
			if flag == True:
				return x
			if x.uri == classuri:
				flag = True
		return None

	def nextProperty(self, propuri):
		"""Returns the next property in the list of properties. If it's the last one, returns the first one."""
		if propuri == self.all_properties[-1].uri:
			return self.all_properties[0]
		flag = False
		for x in self.all_properties:
			if flag == True:
				return x
			if x.uri == propuri:
				flag = True
		return None

	def nextConcept(self, concepturi):
		"""Returns the next skos concept in the list of concepts. If it's the last one, returns the first one."""
		if concepturi == self.all_skos_concepts[-1].uri:
			return self.all_skos_concepts[0]
		flag = False
		for x in self.all_skos_concepts:
			if flag == True:
				return x
			if x.uri == concepturi:
				flag = True
		return None

	def ontologyClassTree(self):
		"""
		Returns a dict representing the ontology tree
		Top level = {0:[top classes]}
		Multi inheritance is represented explicitly
		"""
		treedict = {}
		if self.all_classes:
			treedict[0] = self.toplayer_classes
			for element in self.all_classes:
				if element.children():
					treedict[element] = element.children()
			return treedict
		return treedict

	def ontologyPropTree(self):
		"""
		Returns a dict representing the ontology tree
		Top level = {0:[top properties]}
		Multi inheritance is represented explicitly
		"""
		treedict = {}
		if self.all_properties:
			treedict[0] = self.toplayer_properties
			for element in self.all_properties:
				if element.children():
					treedict[element] = element.children()
			return treedict
		return treedict

	def ontologyConceptTree(self):
		"""
		Returns a dict representing the skos tree
		Top level = {0:[top concepts]}
		Multi inheritance is represented explicitly
		"""
		treedict = {}
		if self.all_skos_concepts:
			treedict[0] = self.toplayer_skos
			for element in self.all_skos_concepts:
				if element.children():
					treedict[element] = element.children()
			return treedict
		return treedict

	def ontologyShapeTree(self):
		"""
		Returns a dict representing the shapes tree
		Top level = {0:[top properties]}
		Multi inheritance is represented explicitly
		"""
		treedict = {}
		if self.all_shapes:
			treedict[0] = self.toplayer_shapes
			for element in self.all_shapes:
				if element.children():
					treedict[element] = element.children()
			return treedict
		return treedict


	def ontologyIndividualsTree(self):
		"""
		Returns a dict representing the individuals
		Top level = {0:[all individuals]}
		NOTE individuals have no inherent hierarchy, this method was added 
		so to be more consistent with the similar methods for classes etc..
		"""
		treedict = {}
		if self.all_individuals:
			treedict[0] = self.all_individuals
			return treedict
		return treedict


	# ------------
	# === utils === #
	# ------------


	def rdf_source(self, format="turtle"):
		"""
		Wrapper for rdflib serializer method.
		Valid options are: xml, n3, turtle, nt, pretty-xml, json-ld [trix not working out of the box]
		"""
		s = self.rdflib_graph.serialize(format=format)
		if isinstance(s, bytes):
			s = s.decode('utf-8')
		return s


	def serialize(self, format="turtle"):
		"for backward compatibility"
		return self.rdf_source(format)

	def query(self, stringa):
		"""SPARQL query / wrapper for rdflib sparql query method """
		qres = self.rdflib_graph.query(stringa)
		return list(qres)
	def sparql(self, stringa):
		"SPARQL query / replacement for query"
		return self.query(stringa)

	def stats(self):
		""" shotcut to pull out useful info for a graph"""
		out = []
		out += [("Ontologies", len(self.all_ontologies))]
		out += [("Triples", self.triplesCount())]
		out += [("Classes", len(self.all_classes))]
		out += [("Properties", len(self.all_properties))]
		out += [("Annotation Properties", len(self.all_properties_annotation))]
		out += [("Object Properties", len(self.all_properties_object))]
		out += [("Datatype Properties", len(self.all_properties_datatype))]
		out += [("Skos Concepts", len(self.all_skos_concepts))]
		out += [("Data Shapes", len(self.all_shapes))]
		if not self.hide_individuals:
			out += [("Individuals", len(self.all_individuals))]
		out += [("Data Sources", len(self.sources))]
		return out

	def triplesCount(self):
		"""

		2016-08-18 the try/except is a dirty solution to a problem
		emerging with counting graph length on cached Graph objects..
		"""
		# @todo  investigate what's going on..
		# printDebug(unicode(type(self.rdflib_graph)), fg="red")
		try:
			return len(self.rdflib_graph)
		except:
			printDebug("Ontospy: error counting graph length..", fg="red")
			return 0


	def printClassTree(self, element=None, showids=False, labels=False, showtype=False):
		"""
		Print nicely into stdout the class tree of an ontology

		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		TYPE_MARGIN = 11  # length for owl:class etc..

		if not element:  # first time
			for x in self.toplayer_classes:
				printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

		else:
			printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)

	def printPropertyTree(self, element=None, showids=False, labels=False, showtype=False):
		"""
		Print nicely into stdout the property tree of an ontology

		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		TYPE_MARGIN = 18  # length for owl:AnnotationProperty etc..

		if not element:  # first time
			for x in self.toplayer_properties:
				printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

		else:
			printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)

	def printSkosTree(self, element=None, showids=False, labels=False, showtype=False):
		"""
		Print nicely into stdout the SKOS tree of an ontology

		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		TYPE_MARGIN = 13  # length for skos:concept

		if not element:  # first time
			for x in self.toplayer_skos:
				printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

		else:
			printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)
