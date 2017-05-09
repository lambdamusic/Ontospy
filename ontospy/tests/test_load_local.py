# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_load_local

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = dir_path + "/rdf/"

# sanity check
print("-------------------\nOntoSpy ",  VERSION, "\n-------------------")


class TestLoadOntologies(unittest.TestCase):


	def test1_load_locally(self):
		"""
		Check if the ontologies in /RDF folder load ok
		"""
		print("=================\nTEST 1: Loading ontologies from <%s> folder and printing detailed entities descriptions.\n=================" % DATA_FOLDER)

		for f in os.listdir(DATA_FOLDER):
			if not f.startswith('.'):
				printDebug("\n*****\nTest: loading local file... > %s\n*****" % str(f), "important")

				o = Ontospy(DATA_FOLDER + f, verbose=True)

				print("CLASS TREE")
				o.printClassTree()
				print("----------")

				for c in o.classes:
					c.describe()

				for p in o.properties:
					p.describe()

				for s in o.skosConcepts:
					s.describe()

				# self.assertEqual(type(o), ontospy.Ontology)

				print("Success.\n")



if __name__ == "__main__":
	unittest.main()
