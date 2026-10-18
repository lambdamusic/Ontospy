# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for looking entities up by URI, eg get_class(uri=...), which since backlog #13
uses an index rather than scanning the entity lists.

Run like this:

$ pytest ontospy/tests/test_lookup.py

"""

import pytest

from .. import Ontospy
from ..core.entities import OntoClass

NS = "http://example.org/l#"

ONTO = """
@prefix : <http://example.org/l#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://example.org/l> a owl:Ontology .
:Animal a owl:Class .
:Dog a owl:Class ; rdfs:subClassOf :Animal .
:Cat a owl:Class ; rdfs:subClassOf :ANIMAL .
:givenName a owl:DatatypeProperty .
:givenname a owl:DatatypeProperty ; rdfs:subPropertyOf :givenName .
:c1 a skos:Concept ; skos:broader :c2 .
:c2 a skos:Concept .
"""


@pytest.fixture(scope="module")
def g():
	return Ontospy(data=ONTO, rdf_format="turtle", verbose=False)


def test_lookup_is_case_insensitive(g):
	assert str(g.get_class(uri=NS + "Dog").uri) == NS + "Dog"
	assert g.get_class(uri=NS + "dOG") is g.get_class(uri=NS + "Dog")
	assert g.get_class(NS + "DOG") is g.get_class(uri=NS + "Dog")  # a URI passed as id
	assert g.get_skos(uri=NS + "C1") is g.get_skos(uri=NS + "c1")
	assert str(g.get_ontology(uri="http://example.org/L").uri) == "http://example.org/l"
	assert g.get_class(uri=NS + "Nothing") is None
	# unlike properties, classes whose URIs differ only by case are still merged: :ANIMAL is :Animal
	assert g.get_class(uri=NS + "Cat").parents() == [g.get_class(uri=NS + "Animal")]


def test_uris_differing_by_case(g):
	"""foaf:givenName and foaf:givenname are two properties: both are found, and a
	lookup returns the first one in the list (qname order), as a scan of the list did"""
	props = [p for p in g.all_properties if "iven" in p.uri]
	assert [str(p.uri) for p in props] == [NS + "givenName", NS + "givenname"]
	assert g.get_property(uri=NS + "givenName") is props[0]
	assert g.get_property(uri=NS + "givenname") is props[0]
	assert g.get_property(match="givenname") == props
	assert props[1].parents() == [props[0]]


def test_index_follows_the_lists():
	"""the index is per list: appending to all_classes, or assigning it a new list, is seen
	by the next lookup"""
	g = Ontospy(data=ONTO, rdf_format="turtle", verbose=False)
	assert g.get_class(uri=NS + "Bird") is None
	bird = OntoClass(NS + "Bird")
	g.all_classes += [bird]
	assert g.get_class(uri=NS + "bird") is bird
	g.all_classes = [bird]
	assert g.get_class(uri=NS + "Dog") is None
	assert g.get_class(uri=NS + "Bird") is bird
	g.all_classes = []
	assert g.get_class(uri=NS + "Bird") is None
	# the entities that are found are the same as with a scan
	g2 = Ontospy(data=ONTO, rdf_format="turtle", verbose=False)
	for x in g2.all_classes + g2.all_properties + g2.all_skos_concepts:
		scan = g2._get_defined_entity(uri=x.uri.upper(), candidates_list=g2.all_classes)
		assert g2.get_class(uri=x.uri.upper()) is scan
