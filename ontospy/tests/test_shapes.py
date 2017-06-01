# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_shapes

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *



# sanity check
print("-------------------\nOntoSpy ",  VERSION, "\n-------------------")

dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = dir_path + "/shapes/"


class TestShapes(unittest.TestCase):


	def test1_local_shapes(self):

		"""
		Check if the shapes in the SciGraph onto are loaded properly
		"""
		printDebug("=================\nTEST: Loading ontology & shapes from <%s> folder and printing summary.\n=================" % DATA_FOLDER, "important")

		o = Ontospy(DATA_FOLDER, verbose=False)

		for el in o.stats():
			print("%s : %d" % (el[0], el[1]))

		for s in o.shapes:
			printDebug("\nSHAPE: %s" % str(s), "green")
			if s.targetClasses:
				for x in s.targetClasses:
					print(".....hasTargetClass: " + str(x))
					print("     Reverse link: the class has %d associated shape." % len(x.shapes))
			else:
				print("..... has no target class!")


if __name__ == "__main__":
	unittest.main()
