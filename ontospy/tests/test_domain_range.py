# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for domains and ranges: properties without their own rdfs:domain or
rdfs:range inherit them from their superproperties (#126).

Run like this:

$ pytest ontospy/tests/test_domain_range.py

"""

import pytest

from .. import Ontospy

ONTO = """
@prefix : <http://example.org/fam#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Agent a owl:Class .
:Person a owl:Class ; rdfs:subClassOf :Agent .
:Woman a owl:Class ; rdfs:subClassOf :Person .

:hasRelative a owl:ObjectProperty ; rdfs:domain :Person ; rdfs:range :Person .
:hasParent a owl:ObjectProperty ; rdfs:subPropertyOf :hasRelative .
:hasMother a owl:ObjectProperty ; rdfs:subPropertyOf :hasParent ; rdfs:range :Woman .

:name a owl:DatatypeProperty ; rdfs:domain :Agent ; rdfs:range xsd:string .
:nickname a owl:DatatypeProperty ; rdfs:subPropertyOf :name .

:related a owl:ObjectProperty .
:range_bnode a owl:ObjectProperty ; rdfs:range [ a owl:Class ; owl:unionOf ( :Person :Agent ) ] .
"""

NS = "http://example.org/fam#"


@pytest.fixture(scope="module")
def g():
	return Ontospy(data=ONTO, rdf_format="turtle", verbose=False)


def qnames(entities):
	return [x.qname for x in entities]


def test_declared_domains_unchanged(g):
	p = g.get_property(uri=NS + "hasRelative")
	assert qnames(p.domains) == ["fam:Person"]
	assert p.domains_inferred == [] and p.ranges_inferred == []


def test_inherited_from_superproperties(g):
	parent = g.get_property(uri=NS + "hasParent")
	assert parent.domains == [] and parent.ranges == []
	assert qnames(parent.domains_inferred) == ["fam:Person"]
	assert qnames(parent.ranges_inferred) == ["fam:Person"]
	# two levels up; the declared range wins over the inherited one
	mother = g.get_property(uri=NS + "hasMother")
	assert qnames(mother.domains_inferred) == ["fam:Person"]
	assert qnames(mother.ranges) == ["fam:Woman"] and mother.ranges_inferred == []
	# external ranges, eg xsd:string, are inherited too
	nickname = g.get_property(uri=NS + "nickname")
	assert qnames(nickname.ranges_inferred) == ["xsd:string"]


def test_class_usage(g):
	"""Properties with an inherited domain are listed under that class, not owl:Thing"""
	person = g.get_class(uri=NS + "Person")
	usage = {k.qname: qnames(v) for group in person.domain_of_inferred for k, v in group.items()}
	assert usage["fam:Person"] == ["fam:hasRelative", "fam:hasMother", "fam:hasParent"]
	assert usage["fam:Agent"] == ["fam:name", "fam:nickname"]
	assert usage["owl:Thing"] == ["fam:range_bnode", "fam:related"]
	# explicitly declared domains stay as they were
	assert qnames(person.domain_of) == ["fam:hasRelative"]


def test_class_range_of(g):
	woman = g.get_class(uri=NS + "Woman")
	usage = {k.qname: qnames(v) for group in woman.range_of_inferred for k, v in group.items()}
	assert usage["fam:Woman"] == ["fam:hasMother"]
	assert usage["fam:Person"] == ["fam:hasRelative", "fam:hasParent"]
	assert "fam:hasMother" not in usage["owl:Thing"]


def test_blank_node_range(g):
	"""A blank node range used to be added to the property's domains"""
	p = g.get_property(uri=NS + "range_bnode")
	assert p.domains == []
	assert len(p.ranges) == 1 and p.ranges[0].is_Bnode
