# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

$ python -m ontospy.tests.test_methods

"""

from __future__ import print_function
import click 

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")



class SampleCustomEntity(ontospy.RDF_Entity):

    def __init__(self, uri, rdftype=None, namespaces=None, ext_model=False):
        super(SampleCustomEntity, self).__init__(uri, rdftype, namespaces, ext_model)

    def __repr__(self):
        return "<SampleCustomEntity *%s*>" % ( self.uri)

    def disjointWith(self):
        """
        Example: pull out disjoint with statements
        """
        pred = "http://www.w3.org/2002/07/owl#disjointWith"
        return self.getValuesForProperty(pred)





class TestMethods(unittest.TestCase):

	# updated 2018-05-08

	dir_path = os.path.dirname(os.path.realpath(__file__))
	DATA_FOLDER = dir_path + "/rdf/"
	f = DATA_FOLDER + "pizza.ttl"
	o = Ontospy(f, verbose=True)

	printDebug("\n*****\nTest: loading with local file... > %s\n*****" % str(f), "important")

	def test1(self):
		"""
		Instances method
		"""
		printDebug("\n=================\nTEST 1: Checking the <instances> method", "green")

		for c in self.o.all_classes:
			# c.describe()
			if c.instances:
				print("CLASS: " + c.uri)
				print("INSTANCES: ")
				for el in c.instances:
					print(el.uri, el.qname)
					print(el.getValuesForProperty("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"))
		
		printDebug("Test completed succesfully.\n", "green")


	def test2(self):
		"""
		getValuesForProperty
		"""
		printDebug("\n=================\nTEST 2: Checking the <getValuesForProperty> method", "green")

		for c in self.o.all_classes[:3]:
			print("CLASS: ")
			print(c.uri, c.qname)
			print("RDF:TYPE VALUES: ")
			print(c.getValuesForProperty("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"))

		printDebug("Test completed succesfully.\n", "green")
	
	def test3(self):
		"""
		build_entity_from_uri
		"""
		printDebug("\n=================\nTEST 3: Checking the <build_entity_from_uri> method", "green")

		e = self.o.build_entity_from_uri("http://www.co-ode.org/ontologies/pizza/pizza.owl#Germany")
		print("URI: ", e)
		print("RDFTYPE: ", e.rdftype)
		print("BEST LABEL: ", e.bestLabel())
		print("RDF SOURCE: ")
		print(e.rdf_source())
		printDebug("Test completed succesfully.\n", "green")


	def test4(self):
		"""
		build_entity_from_uri - SampleCustomEntity
		"""
		printDebug("\n=================\nTEST 4: Checking the <build_entity_from_uri> method using a SampleCustomEntity class ", "green")

		e = self.o.build_entity_from_uri("http://www.co-ode.org/ontologies/pizza/pizza.owl#FruttiDiMare", SampleCustomEntity)
		print("URI: ", e)
		print("RDFTYPE: ", e.rdftype)
		print("BEST LABEL: ", e.bestLabel())
		print("OWL DISJOINT WITH: ")
		print("\n".join([x for x in e.disjointWith()]))
		printDebug("Test completed succesfully.\n", "green")
	
	
	print("Success.\n")



if __name__ == "__main__":
	unittest.main()
