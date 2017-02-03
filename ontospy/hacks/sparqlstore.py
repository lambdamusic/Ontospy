# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
# https://groups.google.com/forum/#!msg/rdflib-dev/1owj7Ghp1X8/pwClNSz_LI4J

from __future__ import print_function
from rdflib.plugins.stores.sparqlstore import SPARQLStore
import rdflib


store = SPARQLStore("http://dbpedia.org/sparql")
g = rdflib.ConjunctiveGraph(store=store)
r = g.query("select distinct ?Caoncept where {[] a ?Concept} LIMIT 100")
list(r)
# [(rdflib.term.URIRef(u'http://w...
#
# In order to serialize the result as JSON, you can do
#
serialized=r.serialize(format='json')
print(serialized)
# '{"head": {"vars"...


# legacy docs maybe
# https://github.com/RDFLib/rdflib-sparqlstore
# https://lawlesst.github.io/notebook/rdflib-stardog.html
# https://github.com/RDFLib/rdflib
