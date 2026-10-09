# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
pytest configuration

Tests that load data over the network are marked as `remote`, so they can be skipped, eg in CI:

$ pytest -m "not remote"

Tests in the gitignored `local/` folder are marked as `remote` too.
"""

import pytest

REMOTE_TEST_MODULES = ["test_load_remote", "test_sparql"]


def pytest_collection_modifyitems(items):
	for item in items:
		if item.module.__name__.split(".")[-1] in REMOTE_TEST_MODULES or item.path.parent.name == "local":
			item.add_marker(pytest.mark.remote)
