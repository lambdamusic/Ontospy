# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for walking class and property hierarchies: cycles must not cause a
RecursionError (#142), and deep or multiply-inherited trees must stay fast.

Run like this:

$ pytest ontospy/tests/test_hierarchy.py

"""

import time

from .. import Ontospy

PREFIXES = """
@prefix : <http://example.org/h#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
"""


def load(turtle):
	return Ontospy(data=PREFIXES + turtle, rdf_format="turtle", verbose=False)


def qnames(entities):
	return [x.qname for x in entities]


def test_class_cycle():
	"""A subClassOf B subClassOf C subClassOf A, eg classes declared equivalent this way"""
	g = load("""
	:A a owl:Class ; rdfs:subClassOf :B .
	:B a owl:Class ; rdfs:subClassOf :C .
	:C a owl:Class ; rdfs:subClassOf :A .
	""")
	a = g.get_class(uri="http://example.org/h#A")
	assert sorted(qnames(a.ancestors())) == ["h:A", "h:B", "h:C"]
	assert sorted(qnames(a.descendants())) == ["h:A", "h:B", "h:C"]
	assert g.ontologyClassTree()  # builds without recursing forever


def test_property_cycle():
	g = load("""
	:p a owl:ObjectProperty ; rdfs:subPropertyOf :q .
	:q a owl:ObjectProperty ; rdfs:subPropertyOf :p .
	""")
	p = g.get_property(uri="http://example.org/h#p")
	assert qnames(p.ancestors()) == ["h:q", "h:p"]
	assert qnames(p.descendants()) == ["h:q", "h:p"]


def test_order_is_depth_first():
	"""Ancestors come out depth first, without duplicates, as before"""
	g = load("""
	:Top a owl:Class .
	:L a owl:Class ; rdfs:subClassOf :Top .
	:R a owl:Class ; rdfs:subClassOf :Top .
	:Mid a owl:Class ; rdfs:subClassOf :L, :R .
	:Bottom a owl:Class ; rdfs:subClassOf :Mid .
	""")
	bottom = g.get_class(uri="http://example.org/h#Bottom")
	assert qnames(bottom.ancestors()) == ["h:Mid", "h:L", "h:Top", "h:R"]
	top = g.get_class(uri="http://example.org/h#Top")
	assert qnames(top.descendants()) == ["h:L", "h:Mid", "h:Bottom", "h:R"]


def test_deep_chain():
	"""A subclass chain deeper than Python's default recursion limit"""
	depth = 1500
	turtle = ":C0 a owl:Class .\n" + "\n".join(
		":C%d a owl:Class ; rdfs:subClassOf :C%d ." % (i, i - 1) for i in range(1, depth))
	g = load(turtle)
	leaf = g.get_class(uri="http://example.org/h#C%d" % (depth - 1))
	assert len(leaf.ancestors()) == depth - 1


def test_diamonds_are_fast():
	"""A lattice of diamonds: the number of paths doubles at each level, the classes don't"""
	levels = 25
	lines = [":N0 a owl:Class ."]
	for i in range(1, levels):
		lines += [
			":L%d a owl:Class ; rdfs:subClassOf :N%d ." % (i, i - 1),
			":R%d a owl:Class ; rdfs:subClassOf :N%d ." % (i, i - 1),
			":N%d a owl:Class ; rdfs:subClassOf :L%d, :R%d ." % (i, i, i),
		]
	g = load("\n".join(lines))
	leaf = g.get_class(uri="http://example.org/h#N%d" % (levels - 1))
	start = time.time()
	assert len(leaf.ancestors()) == 3 * (levels - 1)
	assert time.time() - start < 1


def test_description_with_uri_values():
	"""FOVT has rdfs:comment values that are URIs, which have no language tag"""
	g = load("""
	:A a owl:Class ; rdfs:comment <http://example.org/doc>, "a class"@en, "une classe"@fr .
	:B a owl:Class ; rdfs:label <http://example.org/label>, "B"@en .
	""")
	a = g.get_class(uri="http://example.org/h#A")
	assert str(a.bestDescription()) == "a class"
	b = g.get_class(uri="http://example.org/h#B")
	assert str(b.bestLabel()) == "B"


def tree_qnames(treedict):
	return {(k if k == 0 else k.qname): qnames(v) for k, v in treedict.items()}


def test_non_redundant_tree():
	"""PR #87: in a reasoned graph RedBeardedGuy is also a direct subclass of Mammal"""
	g = load("""
	:Mammal a owl:Class .
	:Human a owl:Class ; rdfs:subClassOf :Mammal .
	:RedBeardedGuy a owl:Class ; rdfs:subClassOf :Human, :Mammal .
	""")
	assert tree_qnames(g.ontologyClassTree()) == {
		0: ["h:Mammal"], "h:Human": ["h:RedBeardedGuy"], "h:Mammal": ["h:Human", "h:RedBeardedGuy"]}
	assert tree_qnames(g.ontologyClassTree(non_redundant=True)) == {
		0: ["h:Mammal"], "h:Human": ["h:RedBeardedGuy"], "h:Mammal": ["h:Human"]}


def test_non_redundant_tree_partly_reasoned():
	"""A > B > C > D plus A > D: D is redundant under A, though C isn't a child of A"""
	g = load("""
	:A a owl:Class .
	:B a owl:Class ; rdfs:subClassOf :A .
	:C a owl:Class ; rdfs:subClassOf :B .
	:D a owl:Class ; rdfs:subClassOf :C, :A .
	""")
	assert tree_qnames(g.ontologyClassTree(non_redundant=True))["h:A"] == ["h:B"]


def test_non_redundant_tree_keeps_multiple_inheritance():
	g = load("""
	:P a owl:Class .
	:Q a owl:Class .
	:X a owl:Class ; rdfs:subClassOf :P, :Q .
	""")
	tree = tree_qnames(g.ontologyClassTree(non_redundant=True))
	assert tree["h:P"] == ["h:X"] and tree["h:Q"] == ["h:X"]


def test_non_redundant_tree_sibling_cycle():
	"""Siblings in a cycle are descendants of each other: neither is dropped"""
	g = load("""
	:A a owl:Class .
	:B a owl:Class ; rdfs:subClassOf :A, :C .
	:C a owl:Class ; rdfs:subClassOf :A, :B .
	""")
	assert tree_qnames(g.ontologyClassTree(non_redundant=True))["h:A"] == ["h:B", "h:C"]


def test_non_redundant_property_tree():
	g = load("""
	:p a owl:ObjectProperty .
	:q a owl:ObjectProperty ; rdfs:subPropertyOf :p .
	:r a owl:ObjectProperty ; rdfs:subPropertyOf :q, :p .
	""")
	assert tree_qnames(g.ontologyPropTree())["h:p"] == ["h:q", "h:r"]
	assert tree_qnames(g.ontologyPropTree(non_redundant=True))["h:p"] == ["h:q"]
