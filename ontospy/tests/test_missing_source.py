# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for sources that don't exist or don't parse (backlog #31): the loader says
"File not found" instead of trying every serialization, and gendocs and ser stop instead
of carrying on with an empty graph.

Run like this:

$ pytest ontospy/tests/test_missing_source.py

"""

from click.testing import CliRunner

from .. import Ontospy
from ..cli import main_cli
from ..core.utils import is_missing_file
from .context import TEST_RDF_FOLDER

PIZZA = TEST_RDF_FOLDER + "pizza.ttl"


def test_is_missing_file(tmp_path):
	assert is_missing_file(str(tmp_path / "nope.ttl"))
	assert not is_missing_file(PIZZA)
	assert not is_missing_file(str(tmp_path))  # a folder
	assert not is_missing_file("http://example.org/nope.ttl")
	assert not is_missing_file("file:///nope.ttl")
	assert not is_missing_file("www.example.org/nope.ttl")


def test_loader_says_file_not_found(tmp_path, capsys):
	missing = str(tmp_path / "nope.ttl")
	g = Ontospy(uri_or_path=missing)
	out = capsys.readouterr()
	text = out.out + out.err
	assert g.sources == []
	assert "File not found: <%s>" % missing in text
	assert "Fatal error parsing" not in text


def test_gendocs_missing_file_stops_at_once(tmp_path):
	missing = str(tmp_path / "nope.ttl")
	result = CliRunner().invoke(main_cli, ["gendocs", missing, "-o", str(tmp_path), "--nobrowser"])
	assert result.exit_code == 1, result.output
	assert "File not found: <%s>" % missing in result.output
	assert "Please choose an output format" not in result.output
	assert "Building visualization" not in result.output


def test_gendocs_unparsable_file_stops_before_asking(tmp_path):
	bad = tmp_path / "bad.ttl"
	bad.write_text("this is not RDF {")
	out = tmp_path / "out"
	out.mkdir()
	result = CliRunner().invoke(main_cli, ["gendocs", str(bad), "-o", str(out), "--nobrowser"])
	assert "Nothing to document" in result.output, result.output
	assert "Please choose an output format" not in result.output
	assert "Building visualization" not in result.output
	assert list(out.iterdir()) == []


def test_gendocs_still_asks_for_a_format(tmp_path):
	result = CliRunner().invoke(main_cli, ["gendocs", PIZZA, "-o", str(tmp_path), "--nobrowser"], input="1\n")
	assert result.exit_code == 0, result.output
	assert "Please choose an output format" in result.output
	assert (tmp_path / "index.html").exists()


def test_ser_missing_file_fails(tmp_path):
	missing = str(tmp_path / "nope.ttl")
	result = CliRunner().invoke(main_cli, ["ser", missing])
	assert result.exit_code == 1, result.output
	assert "File not found" in result.output
	assert "Serialized" not in result.output
