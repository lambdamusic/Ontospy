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
