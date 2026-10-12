# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for how gendocs treats the output folder (#60, #62): files already there are
kept unless `empty_folder` / `--emptyfolder` is used, and files left over from earlier
builds are reported.

Run like this:

$ pytest ontospy/tests/test_output_folder.py

"""

import os

from click.testing import CliRunner

from .. import Ontospy
from ..cli import main_cli
from ..gendocs.viz.viz_html_single import HTMLVisualizer
from ..gendocs.viz.viz_html_multi import KompleteViz

TWO_CLASSES = """
@prefix ex: <http://example.org/ex#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Animal a owl:Class .
ex:Plant a owl:Class .
"""

ONE_CLASS = """
@prefix ex: <http://example.org/ex#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
ex:Animal a owl:Class .
"""


def onto(ttl):
	return Ontospy(data=ttl, rdf_format="turtle")


def make_user_files(folder):
	"""a folder that already has the user's own files, a subfolder and a hidden file"""
	folder.mkdir(exist_ok=True)
	(folder / "my-notes.txt").write_text("important")
	(folder / "subfolder").mkdir()
	(folder / "subfolder" / "other.txt").write_text("x")
	(folder / ".DS_Store").write_text("")


def test_existing_files_are_kept(tmp_path):
	make_user_files(tmp_path)
	v = HTMLVisualizer(onto(TWO_CLASSES))
	v.build(str(tmp_path))
	assert (tmp_path / "my-notes.txt").read_text() == "important"
	assert (tmp_path / "subfolder" / "other.txt").exists()
	assert (tmp_path / "index.html").exists()


def test_existing_files_are_reported(tmp_path):
	make_user_files(tmp_path)
	v = HTMLVisualizer(onto(TWO_CLASSES))
	v.build(str(tmp_path))
	leftovers = sorted(os.path.relpath(x, tmp_path) for x in v.leftover_files)
	# hidden files are ignored
	assert leftovers == ["my-notes.txt", os.path.join("subfolder", "other.txt")]


def test_rebuild_reports_nothing(tmp_path):
	"""regenerating the same docs into the same folder is the normal case: no warning"""
	KompleteViz(onto(TWO_CLASSES)).build(str(tmp_path))
	v = KompleteViz(onto(TWO_CLASSES))
	v.build(str(tmp_path))
	assert v.leftover_files == []


def test_stale_pages_are_reported(tmp_path):
	"""a class removed from the ontology leaves its old page behind: that gets reported"""
	KompleteViz(onto(TWO_CLASSES)).build(str(tmp_path))
	plant_page = [f for f in os.listdir(tmp_path) if "plant" in f.lower()]
	assert plant_page
	v = KompleteViz(onto(ONE_CLASS))
	v.build(str(tmp_path))
	assert [os.path.basename(x) for x in v.leftover_files] == plant_page


def test_empty_folder(tmp_path):
	folder = tmp_path / "docs"
	make_user_files(folder)
	inode = os.stat(folder).st_ino
	v = HTMLVisualizer(onto(TWO_CLASSES))
	v.build(str(folder), empty_folder=True)
	# the folder itself is kept (eg a mounted volume, #62), its old contents are gone
	assert os.stat(folder).st_ino == inode
	assert sorted(os.listdir(folder)) == ["index.html", "static"]
	assert v.leftover_files == []


def test_cli_keeps_files_by_default(tmp_path):
	source = tmp_path / "onto.ttl"
	source.write_text(TWO_CLASSES)
	out = tmp_path / "out"
	make_user_files(out)
	result = CliRunner().invoke(main_cli, ["gendocs", str(source), "-o", str(out), "--type", "1", "--nobrowser"])
	assert result.exit_code == 0, result.output
	assert (out / "my-notes.txt").exists()
	assert (out / "index.html").exists()
	assert "not written by this build" in result.output


def test_cli_emptyfolder(tmp_path):
	source = tmp_path / "onto.ttl"
	source.write_text(TWO_CLASSES)
	out = tmp_path / "out"
	make_user_files(out)
	result = CliRunner().invoke(main_cli, ["gendocs", str(source), "-o", str(out), "--type", "1", "--nobrowser", "--emptyfolder"])
	assert result.exit_code == 0, result.output
	assert not (out / "my-notes.txt").exists()
	assert (out / "index.html").exists()
	assert "not written by this build" not in result.output
