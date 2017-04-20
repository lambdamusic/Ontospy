# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

"""
Python and RDF Utils for OntoSpy

Copyright (c) 2013-2017 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""


import rdflib
from .utils import *

DEFAULT_LANGUAGE = "en"





class QueryHelper(object):
    """
    A bunch of RDF queries

    2015-10-1: note - the sparql query returns always a
    rdflib.plugins.sparql.processor.SPARQLResult instance; the list method
    transforms it into a list of tuples/triples results
    eg:
    [(rdflib.term.URIRef(u'http://www.w3.org/2006/time'))]
    2016-02-12: note - when a list is returned, the object is extracted with index [0]
    """


    def __init__(self, rdfgraph):
        super(QueryHelper, self).__init__()
        self.rdfgraph = rdfgraph

        # TODO add 2 versions of queries, one for declared classes only,
        # one with basic (RDFS+?) inference too
        self.inference = False

        # Bind a few prefix, namespace pairs for easier sparql querying
        self.rdfgraph.bind("rdf", rdflib.namespace.RDF)
        self.rdfgraph.bind("rdfs", rdflib.namespace.RDFS)
        self.rdfgraph.bind("owl", rdflib.namespace.OWL)
        self.rdfgraph.bind("skos", rdflib.namespace.SKOS)




    # ..................
    # ONTOLOGY OBJECT
    # ..................


    def getOntology(self):
        qres = self.rdfgraph.query(
            """SELECT DISTINCT ?x
               WHERE {
                  ?x a owl:Ontology
               }""")
        return list(qres)





    # ..................
    # RDF/OWL CLASSES
    # ..................



    def getAllClasses(self, hide_base_schemas=True):
        """
        by default, obscure all RDF/RDFS/OWL/XML stuff
        2016-05-06: not obscured anymore
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
                             # union
                             # { ?y rdf:type ?x }
                         } .

                         ?x a ?c

                    %s

                 }
                 ORDER BY  ?x
                 """
        if hide_base_schemas:
            query = query %  """FILTER(
                     !STRSTARTS(STR(?x), "http://www.w3.org/2002/07/owl")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/1999/02/22-rdf-syntax-ns")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/2000/01/rdf-schema")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/2001/XMLSchema")
                     && !STRSTARTS(STR(?x), "http://www.w3.org/XML/1998/namespace")
                     && (!isBlank(?x))
                      ) ."""
        else:
            query = query % ""

        qres = self.rdfgraph.query(query)
        return list(qres)


    #legacy

    def getAllClassesFromInstancesToo(self):
        """
        by default, obscure all RDF/RDFS/OWL/XML stuff
        NOTE: this is more expensive!

        added: { ?y rdf:type ?x }
        """
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x ?c
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
                             { ?y rdf:type ?x }
                             union
                             { ?y rdfs:domain ?x }
                             union
                             { ?y rdfs:range ?x }
                         } .

                         ?x a ?c

                     FILTER(
                       !STRSTARTS(STR(?x), "http://www.w3.org/2002/07/owl")
                       && !STRSTARTS(STR(?x), "http://www.w3.org/1999/02/22-rdf-syntax-ns")
                       && !STRSTARTS(STR(?x), "http://www.w3.org/2000/01/rdf-schema")
                       && !STRSTARTS(STR(?x), "http://www.w3.org/2001/XMLSchema")
                       && !STRSTARTS(STR(?x), "http://www.w3.org/XML/1998/namespace")
                       && (!isBlank(?x))
                       ) .
                 }
                 ORDER BY  ?x
                 """)
        return list(qres)


    def getClassInstances(self, aURI):
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
                 WHERE {
                     { ?x rdf:type <%s> }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        return list(qres)

    def getClassInstancesCount(self, aURI):
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT (COUNT(?x) AS ?count )
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


    def getClassDirectSupers(self, aURI):
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
                 WHERE {
                     { <%s> rdfs:subClassOf ?x }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        return list(qres)


    def getClassDirectSubs(self, aURI):
        """
        2015-06-03: currenlty not used, inferred from above
        """
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
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
            qres = self.rdfgraph.query(
                  """SELECT DISTINCT ?x
                     WHERE {
                         { <%s> rdfs:subClassOf+ ?x }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug("... warning: the 'getClassAllSupers' query failed (maybe missing SPARQL 1.1 support?)")
            qres = []
        return list(qres)


    def getClassAllSubs(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdfgraph.query(
                  """SELECT DISTINCT ?x
                     WHERE {
                         { ?x rdfs:subClassOf+ <%s> }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug("... warning: the 'getClassAllSubs' query failed (maybe missing SPARQL 1.1 support?)")
            qres = []
        return list(qres)



    # ..................
    # RDF PROPERTIES
    # ..................


    # NOTE this kinf of query could be expanded to classes too!!!
    def getAllProperties(self):
        qres = self.rdfgraph.query(
              """SELECT ?x ?c WHERE {
                        {
                            { ?x a rdf:Property }
                             UNION
                             { ?x a owl:ObjectProperty }
                             UNION
                             { ?x a owl:DatatypeProperty }
                             UNION
                             { ?x a owl:AnnotationProperty }
                        } .
                        ?x a ?c
                     FILTER(!isBlank(?x)
                       ) .
                    } ORDER BY	?c ?x
                 """)
        return list(qres)


    def getPropDirectSupers(self, aURI):
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
                 WHERE {
                     { <%s> rdfs:subPropertyOf ?x }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """ % (aURI))
        return list(qres)


    def getPropAllSupers(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdfgraph.query(
                  """SELECT DISTINCT ?x
                     WHERE {
                         { <%s> rdfs:subPropertyOf+ ?x }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug("... warning: the 'getPropAllSupers' query failed (maybe missing SPARQL 1.1 support?)")
            qres = []
        return list(qres)


    def getPropAllSubs(self, aURI):
        """
        note: requires SPARQL 1.1
        2015-06-04: currenlty not used, inferred from above
        """
        aURI = aURI
        try:
            qres = self.rdfgraph.query(
                  """SELECT DISTINCT ?x
                     WHERE {
                         { ?x rdfs:subPropertyOf+ <%s> }
                         FILTER (!isBlank(?x))
                     }
                     """ % (aURI))
        except:
            printDebug("... warning: the 'getPropAllSubs' query failed (maybe missing SPARQL 1.1 support?)")
            qres = []
        return list(qres)




    # ..................
    # SKOS	: 2015-08-19
    # ..................


    def getSKOSInstances(self):
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
                 WHERE {
                     { ?x rdf:type skos:Concept }
                     FILTER (!isBlank(?x))
                 } ORDER BY ?x
                 """)
        return list(qres)


    def getSKOSDirectSupers(self, aURI):
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
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


    def getSKOSDirectSubs(self, aURI):
        """
        2015-08-19: currenlty not used, inferred from above
        """
        aURI = aURI
        qres = self.rdfgraph.query(
              """SELECT DISTINCT ?x
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





    # ..................
    # UTILS
    # ..................



    def entityTriples(self, aURI):
        """ Builds all triples for an entity
        Note: if a triple object is a blank node (=a nested definition)
        we try to extract all relevant data recursively (does not work with
        sparql endpoins)
        2015-10-18: updated
        """

        aURI = aURI
        qres = self.rdfgraph.query(
              """CONSTRUCT {<%s> ?y ?z }
                 WHERE {
                     { <%s> ?y ?z }
                 }
                 """ % (aURI, aURI ))
        lres = list(qres)

        def recurse(triples_list):
            """ uses the rdflib <triples> method to pull out all blank nodes info"""
            out = []
            for tripl in triples_list:
                if isBlankNode(tripl[2]):
                    # print "blank node", str(tripl[2])
                    temp = [x for x in self.rdfgraph.triples((tripl[2], None, None))]
                    out += temp + recurse(temp)
                else:
                    pass
            return out

        try:
            return lres + recurse(lres)
        except:
            printDebug("Error extracting blank nodes info", "important")
            return lres
