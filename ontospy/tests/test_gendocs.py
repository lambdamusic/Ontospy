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
from ..gendocs.actions import build_visualization, select_visualization, ask_visualization
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


def test_kept_visualizations():
	"""#25: the six kept, with their --type numbers unchanged"""
	assert [v for _, v in VIZ_TYPES] == ["html-simple", "html-complex", "markdown",
		"d3-dendogram", "d3-bubble-chart", "d3-pack-hierarchy"]


@pytest.mark.parametrize("choice,expected", [("1", 0), ("6", 5), (4, 3), (" 2 ", 1),
	("d3-dendogram", 3), ("markdown", 2)])
def test_select_visualization(choice, expected):
	"""#25: a viz is chosen by its number (from 1) or by its ID"""
	assert select_visualization(choice) == expected


@pytest.mark.parametrize("choice", ["0", "-1", "11", "x", "", "d3-nope"])
def test_select_visualization_invalid(choice, capsys):
	"""#25: 0 and -1 used to pick the last vizs, by indexing the list from the end"""
	with pytest.raises(SystemExit) as e:
		select_visualization(choice)
	assert e.value.code == 1
	assert "Invalid viz-type option" in capsys.readouterr().err


@pytest.mark.parametrize("choice", ["7", "8", "9", "10", "d3-bar-hierarchy", "sigma-force-directed"])
def test_select_removed_visualization(choice, capsys):
	"""#25: the removed vizs fail with a message saying so, rather than as invalid"""
	with pytest.raises(SystemExit) as e:
		select_visualization(choice)
	assert e.value.code == 1
	assert "was removed in Ontospy 2.6" in capsys.readouterr().err


def test_ask_visualization_rejects_zero(monkeypatch):
	"""#25: the interactive menu had the same bug: 0 picked the last viz"""
	answers = iter(["0", "11", "4"])
	monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
	assert ask_visualization() == 3


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


REASONED_TTL = """
@prefix : <http://example.org/r#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
:Mammal a owl:Class .
:Human a owl:Class ; rdfs:subClassOf :Mammal .
:RedBeardedGuy a owl:Class ; rdfs:subClassOf :Human, :Mammal .
"""


@pytest.mark.parametrize("non_redundant,expected", [(False, 2), (True, 1)])
def test_html_multi_non_redundant_tree(tmp_path, non_redundant, expected):
	"""PR #87: with non_redundant, RedBeardedGuy appears once in the class tree page,
	under Human, and not again under Mammal"""
	g = Ontospy(data=REASONED_TTL, rdf_format="turtle")
	viz_index = [n for n, v in VIZ_TYPES if v == "html-complex"][0]
	build_visualization(g, viz_index, path=str(tmp_path), non_redundant=non_redundant)
	page = (tmp_path / "entities-tree-classes.html").read_text(encoding="utf-8")
	assert page.count('class="treelinks" href="class-rredbeardedguy.html"') == expected


CYCLE_TTL = """
@prefix : <http://example.org/c#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
:Top a owl:Class .
:A a owl:Class ; rdfs:subClassOf :Top, :B .
:B a owl:Class ; rdfs:subClassOf :A .
"""


@pytest.mark.parametrize("viz_index,viz_id", VIZ_TYPES, ids=[v for _, v in VIZ_TYPES])
def test_build_with_cycle(viz_index, viz_id, tmp_path):
	"""#142: a subclass cycle below a top-level class (A > B > A) used to make the
	html-complex tree pages recurse forever"""
	g = Ontospy(data=CYCLE_TTL, rdf_format="turtle")
	assert build_visualization(g, viz_index, path=str(tmp_path))
	if viz_id == "html-complex":
		page = (tmp_path / "entities-tree-classes.html").read_text(encoding="utf-8")
		# Top > A > B > A: A is shown again under B, but not expanded a second time
		assert page.count('class="treelinks" href="class-ca.html"') == 2
		assert page.count('class="treelinks" href="class-cb.html"') == 1


ONTO_METADATA_TTL = """
@prefix : <http://example.org/m#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
<http://example.org/m> a owl:Ontology ;
    rdfs:label "Metadata test" ;
    dcterms:title "Metadata test" ;
    dcterms:creator [ foaf:name "Ada Lovelace" ; foaf:homepage <http://example.org/ada> ] ,
                    [ foaf:name "Alan Turing" ] ;
    owl:versionInfo "1.0" .
:Thing a owl:Class .
"""


def test_ontology_metadata():
	"""#23: the ontology's own properties, sorted, each once; blank nodes nested, not flattened"""
	g = Ontospy(data=ONTO_METADATA_TTL, rdf_format="turtle")
	meta = g.all_ontologies[0].metadata()
	assert [prop for prop, _ in meta] == ["dcterms:creator", "dcterms:title", "owl:versionInfo", "rdf:type", "rdfs:label"]
	creators = dict(meta)["dcterms:creator"]
	names = sorted(str(dict(c["properties"])["foaf:name"][0]) for c in creators)
	assert names == ["Ada Lovelace", "Alan Turing"]


@pytest.mark.parametrize("viz_id", ["html-complex", "html-simple", "markdown", "d3-dendogram"])
def test_ontology_metadata_rendered(viz_id, tmp_path):
	"""each property shown once, in order; no blank-node ids, nested values shown"""
	g = Ontospy(data=ONTO_METADATA_TTL, rdf_format="turtle")
	viz_index = [n for n, v in VIZ_TYPES if v == viz_id][0]
	build_visualization(g, viz_index, path=str(tmp_path))
	out = read_all_output(tmp_path)
	assert "Ada Lovelace" in out and "Alan Turing" in out
	# the metadata entries, not eg the Turtle source some pages show too
	entry = "* {}" if viz_id == "markdown" else "<dt>{}</dt>"
	assert out.count(entry.format("dcterms:creator")) == 1
	assert (out.index(entry.format("dcterms:creator")) < out.index(entry.format("owl:versionInfo"))
		< out.index(entry.format("rdfs:label")))
	import re
	assert not re.search(r"\bn[0-9a-f]{32}b\d+\b", out), "a blank-node id is shown"
