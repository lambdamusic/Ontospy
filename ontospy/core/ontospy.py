# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c) 2013-2017 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.
"""

from __future__ import print_function

import sys, os, time, optparse

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

import rdflib

from .utils import *
from .rdf_loader import RDFLoader
from .entities import *
from .sparqlHelper import SparqlHelper



class Ontospy(object):
    """
    Object that extracts schema definitions (aka 'ontologies') from an rdf graph.

    In [3]: import ontospy

    In [5]: o = ontospy.Ontospy()

    In [7]: o.load_rdf("foaf.rdf")

    In [11]: o.extract_entities()

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

    def __init__(self, uri_or_path=None, text=None, file_obj=None, rdf_format="", verbose=False, hide_base_schemas=True, sparql_endpoint=None, credentials=None, extract_entities=True):
        """
        Load the graph in memory, then setup all necessary attributes.
        """
        super(Ontospy, self).__init__()

        self.rdfgraph = None
        self.sparql_endpoint = None
        self.credentials = None  # tuple: auth credentials for endpoint if needed
        self.sources = None
        self.sparqlHelper = None
        self.ontologies = []
        self.classes = []
        self.namespaces = []
        self.properties = []
        self.annotationProperties = []
        self.objectProperties = []
        self.datatypeProperties = []
        self.skosConcepts = []
        self.individuals = []
        self.shapes = []
        self.toplayer = []
        self.toplayerProperties = []
        self.toplayerSkosConcepts = []
        self.toplayerShapes = []
        self.OWLTHING = OntoClass(rdflib.OWL.Thing, rdflib.OWL.Class, self.namespaces)

        # finally:
        if uri_or_path or text or file_obj:
            self.load_rdf(uri_or_path, text, file_obj, rdf_format, verbose, hide_base_schemas)
            if extract_entities:
                self.extract_entities(verbose=verbose, hide_base_schemas=hide_base_schemas)
        elif sparql_endpoint: # by default entities are not extracted
            self.load_sparql(sparql_endpoint, verbose, hide_base_schemas, credentials)
        else:
            pass


    def __repr__(self):
        """
        Return some info for the ontospy instance.

        note: if it's a sparql backend, limit the info returned to avoid long queries (tip: a statement like `if self.rdfgraph` on a sparql endpoint is enough to cause a long query!)

        """
        if self.sparql_endpoint and self.rdfgraph != None:
            return "<Ontospy Graph (sparql endpoint = <%s>)>" % self.sparql_endpoint
        elif self.rdfgraph != None:
            return "<Ontospy Graph (%d triples)>" % (len(self.rdfgraph))
        else:
            return "<Ontospy object created but not initialized (use the `load_rdf` method to load an rdf schema)>"


    def load_rdf(self, uri_or_path=None, text=None, file_obj=None, rdf_format="", verbose=False, hide_base_schemas=True):
        """Load an RDF source into an ontospy/rdflib graph"""
        loader = RDFLoader()
        loader.load(uri_or_path, text, file_obj, rdf_format, verbose)
        self.rdfgraph = loader.rdfgraph
        self.sources = loader.sources_valid
        self.sparqlHelper = SparqlHelper(self.rdfgraph)
        self.namespaces = sorted(self.rdfgraph.namespaces())


    def load_sparql(self, sparql_endpoint, verbose=False, hide_base_schemas=True, credentials=None):
        """
        Set up a SPARQLStore backend as a virtual ontospy graph

        Note: we're using a 'SPARQLUpdateStore' backend instead of 'SPARQLStore' cause otherwise authentication fails (https://github.com/RDFLib/rdflib/issues/755)

        """
        try:
            # graph = rdflib.ConjunctiveGraph('SPARQLStore')
            graph = rdflib.ConjunctiveGraph('SPARQLUpdateStore')

            if credentials and type(credentials) == tuple:
                # https://github.com/RDFLib/rdflib/issues/343
                graph.store.setCredentials(credentials[0], credentials[1])
                # graph.store.setHTTPAuth('BASIC') # graph.store.setHTTPAuth('DIGEST')

            graph.open(sparql_endpoint)
            self.rdfgraph = graph
            self.sparql_endpoint = sparql_endpoint
            self.sources = [sparql_endpoint]
            self.sparqlHelper = SparqlHelper(self.rdfgraph, self.sparql_endpoint)
            self.namespaces = sorted(self.rdfgraph.namespaces())
        except:
            printDebug("Error trying to connect to Endpoint.")
            raise
        # don't extract entities by default..


    def serialize(self, format="turtle"):
        """
        Wrapper for rdflib serializer method.
        Valid options are: xml, n3, turtle, nt, pretty-xml [trix not working out of the box]
        """
        return self.rdfgraph.serialize(format=format)


    def query(self, stringa):
        """ wrapper for rdflib sparql query method """
        qres = self.rdfgraph.query(stringa)
        return list(qres)



    # ------------
    # === methods to build python objects === #
    # ------------

    def extract_entities(self, verbose=False, hide_base_schemas=True):
        """
        Extract all ontology entities from an RDF graph and construct Python representations of them.
        """
        if verbose:
            printDebug("Scanning entities...", "green")
            printDebug("----------", "comment")

        self.extract_ontologies()
        if verbose: printDebug("Ontologies.........: %d" % len(self.ontologies), "comment")

        self.extract_classes(hide_base_schemas)
        if verbose: printDebug("Classes............: %d" % len(self.classes), "comment")

        self.extract_properties()
        if verbose: printDebug("Properties.........: %d" % len(self.properties), "comment")
        if verbose: printDebug("..annotation.......: %d" % len(self.annotationProperties), "comment")
        if verbose: printDebug("..datatype.........: %d" % len(self.datatypeProperties), "comment")
        if verbose: printDebug("..object...........: %d" % len(self.objectProperties), "comment")

        self.extract_skos_concepts()
        if verbose: printDebug("Concepts (SKOS)....: %d" % len(self.skosConcepts), "comment")

        self.extract_shapes()
        if verbose: printDebug("Shapes (SHACL).....: %d" % len(self.shapes), "comment")

        # self.__computeTopLayer()

        self.__computeInferredProperties()

        if verbose: printDebug("----------", "comment")


    def extract_ontologies(self, exclude_BNodes = False, return_string=False):
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
                        checkDC_ID = [x for x in self.rdfgraph.objects(candidate[0], rdflib.namespace.DC.identifier)]
                        if checkDC_ID:
                            out += [Ontology(checkDC_ID[0], namespaces=self.namespaces),]
                        else:
                            vannprop = rdflib.URIRef("http://purl.org/vocab/vann/preferredNamespaceUri")
                            vannpref = rdflib.URIRef("http://purl.org/vocab/vann/preferredNamespacePrefix")
                            checkDC_ID = [x for x in self.rdfgraph.objects(candidate[0], vannprop)]
                            if checkDC_ID:
                                checkDC_prefix = [x for x in self.rdfgraph.objects(candidate[0], vannpref)]
                                if checkDC_prefix:
                                    out += [Ontology(checkDC_ID[0],
                                                     namespaces=self.namespaces,
                                                     prefPrefix=checkDC_prefix[0])]
                                else:
                                    out += [Ontology(checkDC_ID[0], namespaces=self.namespaces)]

                else:
                    out += [Ontology(candidate[0], namespaces=self.namespaces)]


        else:
            pass
            # printDebug("No owl:Ontologies found")

        #finally... add all annotations/triples
        self.ontologies = out
        for onto in self.ontologies:
            onto.triples = self.sparqlHelper.entityTriples(onto.uri)
            onto._buildGraph() # force construction of mini graph



    #
    #  RDFS:class vs OWL:class cf. http://www.w3.org/TR/owl-ref/ section 3.1
    #

    def extract_classes(self, hide_base_schemas=True):
        """
        2015-06-04: removed sparql 1.1 queries
        2015-05-25: optimized via sparql queries in order to remove BNodes
        2015-05-09: new attempt

        Note: sparqlHelper.getAllClasses() returns a list of tuples,
        (class, classRDFtype)
        so in some cases there are duplicates if a class is both RDFS.CLass and OWL.Class
        In this case we keep only OWL.Class as it is more informative.
        """


        self.classes = [] # @todo: keep adding?

        qres = self.sparqlHelper.getAllClasses(hide_base_schemas=hide_base_schemas)

        for class_tuple in qres:

            _uri = class_tuple[0]
            try:
                _type = class_tuple[1]
            except:
                _type= ""

            test_existing_cl = self.getClass(uri=_uri)
            if not test_existing_cl:
                # create it
                ontoclass = OntoClass(_uri, _type, self.namespaces)
                self.classes += [ontoclass]
            else:
                # if OWL.Class over RDFS.Class - update it
                if _type == rdflib.OWL.Class:
                    test_existing_cl.rdftype = rdflib.OWL.Class

        #add more data
        for aClass in self.classes:

            aClass.triples = self.sparqlHelper.entityTriples(aClass.uri)
            aClass._buildGraph() # force construction of mini graph

            aClass.sparqlHelper = self.sparqlHelper

            # attach to an ontology
            for uri in aClass.getValuesForProperty(rdflib.RDFS.isDefinedBy):
                onto = self.getOntology(str(uri))
                if onto:
                    onto.classes += [aClass]
                    aClass.ontology = onto

            # add direct Supers
            directSupers = self.sparqlHelper.getClassDirectSupers(aClass.uri)

            for x in directSupers:
                superclass = self.getClass(uri=x[0])
                # note: extra condition to avoid recursive structures
                if superclass and superclass.uri != aClass.uri:
                    aClass._parents.append(superclass)

                    # add inverse relationships (= direct subs for superclass)
                    if aClass not in superclass.children():
                         superclass._children.append(aClass)

        # sort alphabetically
        self.classes = sorted(self.classes, key=lambda x: x.qname)

        # compute top layer
        exit = []
        for c in self.classes:
            if not c.parents():
                exit += [c]
        self.toplayer = exit  # sorted(exit, key=lambda x: x.id) # doesnt work




    def extract_properties(self):
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

        qres = self.sparqlHelper.getAllProperties()

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

            aProp.triples = self.sparqlHelper.entityTriples(aProp.uri)
            aProp._buildGraph() # force construction of mini graph

            # attach to an ontology [2015-06-15: no property type distinction yet]
            for uri in aProp.getValuesForProperty(rdflib.RDFS.isDefinedBy):
                onto = self.getOntology(str(uri))
                if onto:
                    onto.properties += [aProp]
                    aProp.ontology = onto



            self.__buildDomainRanges(aProp)

            # add direct Supers
            directSupers = self.sparqlHelper.getPropDirectSupers(aProp.uri)

            for x in directSupers:
                superprop = self.getProperty(uri=x[0])
                # note: extra condition to avoid recursive structures
                if superprop and superprop.uri != aProp.uri:
                    aProp._parents.append(superprop)

                    # add inverse relationships (= direct subs for superprop)
                    if aProp not in superprop.children():
                         superprop._children.append(aProp)


        # sort alphabetically
        self.properties = sorted(self.properties, key=lambda x: x.qname)

        # computer top layer for properties
        exit = []
        for c in self.properties:
            if not c.parents():
                exit += [c]
        self.toplayerProperties = exit  # sorted(exit, key=lambda x: x.id) # doesnt work




    def extract_skos_concepts(self):
        """
        2015-08-19: first draft
        """
        self.skosConcepts = [] # @todo: keep adding?

        qres = self.sparqlHelper.getSKOSInstances()

        for candidate in qres:

            test_existing_cl = self.getSkosConcept(uri=candidate[0])
            if not test_existing_cl:
                # create it
                self.skosConcepts += [OntoSKOSConcept(candidate[0], None, self.namespaces)]
            else:
                pass

        #add more data
        skos = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')

        for aConcept in self.skosConcepts:

            aConcept.rdftype = skos['Concept']
            aConcept.triples = self.sparqlHelper.entityTriples(aConcept.uri)
            aConcept._buildGraph() # force construction of mini graph

            aConcept.sparqlHelper = self.sparqlHelper

            # attach to an ontology
            for uri in aConcept.getValuesForProperty(rdflib.RDFS.isDefinedBy):
                onto = self.getOntology(str(uri))
                if onto:
                    onto.skosConcepts += [aConcept]
                    aConcept.ontology = onto

            # add direct Supers
            directSupers = self.sparqlHelper.getSKOSDirectSupers(aConcept.uri)

            for x in directSupers:
                superclass = self.getSkosConcept(uri=x[0])
                # note: extra condition to avoid recursive structures
                if superclass and superclass.uri != aConcept.uri:
                    aConcept._parents.append(superclass)

                    # add inverse relationships (= direct subs for superclass)
                    if aConcept not in superclass.children():
                         superclass._children.append(aConcept)


        # sort alphabetically
        self.skosConcepts = sorted(self.skosConcepts, key=lambda x: x.qname)

        # compute top layer for skos
        exit = []
        for c in self.skosConcepts:
            if not c.parents():
                exit += [c]
        self.toplayerSkosConcepts = exit  # sorted(exit, key=lambda x: x.id) # doesnt work




    def extract_shapes(self):
        """
        Extract SHACL data shapes from the rdf graph.
        <http://www.w3.org/ns/shacl#>

        Instatiate the Shape Python objects and relate it to existing classes,
        if available.
        """
        self.shapes = [] # @todo: keep adding?

        qres = self.sparqlHelper.getShapes()

        for candidate in qres:

            test_existing_cl = self.getEntity(uri=candidate[0])
            if not test_existing_cl:
                # create it
                self.shapes += [OntoShape(candidate[0], None, self.namespaces)]
            else:
                pass

        #add more data
        shacl = rdflib.Namespace('http://www.w3.org/ns/shacl#')

        for aShape in self.shapes:

            aShape.rdftype = shacl['Shape']
            aShape.triples = self.sparqlHelper.entityTriples(aShape.uri)
            aShape._buildGraph() # force construction of mini graph

            aShape.sparqlHelper = self.sparqlHelper

            # attach to a class
            for uri in aShape.getValuesForProperty(shacl['targetClass']):
                aclass = self.getClass(str(uri))
                if aclass:
                    aShape.targetClasses += [aclass]
                    aclass.shapes += [aShape]


        # sort alphabetically
        self.shapes = sorted(self.shapes, key=lambda x: x.qname)

        # compute top layer
        exit = []
        for c in self.shapes:
            if not c.parents():
                exit += [c]
        self.toplayerShapes = exit  # sorted(exit, key=lambda x: x.id) # doesnt work





    # ------------
    # === methods to refine the ontology structure  === #
    # ------------



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
                    aProp.domains += [OntoClass(x, None, self.namespaces, ext_model=True)] # edge case: it's not an OntoClass instance

        for x in ranges:
            if not isBlankNode(x):
                aClass = self.getClass(uri=str(x))
                if aClass:
                    aProp.ranges += [aClass]
                    aClass.range_of += [aProp]
                else:
                    # eg a DataType property has xsd:STRING
                    # here we're storing an ontospy entities but not adding it to
                    # the main index
                    aProp.ranges += [OntoClass(x, None, self.namespaces, ext_model=True)]




    def __computeTopLayer(self):

        """
        deprecated: now this is calculated when entities get extracted
        """

        exit = []
        for c in self.classes:
            if not c.parents():
                exit += [c]
        self.toplayer = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

        # properties
        exit = []
        for c in self.properties:
            if not c.parents():
                exit += [c]
        self.toplayerProperties = exit  # sorted(exit, key=lambda x: x.id) # doesnt work

        # skos
        exit = []
        for c in self.skosConcepts:
            if not c.parents():
                exit += [c]
        self.toplayerSkosConcepts = exit  # sorted(exit, key=lambda x: x.id) # doesnt work


    def __computeInferredProperties(self):
        """

        :return: attach a list of dicts to each class, detailing valid props up the subsumption tree
        """
        exit = []
        for c in self.classes:
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

        if rel=="domain_of":
            _list.append({aClass: aClass.domain_of})
            for x in aClass.ancestors():
                if x.domain_of:
                    _list.append({x: x.domain_of})

            # add properties from Owl:Thing ie the inference layer

            topLevelProps = [p for p in self.properties if p.domains == []]
            if topLevelProps:
                _list.append({self.OWLTHING: topLevelProps})

        elif rel=="range_of":
            _list.append({aClass: aClass.range_of})
            for x in aClass.ancestors():
                if x.domain_of:
                    _list.append({x: x.range_of})

            # add properties from Owl:Thing ie the inference layer

            topLevelProps = [p for p in self.properties if p.ranges == []]
            if topLevelProps:
                _list.append({self.OWLTHING: topLevelProps})

        return _list





    # ------------
    # === utils === #
    # ------------


    def stats(self):
        """ shotcut to pull out useful info for a graph"""
        out = []
        out += [("Ontologies", len(self.ontologies))]
        out += [("Triples", self.triplesCount())]
        out += [("Classes", len(self.classes))]
        out += [("Properties", len(self.properties))]
        out += [("Annotation Properties", len(self.annotationProperties))]
        out += [("Object Properties", len(self.objectProperties))]
        out += [("Datatype Properties", len(self.datatypeProperties))]
        out += [("Skos Concepts", len(self.skosConcepts))]
        out += [("Data Shapes", len(self.shapes))]
        # out += [("Individuals", len(self.individuals))] @TODO
        out += [("Data Sources", len(self.sources))]
        return out


    def triplesCount(self):
        """

        2016-08-18 the try/except is a dirty solution to a problem
        emerging with counting graph length on cached Graph objects..
        """
        # @todo  investigate what's going on..
        # click.secho(unicode(type(self.rdfgraph)), fg="red")
        try:
            return len(self.rdfgraph)
        except:
            click.secho("Ontospy: error counting graph length..", fg="red")
            return 0



    # ===============
    # methods for retrieving objects
    # ================


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


    def printClassTree(self, element=None, showids=False, labels=False, showtype=False):
        """
        Print nicely into stdout the class tree of an ontology

        Note: indentation is made so that ids up to 3 digits fit in, plus a space.
        [123]1--
        [1]123--
        [12]12--
        """
        TYPE_MARGIN = 11 # length for owl:class etc..

        if not element:	 # first time
            for x in self.toplayer:
                printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

        else:
            printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)


    def printPropertyTree(self, element = None, showids=False, labels=False, showtype=False):
        """
        Print nicely into stdout the property tree of an ontology

        Note: indentation is made so that ids up to 3 digits fit in, plus a space.
        [123]1--
        [1]123--
        [12]12--
        """
        TYPE_MARGIN = 18 # length for owl:AnnotationProperty etc..

        if not element:	 # first time
            for x in self.toplayerProperties:
                printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

        else:
            printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)


    def printSkosTree(self, element = None, showids=False, labels=False, showtype=False):
        """
        Print nicely into stdout the SKOS tree of an ontology

        Note: indentation is made so that ids up to 3 digits fit in, plus a space.
        [123]1--
        [1]123--
        [12]12--
        """
        TYPE_MARGIN = 13 # length for skos:concept

        if not element:	 # first time
            for x in self.toplayerSkosConcepts:
                printGenericTree(x, 0, showids, labels, showtype, TYPE_MARGIN)

        else:
            printGenericTree(element, 0, showids, labels, showtype, TYPE_MARGIN)


    def ontologyClassTree(self):
        """
        Returns a dict representing the ontology tree
        Top level = {0:[top classes]}
        Multi inheritance is represented explicitly
        """
        treedict = {}
        if self.classes:
            treedict[0] = self.toplayer
            for element in self.classes:
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
        if self.properties:
            treedict[0] = self.toplayerProperties
            for element in self.properties:
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
        if self.skosConcepts:
            treedict[0] = self.toplayerSkosConcepts
            for element in self.skosConcepts:
                if element.children():
                    treedict[element] = element.children()
            return treedict
        return treedict



    def ontologyShapeTree(self):
        """
        Returns a dict representing the ontology tree
        Top level = {0:[top properties]}
        Multi inheritance is represented explicitly
        """
        treedict = {}
        if self.shapes:
            treedict[0] = self.toplayerShapes
            for element in self.shapes:
                if element.children():
                    treedict[element] = element.children()
            return treedict
        return treedict
