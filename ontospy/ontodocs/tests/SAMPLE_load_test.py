# # !/usr/bin/env python
# #  -*- coding: UTF-8 -*-
# """
# Unit test stub for ontosPy
#
# Run like this:
#
# :path/to/ontospyProject>python -m ontospy.tests.load_test
#
# """
#
# from __future__ import print_function
#
# import unittest, os, sys
# from .. import *
# from ..core.utils import *
#
#
# dir_path = os.path.dirname(os.path.realpath(__file__))
# DATA_FOLDER = dir_path + "/rdf/"
#
# # sanity check
# print("-------------------\nOntoSpy ",  VERSION, "\n-------------------")
#
#
# class TestLoadOntologies(unittest.TestCase):
#
#
# 	def test1_load_locally(self):
# 		"""
# 		Check if the ontologies in /RDF folder load ok
# 		"""
# 		print("\nTEST 1: Loading ontologies from <%s> folder.\n=================" % DATA_FOLDER)
#
# 		for f in os.listdir(DATA_FOLDER):
# 			if not f.startswith('.'):
# 				print("\nLoading... >", f)
#
# 				o = Ontospy(DATA_FOLDER + f)
#
# 				o.printClassTree()
# 				for c in o.classes:
# 					c.describe()
#
# 				for p in o.all_properties:
# 					p.describe()
#
# 				for s in o.all_skos_concepts:
# 					s.describe()
#
# 				# self.assertEqual(type(o), ontospy.Ontology)
#
# 				print("Success.\n")
#
#
#
# 	def test2_load_url(self):
# 		"""
# 		Check if the ontologies in BOOTSTRAP list load ok
# 		"""
# 		MAX = 2
# 		print("\nTEST 2: Loading some sample online ontologies.\n=================")
#
# 		printDebug("--------------")
# 		printDebug("The following ontologies will be loaded from the web:")
# 		printDebug("--------------")
# 		count = 0
# 		for s in BOOTSTRAP_ONTOLOGIES[:MAX]:
# 			count += 1
# 			printDebug(str(count) + " <%s>" % s)
#
#
# 		for f in BOOTSTRAP_ONTOLOGIES[:MAX]:
# 			print("\nLoading... >", f)
#
# 			try:
# 				o = Ontospy(f)
#
# 				o.printClassTree()
# 				for c in o.classes:
# 					c.describe()
#
# 				for p in o.all_properties:
# 					p.describe()
# 			except:
# 				printDebug("An error occured - are you sure this resource is online?")
# 				pass
#
# 			# self.assertEqual(type(o), ontospy.Ontology)
#
# 			print("Success.\n")
#
#
#
# if __name__ == "__main__":
# 	unittest.main()
