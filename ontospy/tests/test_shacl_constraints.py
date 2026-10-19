# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for the SHACL constraints shown in the docs (ontospy/core/shacl_helper.py)

Run like this:

$ pytest ontospy/tests/test_shacl_constraints.py

"""

from .. import Ontospy
from ..gendocs.actions import build_visualization
from ..gendocs.CONFIG import VISUALIZATIONS_LIST


HTML_MULTI = [n for n, v in enumerate(VISUALIZATIONS_LIST["Visualizations"]) if v["ID"] == "html-complex"][0]
HTML_SINGLE = [n for n, v in enumerate(VISUALIZATIONS_LIST["Visualizations"]) if v["ID"] == "html-simple"][0]
MARKDOWN = [n for n, v in enumerate(VISUALIZATIONS_LIST["Visualizations"]) if v["ID"] == "markdown"][0]


# classes that are node shapes themselves (implicit class targets), with blank-node
# property shapes, as in SPDX or Brick
IMPLICIT_TTL = """
@prefix i: <http://example.org/i#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
i:Agent a owl:Class, sh:NodeShape ;
    sh:property [ sh:path i:name ; sh:datatype xsd:string ; sh:minCount 1 ; sh:maxCount 1 ] .
i:Person a owl:Class, sh:NodeShape ;
    rdfs:subClassOf i:Agent ;
    sh:property [ sh:path i:status ; sh:in ( i:alive i:dead i:unknown ) ; sh:maxCount 1 ] ,
        [ sh:path i:age ; sh:or ( [ sh:datatype xsd:integer ] [ sh:datatype xsd:decimal ] ) ;
          sh:message "an age is a number" ; sh:severity sh:Warning ] .
i:name a owl:DatatypeProperty ; rdfs:comment "The name." .
i:age a owl:DatatypeProperty .
i:status a owl:ObjectProperty .
"""

# named property shapes, and shapes whose target class is defined elsewhere, as in DCAT-AP
NAMED_TTL = """
@prefix n: <http://example.org/n#> .
@prefix ex: <http://example.org/other#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
n:DatasetShape a sh:NodeShape ;
    sh:targetClass ex:Dataset ;
    sh:closed true ;
    sh:property n:DatasetShape-title, n:DatasetShape-creatorName .
n:DatasetShape-title a sh:PropertyShape ; sh:path ex:title ; sh:name "title" ;
    sh:description "A name given to the dataset." ; sh:nodeKind sh:Literal ; sh:minCount 1 .
n:DatasetShape-creatorName sh:path ( ex:creator ex:name ) ; sh:datatype xsd:string .
"""


def _constraint(constraints, qname):
	return [c for c in constraints if not c.header and c.property_obj.qname == qname][0]


def test_implicit_class_targets():
	"""a class that is also a sh:NodeShape is the shape's target (SHACL 2.1.3.3)"""
	g = Ontospy(data=IMPLICIT_TTL, rdf_format="turtle")
	person = g.get_class(uri="http://example.org/i#Person")
	shape = g.get_shapes(uri="http://example.org/i#Person")
	assert person in shape.targetClasses and shape in person.all_shapes
	assert [(kind, t.qname) for kind, t in shape.targets] == [("implicit sh:targetClass", "i:Person")]
	# the class's own constraints, then those inherited from its superclass
	assert [c.header or c.property_obj.qname for c in person.shacl_constraints] == \
		["i:Person", "i:age", "i:status", "i:Agent", "i:name"]
	name = _constraint(person.shacl_constraints, "i:name")
	assert name.sh_minCount == {"1"} and name.sh_maxCount == {"1"}
	assert [t.qname for t in name.value_types] == ["xsd:string"]
	assert name.rdfs_comment == {"The name."}
	assert name.rdftype_qname == {"owl:DatatypeProperty"}


def test_constraint_details():
	"""sh:in keeps the list order; sh:or members are summarised; severity and message"""
	g = Ontospy(data=IMPLICIT_TTL, rdf_format="turtle")
	shape = g.get_shapes(uri="http://example.org/i#Person")
	assert [c.property_obj.qname for c in shape.shacl_constraints] == ["i:age", "i:status"]
	status = _constraint(shape.shacl_constraints, "i:status")
	assert [t.qname for t in status.sh_in] == ["i:alive", "i:dead", "i:unknown"]
	age = _constraint(shape.shacl_constraints, "i:age")
	other = dict(age.other_constraints)
	assert other["sh:or"] == ["xsd:integer", "xsd:decimal"]
	assert [t.qname for t in other["sh:severity"]] == ["sh:Warning"]
	assert age.sh_message == {"an age is a number"}


def test_named_property_shapes_and_external_targets():
	"""property shapes that are named nodes are followed; a target class not defined in
	the graph is still listed, without a page"""
	g = Ontospy(data=NAMED_TTL, rdf_format="turtle")
	assert not g.all_classes
	shape = g.get_shapes(uri="http://example.org/n#DatasetShape")
	assert [(kind, t.qname, t.href) for kind, t in shape.targets] == [("sh:targetClass", "ex:Dataset", None)]
	assert [c.property_obj.qname for c in shape.shacl_constraints] == ["ex:creator / ex:name", "ex:title"]
	title = _constraint(shape.shacl_constraints, "ex:title")
	assert title.sh_name == {"title"} and title.sh_minCount == {"1"}
	assert [t.qname for t in title.value_types] == ["sh:Literal"]
	assert ("sh:closed", ["true"]) in shape.node_constraints
	# a property shape typed as such has a page of its own: its constraints, and who uses it
	title_shape = g.get_shapes(uri="http://example.org/n#DatasetShape-title")
	assert [c.property_obj.qname for c in title_shape.shacl_constraints] == ["ex:title"]
	assert [t.qname for t in title_shape.used_by] == ["n:DatasetShape"]
	assert title_shape.node_constraints == []


def test_no_state_across_graphs():
	"""the entities of a graph loaded before don't leak into the next one's links"""
	Ontospy(data=IMPLICIT_TTL, rdf_format="turtle")
	g = Ontospy(data=NAMED_TTL.replace("ex:Dataset", "<http://example.org/i#Person>"), rdf_format="turtle")
	shape = g.get_shapes(uri="http://example.org/n#DatasetShape")
	assert [t.href for _, t in shape.targets] == [None]


def test_shape_pages_rendered(tmp_path):
	g = Ontospy(data=NAMED_TTL, rdf_format="turtle")
	build_visualization(g, HTML_MULTI, path=str(tmp_path))
	page = (tmp_path / "shape-ndatasetshape.html").read_text(encoding="utf-8")
	assert "Property Constraints (2)" in page
	assert "A name given to the dataset." in page
	assert "ex:creator / ex:name" in page
	assert 'href=".html"' not in page  # no links to pages that don't exist

	g = Ontospy(data=IMPLICIT_TTL, rdf_format="turtle")
	build_visualization(g, HTML_MULTI, path=str(tmp_path / "implicit"))
	page = (tmp_path / "implicit" / "class-iperson.html").read_text(encoding="utf-8")
	assert "Property Shapes" in page
	assert 'href="prop-iname.html"' in page
	assert "&lt;br&gt;" not in page



def test_html_single_shapes(tmp_path):
	"""#37: html-single has a Shapes section, and class sections their constraints, with
	links to anchors in the page; a shape's anchor is prefixed, as i:Person is a class too"""
	import re
	g = Ontospy(data=IMPLICIT_TTL, rdf_format="turtle")
	build_visualization(g, HTML_SINGLE, path=str(tmp_path))
	page = (tmp_path / "index.html").read_text(encoding="utf-8")
	assert '<a href="#shapes">Shapes</a>' in page
	assert 'name="shape-i:Person"' in page and 'name="i:Person"' in page
	assert page.count("SHACL property constraints:") == 2  # i:Agent and i:Person
	assert 'href="#i:name"' in page
	assert "an age is a number" in page
	anchors = set(re.findall(r'name="([^"]+)"', page))
	links = set(re.findall(r'href="#([^"]+)"', page))
	assert links <= anchors | {"a-z", "toc"}, links - anchors


def test_markdown_shapes(tmp_path):
	"""#37: markdown has a page per shape, listed in the index, and class pages their
	constraints; table rows stay on one line with 6 (shape) or 8 (class) columns"""
	# a description over two lines (Turtle's \n escape) and with a |
	ttl = IMPLICIT_TTL.replace('"The name."', '"The name,\\nor | an alias."')
	g = Ontospy(data=ttl, rdf_format="turtle")
	build_visualization(g, MARKDOWN, path=str(tmp_path))
	for shape in g.all_shapes:
		assert (tmp_path / (shape.slug + ".md")).exists()
	assert "#### Shapes (2)" in (tmp_path / "index.md").read_text(encoding="utf-8")
	shape_page = (tmp_path / "shape-iperson.md").read_text(encoding="utf-8")
	class_page = (tmp_path / "class-iperson.md").read_text(encoding="utf-8")
	assert "#### SHACL property constraints" in class_page
	assert "[i:name](prop-iname.md)" in class_page
	assert "The name, or \\| an alias." in class_page
	assert "( `xsd:integer` \\| `xsd:decimal` )" in shape_page
	for page, heading, columns in [(shape_page, "#### Property constraints", 6),
			(class_page, "#### SHACL property constraints", 8)]:
		table = page.split(heading)[1].split("\n\n\n")[0]
		rows = [l for l in table.split("\n") if l.startswith("| ")]
		assert len(rows) >= 3
		for row in rows:
			assert row.replace("\\|", "").count("|") == columns + 1, row
