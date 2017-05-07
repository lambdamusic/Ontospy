# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_sparql

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *



# sanity check
print("-------------------\nOntoSpy ",  VERSION, "\n-------------------")


class TestSparqlStore(unittest.TestCase):


	def test1_load_dbpedia(self):
		"""
		Check if the dbpedia endpoint loads ok
		"http://dbpedia.org/sparql"
		"""
		print("=================\nTEST 1: Loading DBPEDIA <%s> endpoint.\n=================" % "http://dbpedia.org/sparql")

		o = Ontospy(sparql="http://dbpedia.org/sparql", verbose=True)


		print("Success.\n")



if __name__ == "__main__":
	unittest.main()
