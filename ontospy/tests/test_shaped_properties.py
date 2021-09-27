# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

$ python -m ontospy.tests.test_shaped_properties

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


from .context import TEST_RDF_FOLDER, TEST_SHAPES_FOLDER



# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")

class TestShapedProperties(unittest.TestCase):


	def test_shaped_properties(self):

		"""
		Check if the shapes and their properties on a class are loaded properly.
		"""
		printDebug("=================\nTEST: Loading/merging ALL ontology & shapes from local folder and printing summary.\n .. => %s\n=================" % TEST_RDF_FOLDER, "important")

		o = Ontospy(TEST_RDF_FOLDER, verbose=False)

		for el in o.stats():
			print("%s : %d" % (el[0], el[1]))

		for c in o.all_classes:
			if c.shapedProperties:
				printDebug("Class: %s" % str(c), "green")
				for x in c.shapedProperties:
					print(".....hasProperty: " + str(x["property"]))
					print("     the property has %s associated shapes." % x["shape"])
			else:
				pass
			# print("..... has no target class!")


if __name__ == "__main__":
	unittest.main()
