# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_load_remote

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")


class TestLoadOntologies(unittest.TestCase):


	def test2_load_url(self):
		"""
		Check if the ontologies in BOOTSTRAP list load ok
		"""
		MAX = 1
		print("=================\nTEST 2: Loading some sample online ontologies.\n=================")

		# printDebug("--------------")
		printDebug("The following ontologies will be loaded from the web:")
		printDebug("--------------")
		count = 0
		for s in BOOTSTRAP_ONTOLOGIES[:MAX]:
			count += 1
			printDebug(str(count) + " <%s>" % s)


		for f in BOOTSTRAP_ONTOLOGIES[:MAX]:

			printDebug("\n*****\nTest: loading remote uri... > %s\n*****" % str(f), "important")

			try:
				o = Ontospy(f, verbose=True)

				print("CLASS TREE")
				o.printClassTree()
				print("----------")

			except:
				printDebug("An error occured - are you sure this resource is online?")
				pass

			# self.assertEqual(type(o), ontospy.Ontology)

			print("Success.\n")



if __name__ == "__main__":
	unittest.main()
