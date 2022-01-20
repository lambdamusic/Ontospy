# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_load_remote

"""

from __future__ import print_function

import unittest, os, sys
import time

from .. import *
from ..core import *
from ..core.utils import *


# sanity check
printDebug(f"-------------------\nOntospy {VERSION}\n-------------------")


class TestLoadOntologies(unittest.TestCase):


	def test2_load_url(self):
		"""
		Check if the ontologies in BOOTSTRAP list load ok
		"""
		MAX = 1
		ONTOS = [o for o in BOOTSTRAP_ONTOLOGIES[:MAX]]

		printDebug(f"""\n=================\n
		\nTEST 2: Loading some sample online ontologies => 
		\n {ONTOS} 
		\nFor each model detailed entities descriptions are printed out.
		\n\n=================""", bg="blue", fg="white")

		time.sleep(3)

		for f in BOOTSTRAP_ONTOLOGIES[:MAX]:

			printDebug("\n*****\nTest: loading remote uri... > %s\n*****" % str(f), 	bg="green")

			try:
				o = Ontospy(f, verbose=True)

				print("CLASS TREE")
				o.printClassTree()
				print("----------")

			except:
				printDebug("An error occured - are you sure this resource is online?")
				pass


			print("Success.\n")



if __name__ == "__main__":
	unittest.main()
