# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

$ python -m ontospy.tests.test_sparql

"""

from __future__ import print_function
import time
import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


# sanity check
printDebug(f"-------------------\nOntospy {VERSION}\n-------------------")



class TestSparqlStore(unittest.TestCase):

    ENDPOINT = "http://dbpedia.org/sparql"

    printDebug(f"""\n=================\n
    \nTEST SPARQL: Loading data from remote endpoint.
    \n\n=================""", bg="blue", fg="white")

    time.sleep(3)
    
    def test1_load_dbpedia(self):

        """
        Check if the dbpedia endpoint loads ok
        "http://dbpedia.org/sparql"
        """
        printDebug("\n=================\nTEST: Querying <%s> endpoint...\n=================" % self.ENDPOINT, bg="green")

        o = Ontospy(sparql_endpoint=self.ENDPOINT, verbose=True)

        print(o), print("---------")

        q = o.query("select distinct ?b where {?x a ?b} limit 10")
        if q:
            for el in q:
                print(el)
        else:
            print("No results")



if __name__ == "__main__":
    unittest.main()
