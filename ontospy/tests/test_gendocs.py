# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for gendocs: build every visualization type for an ontology with individuals.

Run like this:

$ pytest ontospy/tests/test_gendocs.py

"""

import os

import pytest

from .. import Ontospy
from ..gendocs.actions import build_visualization
from ..gendocs.CONFIG import VISUALIZATIONS_LIST
from .context import TEST_RDF_FOLDER

VIZ_TYPES = [(n, v["ID"]) for n, v in enumerate(VISUALIZATIONS_LIST["Visualizations"])]

# viz ID => (module in ontospy.gendocs.viz, class), as in gendocs.actions.build_visualization
VIZ_CLASSES = {
	"html-simple": ("viz_html_single", "HTMLVisualizer"),
	"html-complex": ("viz_html_multi", "KompleteViz"),
	"markdown": ("viz_markdown", "MarkdownViz"),
	"d3-dendogram": ("viz_d3dendogram", "Dataviz"),
	"d3-bubble-chart": ("viz_d3bubble_chart", "Dataviz"),
	"d3-pack-hierarchy": ("viz_d3pack_hierarchy", "Dataviz"),
	"d3-bar-hierarchy": ("viz_d3bar_hierarchy", "Dataviz"),
	"d3-partition-table": ("viz_d3partition_table", "Dataviz"),
	"d3-rotating-cluster": ("viz_d3rotating_cluster", "Dataviz"),
	"sigma-force-directed": ("viz_sigmajs", "Dataviz"),
}


@pytest.fixture(scope="module")
def pizza():
	"""pizza.ttl has individuals, eg pizza:Italy, an instance of pizza:Country"""
	g = Ontospy(TEST_RDF_FOLDER + "pizza.ttl", hide_individuals=False)
	assert g.all_individuals
	return g


def read_all_output(path):
	out = ""
	for root, dirs, files in os.walk(path):
		for f in files:
			if f.endswith((".html", ".md")):
				with open(os.path.join(root, f), encoding="utf-8") as fh:
					out += fh.read()
	return out


@pytest.mark.parametrize("viz_index,viz_id", VIZ_TYPES, ids=[v for _, v in VIZ_TYPES])
def test_build_with_individuals(pizza, viz_index, viz_id, tmp_path):
	"""issue #145: building docs with individuals used to fail with
	TypeError: 'method' object is not iterable"""
	url = build_visualization(pizza, viz_index, path=str(tmp_path))
	assert url
	assert "Italy" in read_all_output(tmp_path)


def test_html_multi_individual_pages(pizza, tmp_path):
	"""issue #134: the multi page html had no pages for individuals (the build crashed before writing them)"""
	build_visualization(pizza, 1, path=str(tmp_path))
	for x in pizza.all_individuals:
		assert (tmp_path / (x.slug + ".html")).exists()


EDGE_CASES_TTL = """
@prefix : <http://example.org/edge#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
:Thing a owl:Class .
:Range1 a owl:Class .
:Range2 a owl:Class .
:multiLine a owl:ObjectProperty ; rdfs:domain :Thing ; rdfs:range :Range1 ;
    rdfs:comment \"\"\"First line.
Second line.\"\"\" .
:withPipe a owl:ObjectProperty ; rdfs:domain :Thing ; rdfs:range :Range1 ;
    rdfs:comment "Either A | B" .
:twoRanges a owl:ObjectProperty ; rdfs:domain :Thing ; rdfs:range :Range1, :Range2 .
"""


def test_markdown_property_table_rows(tmp_path):
	"""the markdown class pages list properties in a table (#137): each row must stay
	on one line and have exactly 3 columns, whatever is in the descriptions"""
	g = Ontospy(data=EDGE_CASES_TTL, rdf_format="turtle")
	viz_index = [n for n, v in VIZ_TYPES if v == "markdown"][0]
	build_visualization(g, viz_index, path=str(tmp_path))
	page = (tmp_path / "class-edgething.md").read_text(encoding="utf-8")
	rows = [l for l in page.split("\n") if l.startswith("| [")]
	assert len(rows) == 3
	for row in rows:
		# 4 unescaped | delimit 3 columns
		assert row.replace("\\|", "").count("|") == 4, row
	assert "First line. Second line." in page
	assert "Either A \\| B" in page
	assert "class-edgerange2.md), [" in page or "class-edgerange1.md), [" in page


@pytest.mark.parametrize("viz_index,viz_id", VIZ_TYPES, ids=[v for _, v in VIZ_TYPES])
def test_custom_jinja2env(pizza, viz_index, viz_id, tmp_path):
	"""#138: every visualization uses the Jinja2 environment it's given, so users can
	override templates; here every template is replaced with a marker"""
	from jinja2 import Environment, FunctionLoader
	from ..gendocs.jinja_env import add_default_filters

	env = Environment(loader=FunctionLoader(lambda name: "CUSTOM TEMPLATE " + name))
	add_default_filters(env)
	viz_module, viz_class = VIZ_CLASSES[viz_id]
	cls = getattr(__import__("ontospy.gendocs.viz." + viz_module, fromlist=[viz_class]), viz_class)
	v = cls(pizza, "title", jinja2env=env)
	assert v.jinja2env is env
	v.build(str(tmp_path))
	assert "CUSTOM TEMPLATE" in read_all_output(tmp_path)


def test_custom_jinja2env_multimodel(pizza, tmp_path):
	"""the multi-ontology html used by scripts/export_all.py takes a jinja2env too"""
	from ..gendocs.jinja_env import get_default_env
	from ..gendocs.viz.viz_html_multi import KompleteVizMultiModel

	env = get_default_env()
	v = KompleteVizMultiModel(pizza, jinja2env=env, static_url="../static/",
		output_path_static=str(tmp_path / "static"))
	assert v.jinja2env is env


def test_individual_instance_of(pizza):
	italy = [x for x in pizza.all_individuals if x.qname.endswith("Italy")][0]
	assert [c.qname for c in italy.instance_of()] == ["pizza.owl:Country"]
