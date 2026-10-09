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


def test_individual_instance_of(pizza):
	italy = [x for x in pizza.all_individuals if x.qname.endswith("Italy")][0]
	assert [c.qname for c in italy.instance_of()] == ["pizza.owl:Country"]
