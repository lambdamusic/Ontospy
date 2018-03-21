# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

:path/to/ontospyProject>python -m ontospy.tests.test_load_local

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = dir_path + "/rdf/"

# sanity check
print("-------------------\nOntoSpy ",  VERSION, "\n-------------------")


class TestQuick(unittest.TestCase):


	def test_quick(self):
		"""

		"""
		print("=================\nQUICK TEST **************")

		f = DATA_FOLDER + "pizza.ttl"
		printDebug("\n*****\nTest: loading local file... > %s\n*****" % str(f), "important")

		o = Ontospy(f, verbose=True)

		for c in o.classes:
			c.describe()
			if c.instances:
				for el in c.instances:
					print(el.uri, el.qname)

if __name__ == "__main__":
	unittest.main()
