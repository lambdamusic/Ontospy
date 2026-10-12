# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for recognising properties and their types.

Run like this:

$ pytest ontospy/tests/test_property_types.py

"""

import pytest
import rdflib

from .. import Ontospy

ONTO = """
@prefix : <http://example.org/b#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:Shape a owl:Class .

# as in Brick (#118): a class of properties, subclass of owl:ObjectProperty
:EntityProperty a owl:Class ; rdfs:subClassOf owl:ObjectProperty .
:tilt a :EntityProperty ; rdfs:range :Shape .

# two levels down, from owl:DatatypeProperty
:Measure a owl:Class ; rdfs:subClassOf owl:DatatypeProperty .
:Length a owl:Class ; rdfs:subClassOf :Measure .
:height a :Length .

# several types: the main one must win whatever the order (#10, #53)
:hasBase a owl:ObjectProperty, owl:FunctionalProperty, owl:InverseFunctionalProperty .
:name a owl:DatatypeProperty, owl:FunctionalProperty .
:depth a :Length, owl:FunctionalProperty .
:ancestorOf a rdf:Property, owl:TransitiveProperty .
:plain a rdf:Property .
"""

NS = "http://example.org/b#"


@pytest.fixture(scope="module")
def g():
	return Ontospy(data=ONTO, rdf_format="turtle", verbose=False)


def test_typed_by_subclass_of_object_property(g):
	tilt = g.get_property(uri=NS + "tilt")
	assert tilt is not None
	assert tilt.rdftype == rdflib.OWL.ObjectProperty
	assert tilt in g.all_properties_object
	assert [x.qname for x in tilt.ranges] == ["b:Shape"]


def test_typed_by_subclass_of_datatype_property(g):
	height = g.get_property(uri=NS + "height")
	assert height is not None
	assert height.rdftype == rdflib.OWL.DatatypeProperty
	assert height.rdftype_qname == "owl:DatatypeProperty"
	assert height in g.all_properties_datatype


def test_property_classes_are_still_classes(g):
	assert g.get_class(uri=NS + "EntityProperty") is not None
	assert g.get_property(uri=NS + "EntityProperty") is None


MAIN_TYPES = {
	"owl:ObjectProperty": rdflib.OWL.ObjectProperty,
	"owl:DatatypeProperty": rdflib.OWL.DatatypeProperty,
	"rdf:Property": rdflib.RDF.Property,
}


@pytest.mark.parametrize("name, main_type", [
	("hasBase", "owl:ObjectProperty"),
	("name", "owl:DatatypeProperty"),
	("depth", "owl:DatatypeProperty"),
	("ancestorOf", "owl:ObjectProperty"),
	("plain", "rdf:Property"),
])
def test_main_type(g, name, main_type):
	"""The main type doesn't depend on which type sorts first (#10)"""
	p = g.get_property(uri=NS + name)
	assert p.rdftype_qname == main_type
	assert p.rdftype == MAIN_TYPES[main_type]


def test_all_types_listed(g):
	"""All rdf:types are available for display, not just the main one (#53)"""
	assert g.get_property(uri=NS + "hasBase").rdftypes_qnames == [
		"owl:FunctionalProperty", "owl:InverseFunctionalProperty", "owl:ObjectProperty"]
	assert g.get_property(uri=NS + "depth").rdftypes_qnames == ["b:Length", "owl:FunctionalProperty"]


def test_unique_slugs():
	"""URIs that differ only by case, eg FOAF's givenname and givenName, are two
	properties since 2.4: their slugs, ie their page names, must differ too"""
	g = Ontospy(data=ONTO + """
	:givenName a owl:DatatypeProperty .
	:givenname a owl:DatatypeProperty .
	""", rdf_format="turtle", verbose=False)
	slugs = {p.uri.split("#")[1]: p.slug for p in g.all_properties if "iven" in p.uri}
	assert slugs == {"givenName": "prop-bgivenname", "givenname": "prop-bgivenname-2"}
	entities = g.all_ontologies + g.all_classes + g.all_properties + g.all_skos_concepts + g.all_shapes
	assert len({e.slug for e in entities}) == len(entities)
