# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Python and RDF Utils for Ontospy

Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""

import rdflib
from .utils import *

DEFAULT_LANGUAGE = "en"


class SparqlHelper(object):
    """
    Class containing a bunch of useful RDF queries.

    Tip:the sparql query returns always a `rdflib.plugins.sparql.processor.SPARQLResult` instance;
    calling the list method on it transforms it into a list of tuples/triples

    Eg
    [(rdflib.term.URIRef(u'http://www.w3.org/2006/time'))]

    Hence, when a list is returned, the URI/entity is extracted with index [0]
    """

    def __init__(self, rdfgraph, sparql_endpoint=False):
        super(SparqlHelper, self).__init__()
        self.rdflib_graph = rdfgraph
        self.sparql_endpoint = sparql_endpoint

        # Bind a few prefix, namespace pairs for easier sparql querying
        self.rdflib_graph.bind("rdf", rdflib.namespace.RDF)
        self.rdflib_graph.bind("rdfs", rdflib.namespace.RDFS)
        self.rdflib_graph.bind("owl", rdflib.namespace.OWL)
        self.rdflib_graph.bind("skos", rdflib.namespace.SKOS)
        self.rdflib_graph.bind("dc", "http://purl.org/dc/elements/1.1/")
        self.rdflib_graph.bind("vann", "http://purl.org/vocab/vann/")
        self.rdflib_graph.bind("void", "http://rdfs.org/ns/void#")
        self.rdflib_graph.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
        self.rdflib_graph.bind("sh", "http://www.w3.org/ns/shacl#")

    # ..................
    # ONTOLOGY
    # ..................

    def getOntology(self):
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
               WHERE {
                  ?x a owl:Ontology
               }""")
        return list(qres)

    # ..................
    # RDF/OWL CLASSES
    # ..................

    def getAllClasses(self, hide_base_schemas=True, hide_implicit_types=True):
        """
        * hide_base_schemas: by default, obscure all RDF/RDFS/OWL/XML stuff
        * hide_implicit_types: don't make any inference based on rdf:type declarations
        """
        query = """SELECT DISTINCT ?x ?c
                 WHERE {
                         {
                             { ?x a owl:Class }
                             union
                             { ?x a rdfs:Class }
                             union
                             { ?x rdfs:subClassOf ?y }
                             union
                             { ?z rdfs:subClassOf ?x }
                             union
                             { ?y rdfs:domain ?x }
                             union
                             { ?y rdfs:range ?x }
                             %s
                         } .

                         OPTIONAL { ?x a ?c } 
                         # get the type too if available

                    %s

                 }
                 ORDER BY  ?x
                 """

        BIT_BASE_SCHEMAS = """FILTER(
                     !STRSTARTS(STR(?x), "http://www.w3.org/2002/07/owl")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/1999/02/22-rdf-syntax-ns")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/2000/01/rdf-schema")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/2001/XMLSchema")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/XML/1998/namespace")
                     && (!isBlank(?x))
                      ) ."""
        BIT_IMPLICIT_TYPES = """union
                             { ?y rdf:type ?x }"""

        if hide_base_schemas == False:  # ..then do not filter out XML stuff
            BIT_BASE_SCHEMAS = ""
        if hide_implicit_types == True:  # .. then do not add extra clause
            BIT_IMPLICIT_TYPES = ""

        query = query % (BIT_IMPLICIT_TYPES, BIT_BASE_SCHEMAS)

        # print(query)

        qres = self.rdflib_graph.query(query)
        return list(qres)

    def getClassInstances(self, aURI):
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                     { ?x rdf:type <%s> }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        return list(qres)

    def getClassDirectSupers(self, aURI):
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                     { <%s> rdfs:subClassOf ?x }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        return list(qres)

    # ..................
    # RDF PROPERTIES
    # ..................

    def getAllProperties(self, hide_implicit_preds=True):
        query = """SELECT ?x ?c WHERE {
                        {
                            { ?x a rdf:Property }
                             UNION
                             { ?x a owl:ObjectProperty }
                             UNION
                             { ?x a owl:DatatypeProperty }
                             UNION
                             { ?x a owl:AnnotationProperty }
                             %s
                        } .
                        OPTIONAL  {?x a ?c}
                        FILTER(!isBlank(?x)
                       ) .
                    } ORDER BY	?c ?x
                 """

        BIT_IMPLICIT_PREDICATES = """union
                             { ?a ?x ?b }"""
        if hide_implicit_preds:
            BIT_IMPLICIT_PREDICATES = ""
        query = query % BIT_IMPLICIT_PREDICATES
        # print(query)
        qres = self.rdflib_graph.query(query)
        return list(qres)

    def getPropDirectSupers(self, aURI):
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                     { <%s> rdfs:subPropertyOf ?x }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        return list(qres)

    # ..................
    # SKOS
    # ..................

    def getSKOSInstances(self):
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                     { ?x rdf:type skos:Concept }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """)
        return list(qres)

    def getSKOSDirectSupers(self, aURI):
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                         {
                             { <%s> skos:broader ?x }
                             UNION
                             { ?x skos:narrower <%s> }
                         }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI, aURI))
        return list(qres)

    # ..................
    # SHACL SHAPES
    # ..................

    def getShapes(self):
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
               WHERE {
                        { ?x a sh:Shape }
                        union
                        { ?x a sh:NodeShape }
                        union
                        { ?x a sh:PropertyShape }
                    } """)
        return list(qres)

    # ..................
    # UTILS
    # ..................

    def entityTriples(self, aURI):
        """ Builds all triples for an entity
        Note: if a triple object is a blank node (=a nested definition)
        we try to extract all relevant data recursively (does not work with
        sparql endpoins)
        """

        aURI = aURI
        qres = self.rdflib_graph.query("""CONSTRUCT {<%s> ?y ?z }
                 WHERE {
                     { <%s> ?y ?z }
                 }
                 """ % (aURI, aURI))
        lres = list(qres)

        def recurse(triples_list):
            """ uses the rdflib <triples> method to pull out all blank nodes info"""
            out = []
            for tripl in triples_list:
                if isBlankNode(tripl[2]):
                    # print "blank node", str(tripl[2])
                    temp = [
                        x for x in self.rdflib_graph.triples((tripl[2], None,
                                                              None))
                    ]
                    out += temp + recurse(temp)
                else:
                    pass
            return out

        if self.sparql_endpoint:
            return lres
        else:
            try:
                return lres + recurse(lres)
            except:
                printDebug("Error extracting blank nodes info", "important")
                return lres

    # ..................
    # UNUSED OR LEGACY
    # ..................

    def getClassInstancesCount(self, aURI):
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT (COUNT(?x) AS ?count )
                 WHERE {
                     { ?x rdf:type <%s> }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        try:
            return int(list(qres)[0][0])
        except:
            printDebug("Error with <getClassInstancesCount>")
            return 0

    def getClassDirectSubs(self, aURI):
        """
        2015-06-03: currenlty not used, inferred from above
        """
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                     { ?x rdfs:subClassOf <%s> }
                     FILTER (!isBlank(?x))
                 }
                 """ % (aURI))
        return list(qres)

    def getClassAllSupers(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                     WHERE {
                         { <%s> rdfs:subClassOf+ ?x }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug(
                "... warning: the 'getClassAllSupers' query failed (maybe missing SPARQL 1.1 support?)"
            )
            qres = []
        return list(qres)

    def getClassAllSubs(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                     WHERE {
                         { ?x rdfs:subClassOf+ <%s> }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug(
                "... warning: the 'getClassAllSubs' query failed (maybe missing SPARQL 1.1 support?)"
            )
            qres = []
        return list(qres)

    def getPropAllSupers(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                     WHERE {
                         { <%s> rdfs:subPropertyOf+ ?x }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug(
                "... warning: the 'getPropAllSupers' query failed (maybe missing SPARQL 1.1 support?)"
            )
            qres = []
        return list(qres)

    def getPropAllSubs(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                     WHERE {
                         { ?x rdfs:subPropertyOf+ <%s> }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug(
                "... warning: the 'getPropAllSubs' query failed (maybe missing SPARQL 1.1 support?)"
            )
            qres = []
        return list(qres)

    def getSKOSDirectSubs(self, aURI):
        """
        2015-08-19: currenlty not used, inferred from above
        """
        aURI = aURI
        qres = self.rdflib_graph.query("""SELECT DISTINCT ?x
                 WHERE {
                         {
                             { ?x skos:broader <%s> }
                             UNION
                             { <%s> skos:narrower ?s }
                         }
                     FILTER (!isBlank(?x))
                 }
                 """ % (aURI, aURI))
        return list(qres)