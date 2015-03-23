""" Unit test stub for ontosPy	"""

import unittest, os, sys
from ontospy import ontospy
from ontospy.libs.utils import *


DATA_FOLDER = "data/"


# sanity check
print "-------------------\nOntosPy version: ",  ontospy.VERSION, "\n-------------------"


class TestLoadOntologies(unittest.TestCase):
	

	def test1_loading(self):
		""" 
		Check if the ontologies load ok
		"""
		print "\nTEST 1: Loading ontologies from %s folder.\n=================" % DATA_FOLDER
		
		for f in os.listdir(DATA_FOLDER):
			if not f.startswith('.'):
				print "Loading... >", f		
				
				o = ontospy.Ontology(DATA_FOLDER + f)
				
				self.assertEqual(type(o), ontospy.Ontology)
				print "Success."



	def test2_basic_info(self):
		"""
		Check if we can extract basic info
		"""
		print "\nTEST 2: Extracting basic info from each ontology in %s folder.\n=================" % DATA_FOLDER

		for f in os.listdir(DATA_FOLDER):
			if not f.startswith('.'):
				print "Loading... >", f
				
				# divert output to a file temporarily 
				saveout = sys.stdout 
				fsock = open('out.log', 'w')  
				sys.stdout = fsock 
				
				o = ontospy.Ontology(DATA_FOLDER + f)
				printBasicInfo(o)				
				
				sys.stdout = saveout
				fsock.close()
				print "Success."


	def test3_advanced_info(self):
		"""
		Check if we can extract all entities info
		"""
		print "\nTEST 3: Extracting detailed entities info from each ontology in %s folder.\n=================" % DATA_FOLDER

		for f in os.listdir(DATA_FOLDER):
			if not f.startswith('.'):
				print "Loading... >", f

				# divert output to a file temporarily 
				saveout = sys.stdout 
				fsock = open('out.log', 'w')  
				sys.stdout = fsock 
				
				o = ontospy.Ontology(DATA_FOLDER + f)
				printEntitiesInformation(o)				
				
				sys.stdout = saveout
				fsock.close()
				print "Success."
								


if __name__ == "__main__":
	unittest.main()



