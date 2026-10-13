# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for namespace prefixes: the prefixes declared in the RDF sources win over
rdflib's defaults (#135).

Run like this:

$ pytest ontospy/tests/test_prefixes.py

"""

import rdflib

from .. import Ontospy
from .context import TEST_RDF_FOLDER

# rdflib binds `schema` to <https://schema.org/> by default; this declares it for <http://schema.org/>
SCHEMA_TTL = """
@prefix schema: <http://schema.org/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
schema:Person a owl:Class .
"""


def test_declared_prefix_wins_data():
	g = Ontospy(data=SCHEMA_TTL, rdf_format="turtle")
	assert [c.qname for c in g.all_classes] == ["schema:Person"]


def test_declared_prefix_wins_file(tmp_path):
	f = tmp_path / "schema-test.ttl"
	f.write_text(SCHEMA_TTL, encoding="utf-8")
	g = Ontospy(str(f))
	assert [c.qname for c in g.all_classes] == ["schema:Person"]
	assert "schema1" not in dict(g.rdflib_graph.namespaces())


def test_rdflib_defaults_fill_gaps():
	"""namespaces the source doesn't declare a prefix for still get rdflib's well-known ones"""
	nt = "<http://example.org/x> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> ."
	g = Ontospy(data=nt, rdf_format="nt")
	nm = g.rdflib_graph.namespace_manager
	assert nm.normalizeUri(rdflib.URIRef("http://xmlns.com/foaf/0.1/Person")) == "foaf:Person"


def test_jsonld_still_loads():
	"""JSON-LD is parsed into a ConjunctiveGraph, which rejects `bind_namespaces`: a wrong
	call there made JSON-LD sources fail silently"""
	g = Ontospy(TEST_RDF_FOLDER + "paper.jsonld")
	assert g.sources
	assert len(g.rdflib_graph) > 0


# #14: Ontospy.namespaces lists only the prefixes that matter for the graph, not all of
# rdflib's ~30 defaults (brick, csvw, dcat, odrl, sosa...)

SMALL_TTL = """
@prefix ex: <http://example.org/onto#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix unused: <http://example.org/unused#> .
ex:Person a owl:Class ; rdfs:label "Person" ; rdfs:seeAlso <http://xmlns.com/foaf/0.1/Person> .
"""


def prefixes(g):
	return {prefix for prefix, _ in g.namespaces}


def test_unused_rdflib_defaults_dropped():
	g = Ontospy(data=SMALL_TTL, rdf_format="turtle")
	assert {"brick", "csvw", "dcat", "odrl", "sosa", "xml"}.isdisjoint(prefixes(g))
	assert g.namespaces == sorted(g.namespaces)


def test_used_declared_and_core_prefixes_kept():
	g = Ontospy(data=SMALL_TTL, rdf_format="turtle")
	p = prefixes(g)
	assert {"ex", "owl", "rdfs"} <= p  # used
	assert "foaf" in p  # an rdflib default, used by a URI in the graph
	assert "unused" in p  # declared in the source, even if unused
	assert {"rdf", "xsd"} <= p  # core, eg for owl:Thing


def test_namespaces_with_graph_obj():
	"""a plain rdflib.Graph comes with rdflib's defaults bound: they don't count as declared"""
	graph = rdflib.Graph()
	graph.parse(data=SMALL_TTL, format="turtle")
	g = Ontospy(graph_obj=graph)
	assert {"brick", "csvw", "dcat", "odrl", "sosa"}.isdisjoint(prefixes(g))
	assert {"ex", "foaf", "unused"} <= prefixes(g)


def test_qnames_unchanged():
	"""only unused prefixes go, so no qname changes"""
	g = Ontospy(TEST_RDF_FOLDER + "pizza.ttl")
	all_prefixes = sorted(g.rdflib_graph.namespaces())
	from ..core.utils import uri2niceString
	for e in g.all_classes + g.all_properties:
		assert e.qname == uri2niceString(e.uri, all_prefixes)


def test_add_namespace_updates_namespaces():
	g = Ontospy(data=SMALL_TTL, rdf_format="turtle")
	g.add_namespace("myex", "http://example.org/onto#")
	assert ("myex", rdflib.URIRef("http://example.org/onto#")) in g.namespaces
	assert "ex" not in prefixes(g)  # rebinding the namespace replaces its old prefix
