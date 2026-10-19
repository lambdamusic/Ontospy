# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for how the loader builds its graph: every triple from every source ends up
in the one graph, whatever the RDF format, without rdflib's deprecated ConjunctiveGraph (#7).

Run like this:

$ pytest ontospy/tests/test_loader_graphs.py

"""

import os
import warnings

import pytest
import rdflib

from ..core.rdf_loader import RDFLoader
from .context import TEST_RDF_FOLDER

ONTOSPY_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# rdflib format name => file extension
FORMATS = {
	"turtle": "ttl",
	"xml": "rdf",
	"n3": "n3",
	"nt": "nt",
	"json-ld": "jsonld",
}

# a JSON-LD named graph: a `@graph` with an `@id`. A plain rdflib Graph drops these triples
NAMED_GRAPH_JSONLD = """
{"@context": {"ex": "http://example.org/named#", "owl": "http://www.w3.org/2002/07/owl#"},
 "@id": "http://example.org/named-graph",
 "@graph": [{"@id": "ex:A", "@type": "owl:Class"}, {"@id": "ex:B", "@type": "owl:Class"}]}
"""


def make_graph(name, n=3):
	"""a small graph with its own namespace, so graphs made for different formats share no triples"""
	ns = rdflib.Namespace("http://example.org/%s#" % name.replace("-", ""))
	g = rdflib.Graph()
	for i in range(n):
		g.add((ns["C%d" % i], rdflib.RDF.type, rdflib.OWL.Class))
		g.add((ns["C%d" % i], rdflib.RDFS.label, rdflib.Literal("class %d" % i)))
	return g


def write_sources(tmp_path):
	"""one file per format; returns [(path, expected number of triples)]"""
	sources = []
	for fmt, ext in FORMATS.items():
		g = make_graph(fmt)
		path = tmp_path / ("source.%s" % ext)
		path.write_text(g.serialize(format=fmt), encoding="utf-8")
		sources.append((str(path), len(g)))
	return sources


@pytest.mark.parametrize("fmt", list(FORMATS))
def test_each_format_loads_all_triples(tmp_path, fmt):
	g = make_graph(fmt)
	path = tmp_path / ("source.%s" % FORMATS[fmt])
	path.write_text(g.serialize(format=fmt), encoding="utf-8")
	loaded = RDFLoader().load(str(path))
	assert len(loaded) == len(g)
	assert set(loaded) == set(g)


def test_multiple_files_into_one_graph(tmp_path):
	"""several sources loaded together give the union of their triples"""
	sources = write_sources(tmp_path)
	loader = RDFLoader()
	loaded = loader.load([path for path, _ in sources])
	assert len(loader.sources_valid) == len(sources)
	assert len(loaded) == sum(n for _, n in sources)
	assert isinstance(loaded, rdflib.Graph) and not isinstance(loaded, rdflib.Dataset)


def test_multiple_data_strings_into_one_graph():
	graphs = [make_graph(fmt) for fmt in FORMATS]
	data = [g.serialize(format="turtle") for g in graphs]
	loaded = RDFLoader().load(data=data, rdf_format="turtle")
	assert len(loaded) == sum(len(g) for g in graphs)


def test_jsonld_named_graph_file(tmp_path):
	path = tmp_path / "named.jsonld"
	path.write_text(NAMED_GRAPH_JSONLD, encoding="utf-8")
	loaded = RDFLoader().load([str(path), TEST_RDF_FOLDER + "pizza.ttl"])
	pizza = rdflib.Graph().parse(TEST_RDF_FOLDER + "pizza.ttl", format="turtle")
	assert len(loaded) == len(pizza) + 2
	assert (rdflib.URIRef("http://example.org/named#A"), rdflib.RDF.type, rdflib.OWL.Class) in loaded


def test_jsonld_named_graph_data():
	loaded = RDFLoader().load(data=NAMED_GRAPH_JSONLD, rdf_format="json-ld")
	assert len(loaded) == 2


def test_no_conjunctivegraph_warning_from_ontospy(tmp_path):
	"""rdflib's own parsers may still use ConjunctiveGraph internally, but ontospy shouldn't"""
	path = tmp_path / "named.jsonld"
	path.write_text(NAMED_GRAPH_JSONLD, encoding="utf-8")
	with warnings.catch_warnings(record=True) as caught:
		warnings.simplefilter("always")
		RDFLoader().load([str(path), TEST_RDF_FOLDER + "paper.jsonld"] + [p for p, _ in write_sources(tmp_path)])
		RDFLoader().load(data=NAMED_GRAPH_JSONLD, rdf_format="json-ld")
	ours = [
		w for w in caught
		if "ConjunctiveGraph" in str(w.message) and os.path.realpath(w.filename).startswith(ONTOSPY_DIR)
	]
	assert ours == []
