#!/usr/bin/env python
# encoding: utf-8


"""
Based on from http://terse-words.blogspot.co.uk/2012/01/get-real-data-from-semantic-web.html
I just added a few methods for other sparql queries, separate the conversion step from the queryset, and parametrized the format for the results set...



##################
# 
#  USAGE

# python sparqly.py "http://data.nature.com/sparql" -q "SELECT ?t WHERE { ?a a <http://ns.nature.com/terms/Article> . ?a dc:title ?t} LIMIT 10"

# or

# python sparqly.py "http://data.nature.com/sparql" -q "SELECT ?c WHERE { ?c a owl:Class} "  -f "XML"

or

python sparqly.py "http://data.nature.com/sparql" -o

#
##################


"""







import sys
import time
import math
import optparse
import xml.dom.minidom

try:
	from SPARQLWrapper import SPARQLWrapper, JSON, XML, RDF
except:
	print "Error: can't find SPARQLWrapper (==> easy_install SPARQLWrapper)"
	sys.exit()



__version__ = "0.1"
__copyright__ = "CopyRight (C) 2013 by Michele Pasin - based on http://terse-words.blogspot.co.uk/2012/01/get-real-data-from-semantic-web.html"
__license__ = "MIT"
__author__ = "Michele Pasin"
__author_email__ = "michele dot pasin at gmail dot com"

USAGE = "%prog [options] <sparql endpoint url>"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)




 

class SparqlEndpoint(object):

	"""
	Instantiate an object that knows how to run a sparql query. 
	Results default to JSON, and usually have this format 
	('s' is the variable name used in the SPARQL query): 

	In [8]: results   
	Out[8]: 
	{u'head': {u'vars': [u's']},
	 u'results': {u'bindings': [
	   {u's': {u'type': u'uri',
		 u'value': u'http://ns.nature.com/subjects/occupational_toxicity'}},
	   {u's': {u'type': u'uri',
		 u'value': u'http://ns.nature.com/subjects/chemistry_publishing'}},  ... etc....
		]}}

	"""
 
	def __init__(self, endpoint, prefixes={}, verbose=False):
		self.sparql = SPARQLWrapper(endpoint)
		self.prefixes = {

			"dc": "http://purl.org/dc/elements/1.1/"  ,
			"dcterms": "http://purl.org/dc/terms/",
			"foaf": "http://xmlns.com/foaf/0.1/",
			"owl": "http://www.w3.org/2002/07/owl#",
			"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
			"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
			"skos": "http://www.w3.org/2004/02/skos/core#",
			"void": "http://rdfs.org/ns/void#",
			"xsd": "http://www.w3.org/2001/XMLSchema#",
		}
		self.prefixes.update(prefixes)
		self.verbose = verbose
		self.format = ""  # dynamically assigned at query time
		self.endpoint = endpoint  # just for caching it



	def query(self, q, format="", convert=True):
		"""
		Generic SELECT query structure. 'q' is the main body of the query.

		The results passed out are not converted yet: see the 'format' method
		Results could be iterated using the idiom: for l in obj : do_something_with_line(l)

		If convert is False, we return the collection of rdflib instances

		"""
		
		lines = ["PREFIX %s: <%s>" % (k, r) for k, r in self.prefixes.iteritems()]
		lines.extend(q.split("\n"))
		query = "\n".join(lines)

		if self.verbose:
			print query, "\n\n" 

		return self.__doQuery(query, format, convert)		



	def describe(self, uri, format="", convert=True):
		"""
		A simple DESCRIBE query with no 'where' arguments. 'uri' is the resource you want to describe.

		TODO: there are some errors with describe queries, due to the results being sent back
		For the moment we're not using them much.. needs to be tested more.

		"""
		lines = ["PREFIX %s: <%s>" % (k, r) for k, r in self.prefixes.iteritems()]
		if uri.startswith("http://"):
			lines.extend(["DESCRIBE <%s>" % uri])
		else:  # it's a shortened uri 
			lines.extend(["DESCRIBE %s" % uri])
		query = "\n".join(lines)


		if self.verbose:
			print query, "\n\n" 

		return self.__doQuery(query, format, convert)




	def allTriplesForURI(self, resource_uri, format="", convert=True):
		"""
		Get all triples for a URI TODO: expand with union where URI is both predicate and object
		"""

		if resource_uri.startswith("http://"):
			resource_uri = "<%s>" % resource_uri
		else:  # it's a QName
			pass

		lines = ["PREFIX %s: <%s>" % (k, r) for k, r in self.prefixes.iteritems()]
		q =  """
			SELECT *
			WHERE { %s ?pred ?obj . }""" % resource_uri

		lines.extend([q])
		query = "\n".join(lines)


		if self.verbose:
			print query, "\n\n" 


		return self.__doQuery(query, format, convert)	



	def ontology(self, format="", convert=True):
		"""
		Get all entities of type owl:Class
		"""

		lines = ["PREFIX %s: <%s>" % (k, r) for k, r in self.prefixes.iteritems()]
		q =  """
			SELECT *
			WHERE { ?class a owl:Class }"""

		lines.extend([q])
		query = "\n".join(lines)


		if self.verbose:
			print query, "\n\n" 


		return self.__doQuery(query, format, convert)	


	def __getFormat(self, format):
		"""
		Defaults to JSON  [ps: 'RDF' is the native rdflib representation]
		"""
		if format == "XML":
			self.sparql.setReturnFormat(XML)	
			self.format = "XML"
		elif format == "RDF":
			self.sparql.setReturnFormat(RDF)	
			self.format = "RDF"
		else:
			self.sparql.setReturnFormat(JSON)
			self.format = "JSON"


	def __doQuery(self, query, format, convert):
		"""
		Inner method that does the actual query 
		"""
		self.__getFormat(format)
		self.sparql.setQuery(query)
		if convert:
			results = self.sparql.query().convert()
		else:
			results = self.sparql.query()

		return results	













def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=VERSION)

	parser.add_option("-q", "--query",
			action="store", type="string", default="", dest="query",
			help="SPARQL query string")

	parser.add_option("-f", "--format",
			action="store", type="string", default="JSON", dest="format",
			help="Results format: one of JSON, XML")

	parser.add_option("-d", "--describe",
			action="store", type="string", default="", dest="describe",
			help="Describe Query: just pass a URI")

	parser.add_option("-a", "--alltriples",
			action="store", type="string", default="", dest="alltriples",
			help="Get all available triples for a URI")
  
	parser.add_option("-o", "--ontology",
			action="store_true", default=False, dest="ontology",
			help="Get all entities of type owl:Class - aka the ontology")

	opts, args = parser.parse_args()

	if len(args) < 1 and not (opts.query or opts.describe or opts.alltriples or opts.ontology):
		parser.print_help()
		raise SystemExit, 1

	return opts, args





def main():
	# get parameters
	opts, args = parse_options()
	url = args[0]
	query, format, describe, alltriples, ontology = opts.query, opts.format, opts.describe, opts.alltriples, opts.ontology

	sTime = time.time()

	s = SparqlEndpoint(url)

	if query:
		print "Contacting %s ... \nQuery: \"%s\"; Format: %s\n" % (url, query, format)
		results = s.query(query, format)
	elif describe:
		print "Contacting %s ... \nQuery: DESCRIBE %s; Format: %s\n" % (url, describe, format)
		results = s.describe(describe, format)
	elif alltriples:
		print "Contacting %s ... \nQuery: ALL TRIPLES FOR %s; Format: %s\n" % (url, alltriples, format)
		results = s.allTriplesForURI(alltriples, format)
	elif ontology:
		print "Contacting %s ... \nQuery: ONTOLOGY; Format: %s\n" % (url, format)
		results = s.ontology(format)


	if format == "JSON":
		results = results["results"]["bindings"]
		for d in results:
			for k, v in d.iteritems():
				print "[%s] %s=> %s" % (k, v['type'],v['value'])
			print "----"
	elif format == "XML":
		print results.toxml()
	else:
		print results




	# print some stats.... 
	eTime = time.time()
	tTime = eTime - sTime
	print "-" * 10
	print "Time:	   %0.2fs" %  tTime
	
	try:
		# most prob this works only with JSON results, but you get the idea!
		print "Found:	   %d" % len(results)
		print "Stats:	   (%d/s after %0.2fs)" % (
				  int(math.ceil(float(len(results)) / tTime)), tTime)
	except:
		pass

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e





