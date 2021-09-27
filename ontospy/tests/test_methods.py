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



from .context import TEST_RDF_FOLDER, TEST_SHAPES_FOLDER



# sanity check
print("-------------------\nOntospy ",  VERSION, "\n-------------------")




class SampleCustomEntity(ontospy.RdfEntity):

    def __init__(self, uri, rdftype=None, namespaces=None, ext_model=False, pref_title="qname", pref_lang="en"):
        super(SampleCustomEntity, self).__init__(uri, rdftype, namespaces, ext_model, pref_title, pref_lang)

    def __repr__(self):
        return "<SampleCustomEntity *%s*>" % ( self.uri)

    def disjointWith(self):
        """
        Example: pull out disjoint with statements
        """
        pred = "http://www.w3.org/2002/07/owl#disjointWith"
        return self.getValuesForProperty(pred)





class TestMethods(unittest.TestCase):

	# load sample ontologies

	f = TEST_RDF_FOLDER + "pizza.ttl"
	printDebug("\n*****\n ..loading local ontology > %s\n*****" % str(f), "important")
	o = Ontospy(f, verbose=True, pref_title="label")
	
	f = TEST_RDF_FOLDER + "multilingual.ttl"
	printDebug("\n*****\n ..loading local ontology > %s\n*****" % str(f), "important")
	o2 = Ontospy(f, verbose=True, pref_title="qname", pref_lang="en")


	def test0(self):
		"""
		Class methods
		"""
		printDebug("\n=================\nTEST 0: Checking the <class> displays", "green")

		for c in self.o.all_classes:
			print("URI: ", c.uri)
			print("RDFTYPE: ", c.rdftype)
			print("BEST LABEL: ", c.bestLabel())
			print("TITLE: ", c.title)
			print("===")

		printDebug("Test completed succesfully.\n", "green")


	def test1(self):
		"""
		Instances method
		"""
		printDebug("\n=================\nTEST 1: Checking the <instances> method", "green")

		for c in self.o.all_classes:
			# c.describe()
			if c.instances:
				print("CLASS: " + c.uri + " " + c.title)
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
			print(c.uri, c.qname, c.title)
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
		print("TITLE: ", e.title)
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
		print("TITLE: ", e.title)
		print("OWL DISJOINT WITH: ")
		print("\n".join([x for x in e.disjointWith()]))
		printDebug("Test completed succesfully.\n", "green")



	def test5(self):
		"""
		Pref label and pref language parameters
		"""

		printDebug("\n=================\nTEST 5-1: pref_title=qname / pref_lang=en", "green")
		for c in self.o2.all_classes:
			print("URI: ", c.uri)
			print("RDFTYPE: ", c.rdftype)
			print("BEST LABEL: ", c.bestLabel())
			print("TITLE: ", c.title)
			print("===")

		printDebug("\n=================\nTEST 5-2: pref_title=label / pref_lang=it", "green")
		for c in self.o2.all_classes:
			print("URI: ", c.uri)
			print("RDFTYPE: ", c.rdftype)
			print("BEST LABEL: ", c.bestLabel())
			print("TITLE: ", c.title)
			print("===")

		printDebug("\n=================\nTEST 5-3: pref_title=label / pref_lang=es", "green")
		for c in self.o2.all_classes:
			print("URI: ", c.uri)
			print("RDFTYPE: ", c.rdftype)
			print("BEST LABEL: ", c.bestLabel())
			print("TITLE: ", c.title)
			print("===")

		printDebug("Test completed succesfully.\n", "green")

	
	print("Success.\n")









if __name__ == "__main__":
	unittest.main()
