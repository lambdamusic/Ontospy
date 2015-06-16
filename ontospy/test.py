#!/usr/bin/env python
# encoding: utf-8

# script used in development for testing

import ontospy
import rdflib


g = ontospy.Graph("data/schemas/fabio.rdf")


for x in g.classes:
	print x, x.count()


# g = ontospy.Graph("http://dbpedia.org/sparql", endpoint=True)
# g = ontospy.Graph("http://factforge.net/sparql", endpoint=True)


# endpoints = ["http://uriburner.com/sparql", "http://www.w3.org/wiki/SparqlEndpoints", "http://data.semanticweb.org/sparql", "http://zbw.eu/beta/sparql/", "http://factforge.net/sparql", "http://sparql.vivo.ufl.edu/"]
#
#
#
# g = ontospy.SparqlEndpoint("http://factforge.net/sparql")