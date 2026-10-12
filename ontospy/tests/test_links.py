# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for links in the generated documentation: URLs in the ontology metadata are
shown as links (#61), and rdfs:seeAlso values are shown for classes, properties,
concepts and individuals (#65).

Run like this:

$ pytest ontospy/tests/test_links.py

"""

import os

import pytest

from .. import Ontospy
from ..gendocs.actions import build_visualization
from ..gendocs.CONFIG import VISUALIZATIONS_LIST
from ..gendocs.jinja_env import url_test

LINKS_TTL = """
@prefix ex: <http://example.org/links#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://example.org/links> a owl:Ontology ;
    dct:creator <http://creator.example.org/> ;
    dct:publisher "http://publisher.example.org/" ;
    dct:contributor "mailto:someone@example.org" ;
    dct:description "A test ontology, see http://example.org for more" ;
    rdfs:seeAlso <http://docs.example.org/onto> .

ex:Animal a owl:Class ;
    rdfs:seeAlso <http://docs.example.org/animal>, "Some book about animals" .
ex:hasName a owl:DatatypeProperty ; rdfs:domain ex:Animal ;
    rdfs:seeAlso <http://docs.example.org/hasName> .
ex:Rex a ex:Animal ;
    rdfs:seeAlso <http://docs.example.org/rex> .
ex:Mammals a skos:Concept ; skos:prefLabel "Mammals" ;
    rdfs:seeAlso <http://docs.example.org/mammals> .
"""

VIZ = {v["ID"]: n for n, v in enumerate(VISUALIZATIONS_LIST["Visualizations"])}


@pytest.fixture(scope="module")
def onto():
	return Ontospy(data=LINKS_TTL, rdf_format="turtle", hide_individuals=False)


def build(onto, viz_id, path):
	build_visualization(onto, VIZ[viz_id], path=str(path))
	out = ""
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith((".html", ".md")):
				with open(os.path.join(root, f), encoding="utf-8") as fh:
					out += fh.read()
	return out


def test_url_test():
	assert url_test("http://example.org")
	assert url_test("https://example.org/x?y=1")
	assert url_test("mailto:someone@example.org")
	assert not url_test("A test ontology, see http://example.org for more")
	assert not url_test("example.org")
	assert not url_test("")


def test_see_also(onto):
	animal = onto.get_class(match="Animal")[0]
	assert sorted(str(x) for x in animal.seeAlso()) == ["Some book about animals", "http://docs.example.org/animal"]


@pytest.mark.parametrize("viz_id", ["html-simple", "html-complex"])
def test_html_links(onto, viz_id, tmp_path):
	out = build(onto, viz_id, tmp_path)
	# #61: metadata URLs are links, whether URIs or strings; other text isn't linked
	for url in ["http://creator.example.org/", "http://publisher.example.org/", "mailto:someone@example.org"]:
		assert '<a href="%s"' % url in out, url
	assert '<a href="http://example.org"' not in out
	# #65: See also, for each kind of entity
	assert "See also" in out
	for url in ["animal", "hasName", "rex", "mammals"]:
		assert '<a href="http://docs.example.org/%s"' % url in out, url
	assert "Some book about animals" in out


def test_markdown_links(onto, tmp_path):
	out = build(onto, "markdown", tmp_path)
	# individual and concept pages used to be saved as .ms, so links to them were broken
	assert not [f for f in os.listdir(tmp_path) if f.endswith(".ms")]
	assert "[http://creator.example.org/](http://creator.example.org/)" in out
	assert "[mailto:someone@example.org](mailto:someone@example.org)" in out
	assert "#### See also" in out
	for url in ["animal", "hasName", "rex", "mammals"]:
		assert "(http://docs.example.org/%s)" % url in out, url
	assert "* Some book about animals" in out


def test_d3_metadata_links(onto, tmp_path):
	"""the D3 visualizations share the metadata template"""
	out = build(onto, "d3-dendogram", tmp_path)
	assert '<a href="http://creator.example.org/"' in out
