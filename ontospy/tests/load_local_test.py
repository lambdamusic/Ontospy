# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.load_local_test

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import manager
from ..shared.utils import *


DATA_FOLDER = manager.get_home_location()


# sanity check
print("-------------------\nOntoSpy ",  VERSION, "\n-------------------")


class TestLoadOntologies(unittest.TestCase):


	def test1_loading(self):
		"""
		Check if the ontologies load ok (from local repo)
		"""
		print("\nTEST 1: Loading ontologies from %s folder.\n=================" % DATA_FOLDER)

		for f in os.listdir(DATA_FOLDER):
			if not f.startswith('.'):
				print("\nLoading... >", f)

				o = Ontospy(DATA_FOLDER + f)

				o.printClassTree()
				for c in o.classes:
					c.describe()

				for p in o.properties:
					p.describe()

				# self.assertEqual(type(o), ontospy.Ontology)

				print("Success.\n")





if __name__ == "__main__":
	unittest.main()
