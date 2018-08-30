# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_shaped_properties

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *



# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")

class TestShapedProperties(unittest.TestCase):


	dir_path = os.path.dirname(os.path.realpath(__file__))
	DATA_FOLDER = dir_path + "/rdf/schema/webapi.ttl"


	def test_shaped_properties(self):

		"""
		Check if the shapes and their properties on a class are loaded properly.
		"""
		printDebug("=================\nTEST: Loading ontology & shapes from <%s> folder and printing summary.\n=================" % self.DATA_FOLDER, "important")

		o = Ontospy(self.DATA_FOLDER, verbose=False)

		for el in o.stats():
			print("%s : %d" % (el[0], el[1]))

		for c in o.all_classes:
			printDebug("\Class: %s" % str(c), "green")
			if c.shapedProperties:
				for x in c.shapedProperties:
					print(".....hasProperty: " + str(x["property"]))
					print("     the property has %s associated shapes." % x["shape"])
			else:
				print("..... has no target class!")


if __name__ == "__main__":
	unittest.main()
