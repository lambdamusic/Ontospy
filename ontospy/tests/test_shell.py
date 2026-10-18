# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for the shell's printouts: domains and ranges inherited from superproperties
are shown, marked "(inferred)", instead of owl:Thing (#15, follow-up to #126).

The shell is interactive, so the printing methods are called directly, with the
ontology from test_domain_range.py as the current graph.

Run like this:

$ pytest ontospy/tests/test_shell.py

"""

import io
import re
import contextlib

import pytest

from .. import Ontospy
from ..shell.shell_lib import Shell
from .test_domain_range import ONTO, NS

ANSI = re.compile(r"\x1b\[[0-9;]*m")


@pytest.fixture(scope="module")
def g():
	return Ontospy(data=ONTO, rdf_format="turtle", verbose=False)


@pytest.fixture
def shell():
	# skip __init__: it creates the local ontology repo in the home folder
	return Shell.__new__(Shell)


def output(shell, entity, kind, method, *args):
	"""Run a printing method on <entity> and return what it printed, without colours"""
	shell.currentEntity = {'name': entity.uri, 'object': entity, 'type': kind}
	buf = io.StringIO()
	with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
		getattr(shell, method)(*args)
	return [ANSI.sub("", l).strip() for l in buf.getvalue().splitlines()]


def usage(g, shell, name):
	p = g.get_property(uri=NS + name)
	return output(shell, p, "property", "_printPropertyDomainRange", False)


def test_property_usage_inherited(g, shell):
	lines = usage(g, shell, "hasParent")
	assert lines[1:4] == ["fam:Person (inferred)", "fam:hasParent", "=> fam:Person (inferred)"]
	assert "owl:Thing" not in "\n".join(lines)
	# a datatype range two levels up
	lines = usage(g, shell, "nickname")
	assert lines[1:4] == ["fam:Agent (inferred)", "fam:nickname", "=> xsd:string (inferred)"]


def test_property_usage_declared_unchanged(g, shell):
	assert usage(g, shell, "hasRelative")[1:4] == ["fam:Person", "fam:hasRelative", "=> fam:Person"]
	# own range, inherited domain
	assert usage(g, shell, "hasMother")[1:4] == ["fam:Person (inferred)", "fam:hasMother", "=> fam:Woman"]
	# nothing declared anywhere up the hierarchy
	assert usage(g, shell, "related")[1:4] == ["owl:Thing", "fam:related", "=> owl:Thing"]


def test_class_domain_of(g, shell):
	person = g.get_class(uri=NS + "Person")
	lines = output(shell, person, "class", "_printClassDomain", False)
	assert lines[1:3] == ["[1] Explicitly declared", "fam:Person => fam:hasRelative => fam:Person"]
	assert "fam:hasParent" not in "\n".join(lines)  # inherited usage is opt-in
	lines = output(shell, person, "class", "_printClassDomain", False, True)
	assert "[2] Inferred from superproperties" in lines
	assert "fam:Person => fam:hasParent => fam:Person (inferred)" in lines
	assert "fam:Person => fam:nickname => xsd:string (inferred)" in lines
	assert "fam:Person => fam:related => owl:Thing" in lines


def test_class_range_of(g, shell):
	person = g.get_class(uri=NS + "Person")
	lines = output(shell, person, "class", "_printClassRange", False, True)
	assert "fam:Person => fam:hasRelative => fam:Person" in lines
	assert "fam:Person (inferred) => fam:hasParent => fam:Person" in lines
	assert "owl:Thing => fam:related => fam:Person" in lines
