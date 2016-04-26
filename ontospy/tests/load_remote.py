""" 
Unit test stub for ontosPy	

Run like this: 

:path/to/ontospyProject>python -m ontospy.tests.load_remote

"""

import unittest, os, sys
from .. import *
from .. import ontospy
from ..core.util import *

DATA_FOLDER = ontospy.get_home_location()

BOOTSTRAP_ONTOLOGIES

# sanity check
print "-------------------\nOntoSPy ",  ontospy.VERSION, "\n-------------------"


class TestLoadOntologies(unittest.TestCase):
	

	def test1_loading(self):
		""" 
		Check if the ontologies in BOOTSTRAP list load ok
		"""

		print "\nTEST 1: Loading ontologies from default list.\n================="

		printDebug("--------------")
		printDebug("The following ontologies will be imported:")
		printDebug("--------------")
		count = 0 
		for s in BOOTSTRAP_ONTOLOGIES:
			count += 1
			printDebug(str(count) + " <%s>" % s)

		
		for f in BOOTSTRAP_ONTOLOGIES:
			print "\nLoading... >", f		
							
			o = ontospy.Graph(f)
			
			o.printClassTree()
			for c in o.classes:
				c.describe()

			for p in o.properties:
				p.describe()
			
			# self.assertEqual(type(o), ontospy.Ontology)

			print "Success.\n"





if __name__ == "__main__":
	unittest.main()



