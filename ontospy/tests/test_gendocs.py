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


def test_html_single_not_too_wide(pizza, tmp_path):
	"""#35: a fixed 3000em width on the class trees made the page ~48,000px wide"""
	build_visualization(pizza, 0, path=str(tmp_path))
	assert "3000em" not in (tmp_path / "index.html").read_text(encoding="utf-8")


RDF_PROPERTY_TTL = """
@prefix ex: <http://example.org/p#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Thing a owl:Class .
ex:plain a rdf:Property ; rdfs:domain ex:Thing ; rdfs:comment "Only an rdf:Property." .
ex:linked a owl:ObjectProperty ; rdfs:domain ex:Thing ; rdfs:range ex:Thing .
"""


def test_html_single_other_properties(tmp_path):
	"""#39: a property typed only rdf:Property had no section in the single page, as
	most of QUDT's; now it has one, under Other Properties, and an A-Z entry"""
	g = Ontospy(data=RDF_PROPERTY_TTL, rdf_format="turtle")
	build_visualization(g, 0, path=str(tmp_path))
	page = (tmp_path / "index.html").read_text(encoding="utf-8")
	assert '<a href="#otherproperties">Other properties</a>' in page
	assert 'Property: <a name="ex:plain"' in page
	assert "Only an rdf:Property." in page
	assert 'Object Property: <a name="ex:linked"' in page
	assert page.count('<a name="ex:linked"') == 1  # not repeated under Other Properties


def test_no_protocol_relative_urls():
	"""#36: the Bootswatch themes imported Google Fonts as //fonts.googleapis.com, which
	fails when the docs are opened from disk (file://)"""
	import glob
	from ..gendocs.actions import ONTODOCS_VIZ_STATIC
	css = glob.glob(os.path.join(ONTODOCS_VIZ_STATIC, "**", "*.css"), recursive=True)
	assert css
	for f in css:
		with open(f, encoding="utf-8") as fh:
			assert 'url("//' not in fh.read(), f


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


D3_VIZS = ["d3-dendogram", "d3-bubble-chart", "d3-pack-hierarchy"]


@pytest.mark.parametrize("viz_id", D3_VIZS)
def test_d3_libraries(pizza, viz_id, tmp_path):
	"""#34: the D3 vizs use d3 v7, bundled, and plain JavaScript for the side panel: no
	jQuery, slideReveal or older d3, and nothing loaded from the network"""
	viz_index = [n for n, v in VIZ_TYPES if v == viz_id][0]
	build_visualization(pizza, viz_index, path=str(tmp_path))
	assert os.listdir(tmp_path / "static" / "libs") == ["d3-v7"]
	assert (tmp_path / "static" / "libs" / "d3-v7" / "d3.v7.min.js").exists()
	out = read_all_output(tmp_path)
	for old in ["jquery", "slideReveal", "d3.v2", "d3-v3", "http://d3js.org"]:
		assert old not in out, old
	assert 'src="static/libs/d3-v7/d3.v7.min.js"' in out


def _panel_data(html):
	import json, re
	return json.loads(re.search(r"var PANEL_DATA = (.*?);\n", html).group(1))


def test_d3_panel_usage_data(pizza, tmp_path):
	"""#26: a class's Usage table (its properties and its superclasses') is built in the
	browser from data written once per page, not as a table per class"""
	from ..gendocs.utils import build_D3panelData
	data = build_D3panelData(pizza)
	topping = pizza.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#SundriedTomatoTopping")
	pizza_topping = pizza.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#PizzaTopping")
	title, ancestors, own = data["classes"][topping.id]
	assert title == topping.title
	assert pizza_topping.id in ancestors
	is_topping_of = [p.id for p in pizza_topping.domain_of]
	assert is_topping_of and set(is_topping_of) <= set(data["classes"][pizza_topping.id][2])
	# the properties with no domain apply to every class, and are listed once
	assert [p.id for p in pizza.all_properties if p.qname == "pizza.owl:hasCountryOfOrigin"][0] in data["thing"]
	# in the page, as JSON
	build_visualization(pizza, [n for n, v in VIZ_TYPES if v == "d3-dendogram"][0], path=str(tmp_path))
	html = (tmp_path / "index.html").read_text(encoding="utf-8")
	assert _panel_data(html)["classes"][str(topping.id)][0] == topping.title
	assert '<div class="usage" data-class="{}">'.format(topping.id) in html


def test_d3_panel_shapes_data(tmp_path):
	"""#26: the SHACL property shapes of a class, and of its superclasses, a group per
	class written once"""
	from .test_shacl_constraints import IMPLICIT_TTL
	from ..gendocs.utils import build_D3panelData
	g = Ontospy(data=IMPLICIT_TTL, rdf_format="turtle")
	data = build_D3panelData(g)
	person = g.get_class(uri="http://example.org/i#Person")
	assert data["shapes"][person.id] == ["i:Person", "i:Agent"]
	name_row = data["shape_groups"]["i:Agent"][0]
	assert name_row[1:4] == ["i:name", "1", "1"]
	assert name_row[0] == g.get_property(uri="http://example.org/i#name").id
	assert name_row[4] == [[None, "xsd:string"]]
	build_visualization(g, [n for n, v in VIZ_TYPES if v == "d3-dendogram"][0], path=str(tmp_path))
	html = (tmp_path / "index.html").read_text(encoding="utf-8")
	assert _panel_data(html)["shape_groups"]["i:Agent"][0][1] == "i:name"


def test_d3_bubble_labels(tmp_path):
	"""#32: in the bubble chart, parents and children are labelled the same way, honouring
	--preflabel/--preflang (pizza's labels are Portuguese, with English qnames)"""
	from ..gendocs.utils import build_D3bubbleChart
	for pref_title in ["qname", "label"]:
		g = Ontospy(TEST_RDF_FOLDER + "pizza.ttl", pref_title=pref_title)
		by_id = {c.id: c for c in g.all_classes}
		names = []
		def walk(nodes):
			for d in nodes:
				names.append((d["name"], by_id[d["objid"]].title))
				walk(d.get("children", []))
		walk(build_D3bubbleChart(0, 99, 1, g.toplayer_classes))
		assert names and all(name == title for name, title in names)


DIAMOND_TTL = """
@prefix : <http://example.org/d#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
:A a owl:Class .
:B a owl:Class .
:C a owl:Class ; rdfs:subClassOf :A, :B .
:D a owl:Class ; rdfs:subClassOf :C .
"""


def test_d3_bubble_no_duplicates():
	"""#21: the bubble chart shows density, so a class with several parents is one bubble,
	not one under each parent (with its subtree repeated too)"""
	from ..gendocs.utils import build_D3bubbleChart
	g = Ontospy(data=DIAMOND_TTL, rdf_format="turtle")
	bubbles = []
	def walk(nodes):  # as drawBubbleChart's flatten(): a bubble per node with no children
		for d in nodes:
			if "children" in d:
				walk(d["children"])
			else:
				bubbles.append(d["qname"])
	walk(build_D3bubbleChart(0, 99, 1, g.toplayer_classes))
	assert sorted(bubbles) == ["d:A", "d:B", "d:C", "d:D"]


def test_viz_numbers(monkeypatch):
	"""#21: a new viz can take a number above 10 (CONFIG.py), so that the numbers of the
	vizs removed in 2.6 still fail with a message rather than picking the new one"""
	from ..gendocs import actions
	vizs = actions.VISUALIZATIONS_LIST + [{"ID": "new-viz", "Title": "New", "Number": 11}]
	monkeypatch.setattr(actions, "VISUALIZATIONS_LIST", vizs)
	assert [actions.viz_number(n) for n in range(len(vizs))] == [1, 2, 3, 4, 5, 6, 11]
	assert actions._viz_index("11") == actions._viz_index("new-viz") == 6
	assert actions._viz_index("7") is None
	assert actions._viz_index("12") is None


def test_html_multi_sidebar(pizza, tmp_path):
	"""#21: html-multi writes the sidebar's entities once, in sidebar.js, rather than in
	every page"""
	import json
	build_visualization(pizza, [n for n, v in VIZ_TYPES if v == "html-complex"][0], path=str(tmp_path))
	js = (tmp_path / "sidebar.js").read_text(encoding="utf-8")
	assert js.startswith("var SIDEBAR = ")
	data = json.loads(js[len("var SIDEBAR = "):].rstrip().rstrip(";"))
	assert len(data["classes"]) == len(pizza.all_classes)
	assert len(data["properties"]) == len(pizza.all_properties)
	assert len(data["individuals"]) == len(pizza.all_individuals)
	veneziana = [c for c in pizza.all_classes if c.qname == "pizza.owl:Veneziana"][0]
	assert [veneziana.id, veneziana.title, veneziana.slug] in data["classes"]
	# a page has the section headers and the script, not the entries
	page = (tmp_path / (veneziana.slug + ".html")).read_text(encoding="utf-8")
	assert page.count('class="second-level"') == 1  # in the script that builds the entries
	assert 'href="entities-tree-classes.html">Classes (' in page
	assert '<script src="sidebar.js"></script>' in page
	assert 'data-thispage="pizza.owl:Veneziana"' in page


def test_html_multi_usage(pizza, tmp_path):
	"""#21: the rows of the class pages' Usage tables are written once, in usage.js; a
	page names the classes whose properties it lists, and builds the rows in the browser"""
	import json
	build_visualization(pizza, [n for n, v in VIZ_TYPES if v == "html-complex"][0], path=str(tmp_path))
	js = (tmp_path / "usage.js").read_text(encoding="utf-8")
	assert js.startswith("var USAGE = ")
	data = json.loads(js[len("var USAGE = "):].rstrip().rstrip(";"))
	topping = pizza.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#SundriedTomatoTopping")
	pizza_topping = pizza.get_class(uri="http://www.co-ode.org/ontologies/pizza/pizza.owl#PizzaTopping")
	title, qname, slug, props = data["groups"][str(pizza_topping.id)]
	assert (title, slug) == (pizza_topping.title, pizza_topping.slug)
	is_topping_of = [p for p in pizza_topping.domain_of if p.qname == "pizza.owl:isToppingOf"][0]
	assert is_topping_of.id in props
	row = data["props"][str(is_topping_of.id)]
	assert row[:4] == [is_topping_of.title, is_topping_of.qname, is_topping_of.slug, "owl:ObjectProperty"]
	assert [r[1] for r in row[5]] == [r.title for r in is_topping_of.ranges]
	# the properties with no domain, under owl:Thing, are a group too
	assert str(pizza.OWLTHING.id) in data["groups"]
	# the page: the groups in order (the class, its ancestors, owl:Thing), no rows
	page = (tmp_path / (topping.slug + ".html")).read_text(encoding="utf-8")
	groups = [k.id for group in topping.domain_of_inferred for k, v in group.items() if v]
	assert pizza_topping.id in groups and groups[-1] == pizza.OWLTHING.id
	assert 'data-groups="{}"'.format(" ".join(map(str, groups))) in page
	assert '<script src="usage.js"></script>' in page
	assert 'custom/js/usage.js"></script>' in page
	assert is_topping_of.slug + ".html" not in page.split('id="usage-table"')[1].split("</table>")[0]
	assert (tmp_path / "static" / "custom" / "js" / "usage.js").exists()


def test_html_multi_one_theme(pizza, tmp_path):
	"""#21: only the chosen Bootswatch theme is copied, not all 14"""
	from ..gendocs.viz.viz_html_multi import KompleteViz
	KompleteViz(pizza, theme="flatly").build(str(tmp_path))
	themes = os.listdir(tmp_path / "static" / "libs" / "bootswatch3_2")
	assert sorted(themes) == ["flatly", "fonts"]
	assert 'bootswatch3_2/flatly/bootstrap.min.css' in (tmp_path / "index.html").read_text(encoding="utf-8")


def test_html_multi_multimodel(pizza, tmp_path):
	"""for the examples site: static files shared by several outputs, sidebar.js and
	usage.js with each"""
	from ..gendocs.viz.viz_html_multi import KompleteVizMultiModel
	v = KompleteVizMultiModel(pizza, static_url="../static/", output_path_static=str(tmp_path / "static"))
	v.build(str(tmp_path / "pizza"))
	assert (tmp_path / "pizza" / "sidebar.js").exists()
	assert (tmp_path / "pizza" / "usage.js").exists()
	assert (tmp_path / "static" / "custom" / "js" / "usage.js").exists()
	assert not (tmp_path / "pizza" / "static").exists()
	assert 'href="../static/libs/bootswatch3_2/' in (tmp_path / "pizza" / "index.html").read_text(encoding="utf-8")


def test_html_multi_statistics_charts(pizza, tmp_path):
	"""the statistics page draws the hierarchy and the density of classes and properties
	as in the D3 vizs, with the basics of each entity for a drawer; d3 is copied with the
	static files"""
	import json, re
	build_visualization(pizza, [n for n, v in VIZ_TYPES if v == "html-complex"][0], path=str(tmp_path))
	page = (tmp_path / "statistics.html").read_text(encoding="utf-8")
	assert "libs/d3-v7/d3.v7.min.js" in page
	assert (tmp_path / "static" / "libs" / "d3-v7" / "d3.v7.min.js").exists()
	assert 'id="chart-pack-classes"' in page and 'id="chart-bubble-properties"' in page
	assert 'id="chart-pack-concepts"' not in page  # pizza has no SKOS concepts
	info = json.loads(re.search(r"var info = (.*);\n", page).group(1))
	veneziana = [c for c in pizza.all_classes if c.qname == "pizza.owl:Veneziana"][0]
	title, qname, slug, description, parents, children = info["classes"][str(veneziana.id)]
	assert (title, qname, slug) == (veneziana.title, veneziana.qname, veneziana.slug)
	assert sorted(parents) == sorted(p.id for p in veneziana.parents())
	assert "toplayerChart" not in page
	# the number of triples, without a chart
	assert "{:,}".format(pizza.triplesCount()) in page and "triplesStats" not in page
