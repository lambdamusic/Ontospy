# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for the different kinds of RDF sources Ontospy can load from: rdflib graphs
(`graph_obj`, #111), open files (`file_obj`), and combinations of sources.

Run like this:

$ pytest ontospy/tests/test_sources.py

"""

import rdflib

from .. import Ontospy
from .context import TEST_RDF_FOLDER

PIZZA = TEST_RDF_FOLDER + "pizza.ttl"

ANIMALS_TTL = """
@prefix zoo: <http://example.org/zoo#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
zoo:Animal a owl:Class .
zoo:Cat a owl:Class ; rdfs:subClassOf zoo:Animal .
"""

PLANTS_TTL = """
@prefix garden: <http://example.org/garden#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
garden:Plant a owl:Class .
"""


def make_graph(ttl):
	g = rdflib.Graph()
	g.parse(data=ttl, format="turtle")
	return g


def test_graph_obj():
	o = Ontospy(graph_obj=make_graph(ANIMALS_TTL))
	assert sorted(c.qname for c in o.all_classes) == ["zoo:Animal", "zoo:Cat"]
	assert o.get_class(match="Cat")[0].parents()[0].qname == "zoo:Animal"
	assert len(o.sources) == 1


def test_graph_obj_not_modified():
	g = make_graph(ANIMALS_TTL)
	before = len(g)
	o = Ontospy(graph_obj=g, data=PLANTS_TTL, rdf_format="turtle")
	assert len(g) == before
	assert len(o.rdflib_graph) > before


def test_graph_obj_list():
	o = Ontospy(graph_obj=[make_graph(ANIMALS_TTL), make_graph(PLANTS_TTL)])
	assert sorted(c.qname for c in o.all_classes) == ["garden:Plant", "zoo:Animal", "zoo:Cat"]
	assert len(o.sources) == 2


def test_graph_obj_with_file():
	o = Ontospy(PIZZA, graph_obj=make_graph(ANIMALS_TTL))
	assert o.get_class(uri="http://example.org/zoo#Cat")
	assert o.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza")
	assert len(o.sources) == 2


def test_graph_obj_empty_graph():
	"""an empty graph is still a source: it shouldn't be mistaken for 'nothing to load'"""
	o = Ontospy(graph_obj=rdflib.Graph())
	assert o.rdflib_graph is not None
	assert o.all_classes == []


def test_file_obj_text():
	with open(PIZZA, encoding="utf-8") as f:
		o = Ontospy(file_obj=f)
	assert o.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza")
	assert o.sources == ["File: <%s>" % PIZZA]


def test_file_obj_binary():
	with open(PIZZA, "rb") as f:
		o = Ontospy(file_obj=f)
	assert o.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza")


def test_data_and_file_obj_combined():
	with open(PIZZA, encoding="utf-8") as f:
		o = Ontospy(data=ANIMALS_TTL, file_obj=f, rdf_format="turtle")
	assert o.get_class(uri="http://example.org/zoo#Cat")
	assert o.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza")
