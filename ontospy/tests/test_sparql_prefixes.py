# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for the PREFIX declarations sent to SPARQL endpoints (#14): rdflib's SPARQLStore
prepends every prefix bound on the graph to each query, which since rdflib 7 means ~30
well-known ones the query doesn't use. No network needed: the store's HTTP call is
replaced by a stub that records the queries.

Run like this:

$ pytest ontospy/tests/test_sparql_prefixes.py

"""

import re

import pytest
import rdflib
from rdflib.query import Result

from .. import Ontospy


@pytest.fixture
def endpoint():
	"""an endpoint graph whose queries are recorded in `g.sent` instead of being sent"""
	g = Ontospy(sparql_endpoint="http://example.invalid/sparql")
	g.sent = []

	def fake_query(query, default_graph=None):
		g.sent.append(query)
		result = Result("SELECT")
		result.vars, result.bindings = [], []
		return result

	g.rdflib_graph.store._query = fake_query
	return g


def declared(query):
	"""prefix => namespace for the PREFIX lines of a query, failing on duplicates"""
	found = re.findall(r"PREFIX\s+([\w.-]*):\s*<([^>]*)>", query)
	assert len(found) == len({p for p, _ in found}), "a prefix is declared twice"
	return dict(found)


def test_own_queries_send_few_prefixes(endpoint):
	endpoint.sparqlHelper.getAllClasses()
	sent = declared(endpoint.sent[-1])
	assert {"rdf", "rdfs", "owl"} <= set(sent)
	assert {"brick", "dcat", "odrl", "sosa"}.isdisjoint(sent)
	assert len(sent) <= 12


def test_user_query_gets_the_prefixes_it_uses(endpoint):
	"""rdflib's well-known prefixes still work in queries without a PREFIX declaration"""
	endpoint.query("SELECT ?x WHERE { ?x a foaf:Person ; schema:name ?n }")
	sent = declared(endpoint.sent[-1])
	assert sent["foaf"] == "http://xmlns.com/foaf/0.1/"
	assert sent["schema"] == "https://schema.org/"
	assert {"brick", "dcat", "odrl", "sosa"}.isdisjoint(sent)


def test_user_query_with_its_own_prefixes(endpoint):
	endpoint.query("PREFIX ex: <http://example.org/> SELECT ?x WHERE { ?x a ex:Thing }")
	assert declared(endpoint.sent[-1])["ex"] == "http://example.org/"


def test_namespaces_still_list_the_defaults(endpoint):
	"""Ontospy.namespaces is unchanged for endpoints, so qnames are too"""
	prefixes = {p for p, _ in endpoint.namespaces}
	assert {"foaf", "schema", "skos", "owl"} <= prefixes
