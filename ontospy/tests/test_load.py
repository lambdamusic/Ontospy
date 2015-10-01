""" 
Unit test stub for ontosPy	

Launch with 

python test_simple.py

"""

import unittest, os, sys

from .. import ontospy


DATA_FOLDER = "ontospy/data/schemas/"


# sanity check
print "-------------------\nOntoSPy ",  ontospy.VERSION, "\n-------------------"


class TestLoadOntologies(unittest.TestCase):
	

	def test1_loading(self):
		""" 
		Check if the ontologies load ok
		"""
		print "\nTEST 1: Loading ontologies from %s folder.\n=================" % DATA_FOLDER
		
		for f in os.listdir(DATA_FOLDER):
			if not f.startswith('.'):
				print "\nLoading... >", f		
								
				o = ontospy.Graph(DATA_FOLDER + f)
				
				o.printClassTree()
				for c in o.classes:
					c.describe()

				for p in o.properties:
					p.describe()
				
				# self.assertEqual(type(o), ontospy.Ontology)

				print "Success.\n"





if __name__ == "__main__":
	unittest.main()



