# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.
"""

from itertools import chain
import json
import re
import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLStore

from .utils import *
from .rdf_loader import RDFLoader
from .entities import *
from .sparql_helper import SparqlHelper
from .shacl_helper import build_shacl_constraints

# a PREFIX declaration in a sparql query, eg `PREFIX owl: <http://www.w3.org/2002/07/owl#>`
PREFIX_DECLARATION = re.compile(r"PREFIX\s+([\w.-]*)\s*:\s*<([^>]*)>", re.IGNORECASE)

def _remove_redundant_children(children):
	"""
	Leave out the children that are also descendants of another child, eg in a reasoned
	graph with A > B > C and the materialised A > C, C is left out under A (PR #87).
	Multiple inheritance is kept: C still appears under B, and under any other parent.
	Children that are descendants of each other (a cycle) are all kept.
	"""
	if len(children) < 2:
		return children
	descendants = {c: set(c.descendants()) for c in children}
	return [c for c in children
			if not any(c in descendants[s] and s not in descendants[c]
						for s in children if s is not c)]


class Ontospy(object):
	"""
	Object that extracts schema definitions (aka 'ontologies') from an rdf graph.

	Load some RDF, and Ontospy extracts the ontologies, classes, properties, SKOS concepts,
	SHACL shapes and (optionally) individuals it defines, as Python objects:

	In [1]: import ontospy

	In [2]: o = ontospy.Ontospy("foaf.rdf")

	In [3]: o.stats()
	Out[3]:
	[('Ontologies', 1),
	 ('Triples', 630),
	 ('Classes', 16),
	 ('Properties', 67),
	 ('Annotation Properties', 7),
	 ('Object Properties', 34),
	 ('Datatype Properties', 26),
	 ('Skos Concepts', 0),
	 ('Data Shapes', 0),
	 ('Data Sources', 1)]

	In [4]: o.all_classes[:2]
	Out[4]:
	[<Class *http://xmlns.com/foaf/0.1/Agent*>,
	 <Class *http://xmlns.com/foaf/0.1/Document*>]

	The extracted entities are in the `all_*` attributes (`all_ontologies`, `all_classes`,
	`all_properties`, `all_skos_concepts`, `all_shapes`, `all_individuals`), and can be
	looked up with `get_class()`, `get_property()` etc. The underlying rdflib graph is
	`rdflib_graph`, and `query()` runs SPARQL on it.

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
				 graph_obj=None,
				 ):
		"""Load the graph in memory, then setup all necessary attributes.

		RDF can come from files or URLs (`uri_or_path`), strings (`data`), open files
		(`file_obj`), existing rdflib graphs (`graph_obj`), or a mix of these: everything
		is loaded into a single graph. Alternatively, `sparql_endpoint` connects to a remote
		endpoint instead of loading anything in memory.

		Parameters
		----------
		uri_or_path : str or list of str, optional
			A local file path, a folder (all the RDF files in it are loaded), or a URL.
			A list loads all of them into one graph. By default None
		data : str or list of str, optional
			A string (or list of strings) containing RDF, eg Turtle. By default None
		file_obj : file object or list of file objects, optional
			An open file (text or binary mode) containing RDF. By default None
		rdf_format : str, optional
			The RDF serialization of the sources: "turtle", "xml", "n3", "nt", "json-ld"
			or "rdfa". By default "", which tries each of them in turn, starting from the
			most likely one given the file extension.
		verbose : bool, optional
			Print out what is being loaded and extracted. By default False
		hide_base_schemas : bool, optional
			Leave out the classes and properties of the RDF, RDFS, OWL and XML Schema
			vocabularies themselves (eg rdfs:Resource), so that only the ontology's own
			entities are listed. By default True
		hide_implicit_types : bool, optional
			Leave out classes that are only used as the type of something (`?x rdf:type ?c`)
			but never declared as classes or used in subClassOf, domain or range statements.
			By default True
		hide_implicit_preds : bool, optional
			Leave out properties that are only used in triples, without being declared as
			properties. By default True
		hide_individuals : bool, optional
			Don't extract individuals, ie instances of the classes. Set it to False to get
			them in `all_individuals`. By default True
		sparql_endpoint : str, optional
			The URL of a SPARQL endpoint to query, instead of loading RDF in memory. Only
			used if no other source is given. Entities aren't extracted automatically for
			endpoints, as that can mean many slow queries: call `build_all()`, or eg
			`build_ontologies()`, when needed. By default None
		credentials : tuple, optional
			A (user, password) tuple, for SPARQL endpoints that need authentication.
			By default None
		build_all : bool, optional
			Extract the ontologies, classes, properties etc. as soon as the RDF is loaded.
			Set it to False to only load the graph, then call `build_all()` later.
			By default True
		pref_title : str, optional
			How entities are named by default, eg in their `title` and in generated
			documentation: "qname" for their prefixed name, eg foaf:Person (default), or
			"label" for their rdfs:label.
		pref_lang : str, optional
			The preferred language for labels and descriptions, when an entity has them
			in several languages. By default "en"
		graph_obj : rdflib.Graph or list of rdflib.Graph, optional
			An existing rdflib graph (or several) to load. The graphs passed are not
			modified, and their prefix bindings are kept. By default None
		"""
		
		super(Ontospy, self).__init__()

		self.verbose = verbose
		self.rdflib_graph = None
		self.sparql_endpoint = None
		self.credentials = None  # tuple: auth credentials for endpoint if needed
		self.sources = None
		self.sparqlHelper = None
		self.pref_title = pref_title
		self.pref_lang = pref_lang
		self.hide_individuals = hide_individuals
		self.namespaces = []
		self._namespaces_kept = None  # see _namespaces_in_use
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
		if uri_or_path or data or file_obj or graph_obj is not None:
			self.load_rdf(uri_or_path, data, file_obj, rdf_format, verbose, graph_obj)
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
				 verbose=False,
				 graph_obj=None):
		"""Load RDF sources into an ontospy/rdflib graph. See `__init__` for the parameters."""
		loader = RDFLoader(verbose=verbose)
		loader.load(uri_or_path, data, file_obj, rdf_format, graph_obj=graph_obj)
		self.rdflib_graph = loader.rdflib_graph
		self.sources = loader.sources_valid
		self.sparqlHelper = SparqlHelper(self.rdflib_graph)
		self._namespaces_kept = self._namespaces_in_use(loader.declared_prefixes)
		self.namespaces = self._filter_namespaces()

	def _namespaces_in_use(self, declared_prefixes):
		"""
		The namespaces worth listing in <self.namespaces> (#14): since rdflib 7 every graph
		comes with ~30 well-known prefixes bound (brick, csvw, dcat, odrl, sosa...), whether
		the RDF uses them or not. Keeps the namespaces that a URI in the graph starts with
		(subjects, predicates, objects, literal datatypes), the ones the sources declare, and
		rdf/rdfs/owl/xsd, which Ontospy uses itself (eg owl:Thing). Dropping the others can't
		change any qname: they don't match any URI in the graph.
		"""
		uris = set()
		for triple in self.rdflib_graph:
			for x in triple:
				if isinstance(x, rdflib.URIRef):
					uris.add(str(x))
			if isinstance(triple[2], rdflib.Literal) and triple[2].datatype:
				uris.add(str(triple[2].datatype))
		keep = {str(rdflib.RDF), str(rdflib.RDFS), str(rdflib.OWL), str(rdflib.XSD)}
		# the sources are parsed with rdflib's core prefixes bound, so `xml` always looks
		# declared: like the other defaults, keep it only if used
		keep |= {str(ns) for ns in declared_prefixes.values()} - {"http://www.w3.org/XML/1998/namespace"}
		for _, ns in self.rdflib_graph.namespaces():
			ns = str(ns)
			if ns and ns not in keep and any(u.startswith(ns) for u in uris):
				keep.add(ns)
		return keep

	def _filter_namespaces(self):
		"""the graph's prefix bindings, limited to the namespaces in <self._namespaces_kept>.

		None is for SPARQL endpoints: there's no graph in memory to check, so rdflib's
		well-known prefixes are listed too, as before, for readable qnames. They're not bound
		on the endpoint graph itself, which has only the prefixes its queries need (#14).
		"""
		bindings = list(self.rdflib_graph.namespaces())
		if self._namespaces_kept is None:
			listed = {p: ns for p, ns in rdflib.Graph().namespaces()}
			bound_ns = {str(ns) for _, ns in bindings}
			listed = {p: ns for p, ns in listed.items() if str(ns) not in bound_ns}
			listed.update(dict(bindings))  # the graph's own bindings win
			return sorted(listed.items())
		return sorted((prefix, ns) for prefix, ns in bindings if str(ns) in self._namespaces_kept)


	def load_sparql(self,
					sparql_endpoint,
					verbose=False,
					credentials=None):
		"""
		Set up an ontospy graph using a sparql endpoint. 

		Note this is using SPARQLStore backend as a virtual ontospy graph. 
		See 
		- https://github.com/RDFLib/rdflib/blob/main/examples/sparqlstore_example.py 
		- https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.plugins.stores.html#rdflib.plugins.stores.sparqlstore.SPARQLStore

		Note: results are requested as JSON. With rdflib's default Accept header (sparql-results+xml
		or rdf+xml) some endpoints eg Virtuoso/DBpedia reply with rdf+xml, which rdflib then
		fails to parse as query results ("Repeat node-elements inside property elements").

		"""
		try:
			if credentials and type(credentials) == tuple:
				store = SPARQLStore(sparql_endpoint, auth=credentials, returnFormat="json")
			else:
				store = SPARQLStore(sparql_endpoint, returnFormat="json")

			# only rdflib's core prefixes on the store: SPARQLStore prepends every prefix
			# bound there to each query it sends, and rdflib's ~30 defaults were mostly
			# unused (#14). Ontospy's own queries add theirs (see SparqlHelper), user queries
			# get the ones they use (see query)
			graph = rdflib.Graph(store, bind_namespaces="core")

			self.rdflib_graph = graph
			self.sparql_endpoint = sparql_endpoint
			self.sources = [sparql_endpoint]
			self.sparqlHelper = SparqlHelper(self.rdflib_graph, self.sparql_endpoint)
			self._namespaces_kept = None  # all of them, see _filter_namespaces
			self.namespaces = self._filter_namespaces()
		except:
			printDebug("Error trying to connect to Endpoint.")
			raise
		# don't extract entities by default..

	def add_namespace(self, ns_prefix, ns_url):
		"""Add a new namespace to the ontospy graph, replacing any existing binding for the same prefix

		eg o.add_namespace("schema", "http://schema.org/")
		"""
		self.rdflib_graph.bind(ns_prefix, ns_url, override=True, replace=True)
		if self._namespaces_kept is not None:
			self._namespaces_kept.add(str(ns_url))
		self.namespaces = self._filter_namespaces()


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

		self.__makeSlugsUnique()

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
		if self.verbose:
			printDebug(".. building ontologies")

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
		qres += self.sparqlHelper.getPropertiesTypedBySubclasses()
		# print("rdflib query done")

		# one row per (property, type): collect all the types first, so that the main
		# type doesn't depend on which row comes first (#10)
		candidate_types = {}
		for candidate in qres:
			types = candidate_types.setdefault(candidate[0], [])
			if candidate[1] and candidate[1] not in types:
				types.append(candidate[1])

		for uri, types in candidate_types.items():
			self.all_properties += [OntoProperty(uri, mainPropertyType(types),
										self.namespaces,
										False,
										self.pref_title,
										self.pref_lang,
										)]
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
			# all the rdf:types, for display (#53)
			aProp.rdftypes_qnames = sorted(aProp._build_qname(x)
				for x in aProp.getValuesForProperty(rdflib.RDF.type))

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

		self.__buildInferredDomainRanges()

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
		self.all_shapes = [] 

		qres = self.sparqlHelper.getShapes()

		for candidate in qres:

			test_existing_cl = self.get_shapes(uri=candidate[0])
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

					#add shaped properties of this class. later can be used for ontodocs
					for propertyUri in aShape.getValuesForProperty(shacl['path']): 
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
		self.toplayer_shapes = exit 

		# compute SHACL property constraints once classes and shapes have been built
		shacl_constraints = build_shacl_constraints(self)
		for onto_class in self.all_classes:
			onto_class.shacl_constraints = shacl_constraints.get(onto_class, [])


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
				aProp.ranges += [RdfEntity(x, None, self.namespaces, is_Bnode=True)]
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

	def __buildInferredDomainRanges(self):
		"""
		2026-10-12: properties with no rdfs:domain (or rdfs:range) of their own inherit
		the ones of their superproperties, all the way up (#126). As in RDFS, all of them
		apply. They are kept apart from the declared ones, in <domains_inferred> and
		<ranges_inferred>; classes list these properties in <domain_of_via_superproperties>
		and <range_of_via_superproperties>.
		"""
		for aProp in self.all_properties:
			if not aProp.domains:
				for superprop in aProp.ancestors():
					for x in superprop.domains:
						if x.uri not in [y.uri for y in aProp.domains_inferred]:
							aProp.domains_inferred.append(x)
							if hasattr(x, "domain_of_via_superproperties"):  # not a blank node
								x.domain_of_via_superproperties.append(aProp)
			if not aProp.ranges:
				for superprop in aProp.ancestors():
					for x in superprop.ranges:
						if x.uri not in [y.uri for y in aProp.ranges_inferred]:
							aProp.ranges_inferred.append(x)
							if hasattr(x, "range_of_via_superproperties"):  # not a blank node
								x.range_of_via_superproperties.append(aProp)

	def __makeSlugsUnique(self):
		"""
		Slugs name the documentation pages and are lowercase, so URIs that differ only by
		case (eg FOAF's givenName and givenname) would get the same page. The first entity
		(in qname order) keeps its slug, the others get -2, -3 etc.
		"""
		seen = set()
		for entities in [self.all_ontologies, self.all_classes, self.all_properties,
						 self.all_skos_concepts, self.all_shapes, self.all_individuals]:
			for x in entities:
				slug, n = x.slug, 1
				while slug in seen:
					n += 1
					slug = "%s-%d" % (x.slug, n)
				x.slug = slug
				seen.add(slug)

	def __computeInferredProperties(self):
		"""

		:return: attach a list of dicts to each class, detailing valid props up the subsumption tree
		"""
		# the same for every class: compute once, not once per class (#142)
		top_level = {rel: self._topLevelProperties(rel) for rel in ("domain_of", "range_of")}
		for c in self.all_classes:
			c.domain_of_inferred = self.getInferredPropertiesForClass(c, "domain_of", top_level["domain_of"])
			c.range_of_inferred = self.getInferredPropertiesForClass(c, "range_of", top_level["range_of"])

	def _topLevelProperties(self, rel="domain_of"):
		"""
		properties with no domain (or range) info, which apply to owl:Thing.
		Properties that apply to a class via a SHACL PropertyShape are not top-level.
		"""
		if rel == "domain_of":
			properties_applicable_by_shapes = {x[0] for x in self.sparqlHelper.getPropsApplicableByShapes()}
			return [p for p in self.all_properties if p.domains == [] and p.domains_inferred == []
						and not p.uri in properties_applicable_by_shapes]
		elif rel == "range_of":
			return [p for p in self.all_properties if p.ranges == [] and p.ranges_inferred == []]
		return []

	def getInferredPropertiesForClass(self, aClass, rel="domain_of", topLevelProps=None):
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
			for x in [aClass] + aClass.ancestors():
				props = x.domain_of + x.domain_of_via_superproperties
				if props or x is aClass:
					_list.append({x: props})

			# add properties from Owl:Thing ie the inference layer
			if topLevelProps is None:
				topLevelProps = self._topLevelProperties(rel)
			if topLevelProps:
				_list.append({self.OWLTHING: topLevelProps})

		elif rel == "range_of":
			for x in [aClass] + aClass.ancestors():
				props = x.range_of + x.range_of_via_superproperties
				if props or x is aClass:
					_list.append({x: props})

			# add properties from Owl:Thing ie the inference layer
			if topLevelProps is None:
				topLevelProps = self._topLevelProperties(rel)
			if topLevelProps:
				_list.append({self.OWLTHING: topLevelProps})

		return _list



	# ===============
	# methods for retrieving objects
	# ================

	def _get_defined_entity(self, id=None, uri=None, match=None, candidates_list=None):
		"""Inner method to help matching uris or strings to entities that have been added 
		to Ontospy. 

		candidates_list
			A list of entities, eg self.all_classes, self.all_properties, self.all_skos_concepts
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
				for x in candidates_list:
					if match.lower() in x.qname.lower():
						res += [x]
			else:
				for x in candidates_list:
					if match.lower() in x.uri.lower():
						res += [x]
			return res
		else:
			for x in candidates_list:
				if id and x.id == id:
					return x
				if uri and x.uri.lower() == uri.lower():
					return x
			return None

	def get_class(self, id=None, uri=None, match=None):
		"""
		Get the saved-class with given ID or via other methods...

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

		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=self.all_classes)


	def get_property(self, id=None, uri=None, match=None):
		"""Get the saved-property with given ID or via other methods...
		"""
		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=self.all_properties)


	def get_individual(self, id=None, uri=None, match=None):
		"""Get the saved-individual with given ID or via other methods...
		"""
		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=self.all_individuals)


	def get_skos(self, id=None, uri=None, match=None):
		"""Get the saved skos concept with given ID or via other methods...
		"""
		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=self.all_skos_concepts)

	def get_shapes(self, id=None, uri=None, match=None):
		"""Get the saved shacl shapes with given ID or via other methods...
		"""
		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=self.all_shapes)

	def get_ontology(self, id=None, uri=None, match=None):
		"""Get the saved-ontology with given ID or via other methods...
		"""
		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=self.all_ontologies)

	def get_any_entity(self, id=None, uri=None, match=None):
		"""Get any entity-type with given ID or via other methods...
		"""

		all_entities = self.all_classes + self.all_properties + self.all_individuals + self.all_skos_concepts + self.all_shapes + self.all_ontologies

		return self._get_defined_entity(
			id=id, 
			uri=uri, 
			match=match, 
			candidates_list=all_entities)



	# ===============
	# methods for the CLI interface, so that the user can interact with the ontospy object
	# ================

	def _next_entity(self, uri, candidates_list):
		"""Returns the next entity in the list it is contained in. If it's the last one, returns the first one."""
		if uri == candidates_list[-1].uri:
			return candidates_list[0]
		flag = False
		for x in candidates_list:
			if flag == True:
				return x
			if x.uri == uri:
				flag = True
		return None

	def nextClass(self, classuri):
		"""Returns the next class in the list of classes."""
		return self._next_entity(classuri, self.all_classes)

	def nextProperty(self, propuri):
		"""Returns the next property in the list of classes."""
		return self._next_entity(propuri, self.all_properties)

	def nextConcept(self, concepturi):
		"""Returns the next skos concept in the list of concepts."""
		return self._next_entity(concepturi, self.all_skos_concepts)

	def nextShapes(self, shapeuri):
		"""Returns the next shape in the list of shapes."""
		return self._next_entity(shapeuri, self.all_shapes)

	def nextOntology(self, shapeuri):
		"""Returns the next ontology in the list of ontologies."""
		return self._next_entity(shapeuri, self.all_ontologies)


	# ===============
	# methods for building super/sub trees
	# TODO factor out common patterns into a separate helper method
	# ================


	def _tree_helper(self, entities_list, toplayer, non_redundant=False):
		"""Common helper method for building super/sub trees"""
		treedict = {}
		if entities_list:
			treedict[0] = toplayer
			for element in entities_list:
				children = element.children()
				if non_redundant:
					children = _remove_redundant_children(children)
				if children:
					treedict[element] = children
			return treedict
		return treedict


	def ontologyClassTree(self, non_redundant=False):
		"""
		Returns a dict representing the ontology class tree
		Top level = {0:[top classes]}
		Multi inheritance is represented explicitly
		non_redundant: leave out children that are also descendants of another child,
		eg in reasoned graphs where subclass relations are materialised (PR #87)
		"""
		return self._tree_helper(self.all_classes, self.toplayer_classes, non_redundant)

	def ontologyPropTree(self, non_redundant=False):
		"""
		Returns a dict representing the ontology properties tree
		Top level = {0:[top properties]}
		Multi inheritance is represented explicitly
		non_redundant: leave out children that are also descendants of another child,
		eg in reasoned graphs where subclass relations are materialised (PR #87)
		"""
		return self._tree_helper(self.all_properties, self.toplayer_properties, non_redundant)

	def ontologyConceptTree(self, non_redundant=False):
		"""
		Returns a dict representing the skos tree
		Top level = {0:[top concepts]}
		Multi inheritance is represented explicitly
		non_redundant: leave out children that are also descendants of another child,
		eg in reasoned graphs where subclass relations are materialised (PR #87)
		"""
		return self._tree_helper(self.all_skos_concepts, self.toplayer_skos, non_redundant)

	def ontologyShapeTree(self, non_redundant=False):
		"""
		Returns a dict representing the shapes tree
		Top level = {0:[top shapes]}
		Multi inheritance is represented explicitly
		non_redundant: leave out children that are also descendants of another child,
		eg in reasoned graphs where subclass relations are materialised (PR #87)
		"""
		return self._tree_helper(self.all_shapes, self.toplayer_shapes, non_redundant)


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



	def _prefixes_used_in(self, sparql_q):
		"""
		The prefixes from <self.namespaces> that a query uses, eg {"foaf": ...} for
		`?x a foaf:Person`. For SPARQL endpoints: rdflib's SPARQLStore declares the prefixes it
		gets at the top of the query, so a query sends only these plus the graph's own
		bindings, instead of all of rdflib's defaults (#14).
		"""
		used = set(re.findall(r"(?<![\w:/#.-])([A-Za-z][\w.-]*):", sparql_q))
		return {prefix: ns for prefix, ns in self.namespaces if prefix in used}

	def _cleanup_ns_declarations(self, sparql_q):
		"""Removes PREFIX declarations from a sparql query and adds them to the graph namespaces.

		Only needed for SPARQL endpoint graphs: rdflib's SPARQLStore prepends all the graph namespaces
		to the query it sends, so a prefix declared in the query too ends up declared twice, which
		many endpoints reject. See
		https://stackoverflow.com/questions/76677670/sparql-namespace-conflict-while-querying

		Parameters
		----------
		sparql_q : string
			A sparql query
		"""
		new_ns = PREFIX_DECLARATION.findall(sparql_q)
		if not new_ns:
			return sparql_q
		for prefix, uri in new_ns:
			self.add_namespace(prefix, uri)
		if self.verbose:
			printDebug(f"Note: query PREFIX declarations moved to graph namespaces: {new_ns}")
		return PREFIX_DECLARATION.sub("", sparql_q)


	def query(self, stringa, format="list"):
		"""SPARQL query / wrapper for rdflib sparql query method

		format: "list" (default) returns a list of result rows.
		"csv", "json", "txt" and "xml" return the results serialized as a string.
		"df" returns a pandas DataFrame of the bindings' values (requires pandas).

		Note this is different from graph serializations, as query results are normally tabular data.
		TODO handle DESCRIBE and CONSTRUCT queries better
		"""
		VALID_FORMATS = ["csv", "json", "txt", "xml", "list", "df"]
		if format not in VALID_FORMATS:
			printInfo(f"Error: format not in VALID_FORMATS: {VALID_FORMATS}\n using default 'list'", "important")
			format = "list"

		if self.sparql_endpoint:
			stringa = self._cleanup_ns_declarations(stringa)
			qres = self.rdflib_graph.query(stringa, initNs=self._prefixes_used_in(stringa))
		else:
			qres = self.rdflib_graph.query(stringa)

		if format == "list":
			return list(qres)
		elif format == "df":
			try:
				import pandas as pd
			except ImportError:
				printDebug("WARNING - This Beta feature requires pandas - `pip install pandas`")
				raise
			d = json.loads(qres.serialize(format="json"))
			if "boolean" in d:  # ASK query
				return pd.DataFrame([{"boolean": d["boolean"]}])
			columns = d.get("head", {}).get("vars", [])
			rows = [{k: v["value"] for k, v in row.items()}
					for row in d.get("results", {}).get("bindings", [])]
			return pd.DataFrame(rows, columns=columns)
		else:
			out = qres.serialize(format=format)
			return out.decode("utf-8") if isinstance(out, bytes) else out

	def sparql(self, stringa):
		"LEGACY -- SPARQL query / replacement for query"
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

	def printShapesTree(self, element=None, showids=False, labels=False, showtype=False):
		"""
		Print nicely into stdout the SHACL shapes tree of an ontology

		Note: indentation is made so that ids up to 3 digits fit in, plus a space.
		[123]1--
		[1]123--
		[12]12--
		"""
		TYPE_MARGIN = 13  # length for skos:concept

		if not element:  # first time
			for x in self.toplayer_shapes:
				printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

		else:
			printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)
