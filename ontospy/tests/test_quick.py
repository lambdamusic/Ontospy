# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Test Quick: use this file to quickly run scripts/tests which will then be integrated into proper tests

Running it:

./run-quick-test.sh

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *

# sanity check
print("-------------------\nOntospy ", VERSION, "\n-------------------")


class MyRDFEntity(ontospy.RDF_Entity):
    def __init__(self, uri, rdftype=None, namespaces=None, ext_model=False):
        super(MyRDFEntity, self).__init__(uri, rdftype, namespaces, ext_model)

    def __repr__(self):
        return "<MyRDFEntity *%s*>" % (self.uri)

    def disjointWith(self):
        """
        Example: pull out disjoint with statements
        """
        pred = "http://www.w3.org/2002/07/owl#disjointWith"
        return self.getValuesForProperty(pred)


class TestQuick(unittest.TestCase):

    # code to load resources for multiple tests

    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # DATA_FOLDER = dir_path + "/rdf/"
    # f = DATA_FOLDER + "pizza.ttl"
    # o = Ontospy(f, verbose=True)
    # printDebug("\n*****\nTest: loading local file... > %s\n*****" % str(f), "important")

    def test_quick1(self):
        """

        """
        print("=================\n*** QUICK TEST 1 ***\n=================\n")

        from ontospy.core.rdf_loader import RDFLoader
        loader = RDFLoader(verbose=True)
        loader.load(uri_or_path="/Users/michele.pasin/Desktop/t.jsonld")
        print(loader.rdflib_graph.serialize(format="turtle"))

    # def test_quick2(self):
    #     """Keep adding tests like this"""
    #     print("=================\n*** QUICK TEST 1 ***\n=================\n")


if __name__ == "__main__":
    unittest.main()
