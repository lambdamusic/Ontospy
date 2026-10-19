# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for the local library listing (`ontospy lib`, `gendocs -l`, the shell): the
file names come in alphabetical order ignoring case.

Run like this:

$ pytest ontospy/tests/test_library.py

"""

from ..core import manager


def test_library_sorted_ignoring_case(tmp_path, monkeypatch):
	for name in ["pizza.ttl", "Brick.ttl", "agrovoc.ttl", "FOAF.rdf", "dcat3.ttl", ".hidden", "pizza.ttl.pickle"]:
		(tmp_path / name).write_text("")
	monkeypatch.setattr(manager, "get_home_location", lambda: str(tmp_path))
	assert manager.get_localontologies() == ["agrovoc.ttl", "Brick.ttl", "dcat3.ttl", "FOAF.rdf", "pizza.ttl"]
	assert manager.get_localontologies(pattern="ttl") == ["agrovoc.ttl", "Brick.ttl", "dcat3.ttl", "pizza.ttl"]
