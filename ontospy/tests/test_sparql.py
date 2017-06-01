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


ENDPOINT = "http://dbpedia.org/sparql"
# ENDPOINT = "http://192.168.1.64:7200/repositories/scigraph-test"

class TestSparqlStore(unittest.TestCase):


    def test1_load_dbpedia(self):

        """
        Check if the dbpedia endpoint loads ok
        "http://dbpedia.org/sparql"
        """
        printDebug("=================\nTEST: Loading <%s> endpoint.\n=================" % ENDPOINT, "important")

        o = Ontospy(sparql_endpoint=ENDPOINT, verbose=True)

        print(o), print("---------")

        q = o.query("select distinct ?b where {?x a ?b} limit 10")
        if q:
            for el in q:
                print(el)
        else:
            print("No results")



if __name__ == "__main__":
    unittest.main()
