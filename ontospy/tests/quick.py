# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Test Quick: use this file to quickly run scripts/tests which will then be integrated into proper tests

Running it:

.tools/run-quick-test.sh

TIP

# code to load resources for multiple tests

```
dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = dir_path + "/rdf/"
f = DATA_FOLDER + "pizza.ttl"
o = Ontospy(f, verbose=True)
printDebug("\n*****\nTest: loading local file... > %s\n*****" % str(f), "important")
```

"""

from __future__ import print_function

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


from .context import TEST_RDF_FOLDER, TEST_SHAPES_FOLDER


# sanity check
print("-------------------\nOntospy ", VERSION, "\n-------------------")




class TestQuick(unittest.TestCase):


	def test_quick1(self):
		"""

		"""
		print("=================\n*** QUICK TEST 1 ***\n=================\n")

		f = TEST_RDF_FOLDER + "periodical.jsonld"

		o = Ontospy(f, verbose=True, rdf_format="json-ld")
			



	# def test_quick2(self):
	#     """Keep adding tests like this"""
	#     print("=================\n*** QUICK TEST 1 ***\n=================\n")


if __name__ == "__main__":
	unittest.main()
