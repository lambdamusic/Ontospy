""" 
Unit test stub for ontosPy	

Launch with 

python test_endpoints.py

"""

import unittest, os, sys

import ontospy



ENDPOINTS = [
				# "http://uriburner.com/sparql", 
				"http://data.semanticweb.org/sparql", 
				# "http://zbw.eu/beta/sparql/", 
				"http://factforge.net/sparql", 
				"http://sparql.vivo.ufl.edu/"
			]




# sanity check
print "-------------------\nOntosPy version: ",  ontospy.VERSION, "\n-------------------"


class TestLoadEndpoints(unittest.TestCase):
	

	def test1_loading(self):
		""" 
		Check if the sparql endpoints load ok
		"""
		print "\nTEST 1: Loading sample sparql endpoints \n================="
		
		for e in ENDPOINTS: 
			print "\nLoading... >", e

			o = ontospy.SparqlEndpoint(e)
			
			# self.assertEqual(type(o), ontospy.Ontology)
			print "Success.\n"
	


if __name__ == "__main__":
	unittest.main()



