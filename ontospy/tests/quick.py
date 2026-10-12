# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Test Quick: use this file to quickly run scripts/tests which will then be integrated into proper tests

"""

import click 

from .. import *
from ..core import *
from ..core.utils import *


from .context import TEST_RDF_FOLDER


# sanity check
print("-------------------\nOntospy ", VERSION, "\n-------------------")



@click.command()
@click.argument('test_number', nargs=1)
def main(test_number):

	test_number = int(test_number)


	if test_number == 1:

		print("=================\n*** QUICK TEST 1 ***\n=================\n")

		f = TEST_RDF_FOLDER + "paper.jsonld"

		o = Ontospy(f, verbose=True, rdf_format="json-ld", hide_implicit_types=False, hide_base_schemas=False, hide_implicit_preds=False)
		print(f)			



	if test_number == 2:

		print("=================\n*** QUICK TEST 2 ***\n=================\n")

		o = Ontospy(sparql_endpoint="http://dbpedia.org/sparql", verbose=True)		

		print(o), print("---------")

		q = o.query("select distinct ?b where {?x a ?b} limit 10")
		if q:
			for el in q:
				print(el)
		else:
			print("No results")


	if test_number == 3:

		from rdflib import Graph, Namespace, URIRef
		from rdflib.plugins.stores.sparqlstore import SPARQLStore
		from rdflib.term import Identifier

		print("Triple navigation using SPARQLStore as a Graph():")
		graph = Graph("SPARQLStore", identifier="http://dbpedia.org")
		graph.open("http://dbpedia.org/sparql")
		# we are asking DBPedia for 3 skos:Concept instances
		count = 0
		from rdflib.namespace import RDF, SKOS

		for s in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
			count += 1
			print(f"\t- {s}")
			if count >= 3:
				break

		q = graph.query("select distinct ?b where {?x a ?b} limit 10")
		if q:
			for el in q:
				print(el)
		


	if test_number == 4:

		print("=================\n*** QUICK TEST 4 ***\n=================\n")

		f = TEST_RDF_FOLDER + "pizza.ttl"

		o = Ontospy(f, verbose=True, rdf_format="ttl", hide_implicit_types=False, hide_base_schemas=True, hide_implicit_preds=False, hide_individuals=False)
		print(f)
		for x in o.all_individuals:
			print(x.qname, [z.uri for z in x.instance_of()])


if __name__ == '__main__':
	main()

