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


# ENDPOINT = "http://dbpedia.org/sparql"
ENDPOINT = "http://192.168.1.64:7200/repositories/scigraph-test"

class TestSparqlStore(unittest.TestCase):


	def test1_load_dbpedia(self):
		"""
		Check if the dbpedia endpoint loads ok
		"http://dbpedia.org/sparql"
		"""
		print("=================\nTEST 1: Loading DBPEDIA <%s> endpoint.\n=================" % ENDPOINT)

		o = Ontospy(sparql=ENDPOINT, verbose=True)

		q = o.sparql("select ?x where {?x a ?b} limit 100")
		if q:
			for el in q:
				print(el)
		else:
			print("No results")

		# print("Success.\n")



if __name__ == "__main__":
	unittest.main()