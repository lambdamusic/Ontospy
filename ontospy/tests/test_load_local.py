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
from .. core import *
from .. core.utils import *



# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")


class TestLoadOntologies(unittest.TestCase):

	dir_path = os.path.dirname(os.path.realpath(__file__))
	DATA_FOLDER = dir_path + "/rdf/"

	def test1_load_locally(self):
		"""
		Check if the ontologies in /RDF folder load ok
		"""
		print("=================\nTEST 1: Loading ontologies from <%s> folder and printing detailed entities descriptions.\n=================" % self.DATA_FOLDER)

		for f in os.listdir(self.DATA_FOLDER):
			if not f.startswith('.'):
				printDebug("\n*****\nTest: loading local file... > %s\n*****" % str(f), "important")

				o = Ontospy(self.DATA_FOLDER + f, verbose=True)

				print("CLASS TREE")
				o.printClassTree()
				print("----------")

				for c in o.all_classes:
					c.describe()

				for p in o.all_properties:
					p.describe()

				for s in o.all_skos_concepts:
					s.describe()


				print("Success.\n")



if __name__ == "__main__":
	unittest.main()
