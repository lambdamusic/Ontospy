# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

$ python -m ontospy.tests.test_shapes

"""

from __future__ import print_function

import time

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


from .context import TEST_RDF_FOLDER



# sanity check
printDebug(f"-------------------\nOntospy {VERSION}\n-------------------")


class TestShapes(unittest.TestCase):


	printDebug(f"""\n=================\n
	\nTEST SHACL SHAPES: Loading selected ontologies in => {TEST_RDF_FOLDER} 
	\nFor each model shapes description is extracted and printed.
	\n\n=================""", bg="blue", fg="white")

	time.sleep(3)

	candidates = [
		TEST_RDF_FOLDER + "scigraph/" ,
		TEST_RDF_FOLDER + "uco_monolithic.ttl" ,
	]


	def test1_local_shapes(self):

		"""
		Check if the shapes in the SciGraph onto are loaded properly
		"""

		for f in self.candidates:

			printDebug("\n*****\nTest: loading resource... > %s\n*****" % str(f), bg="green")

			o = Ontospy(f, verbose=False)

			for el in o.stats():
				printDebug("%s : %d" % (el[0], el[1]))

			for s in o.all_shapes:
				printDebug("\nSHAPE: %s" % str(s), "green")
				if s.targetClasses:
					for x in s.targetClasses:
						printDebug(".....hasTargetClass: " + str(x))
						printDebug("     Reverse link: the class has %d associated shape." % len(x.all_shapes))
				else:
					printDebug("..... has no target class!")


			for c in o.all_classes:
				if c.shapedProperties:
					printDebug("Class: %s" % str(c), "green")
					for x in c.shapedProperties:
						print(".....hasProperty: " + str(x["property"]))
						print("     the property has %s associated shapes." % x["shape"])
				else:
					pass




if __name__ == "__main__":
	unittest.main()
