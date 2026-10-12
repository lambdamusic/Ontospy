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

:Shape a owl:Class .

# as in Brick (#118): a class of properties, subclass of owl:ObjectProperty
:EntityProperty a owl:Class ; rdfs:subClassOf owl:ObjectProperty .
:tilt a :EntityProperty ; rdfs:range :Shape .

# two levels down, from owl:DatatypeProperty
:Measure a owl:Class ; rdfs:subClassOf owl:DatatypeProperty .
:Length a owl:Class ; rdfs:subClassOf :Measure .
:height a :Length .
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
