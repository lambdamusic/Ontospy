#!/usr/bin/env python
# encoding: utf-8


"""
Based on code from http://terse-words.blogspot.co.uk/2012/01/get-real-data-from-semantic-web.html


##################
# 
#  USAGE

python nature.py -q "select * where {?z a npg:Subject}"

or

python nature.py -o

#

##################


"""











from sparqly import *  
 
__version__ = "0.1"
__copyright__ = "CopyRight (C) 2013 by Michele Pasin"
__license__ = "MIT"
__author__ = "Michele Pasin"
__author_email__ = "michele dot pasin at gmail dot com"

USAGE = "%prog [options]"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)





 
class NatureEndpoint(SparqlEndpoint):
	"""
	Specialization for Nature endpoint
	"""
	
	def __init__(self, prefixes={}, verbose=False):
		
		endpoint = "http://data.nature.com/sparql"

		prefixes = {
			"sc": "http://purl.org/science/owl/sciencecommons/" ,
			"npg": "http://ns.nature.com/terms/",
			"npgg": "http://ns.nature.com/graphs/",
			"npgx": "http://ns.nature.com/extensions/",
			"bibo": "http://purl.org/ontology/bibo/",
			"prism": "http://prismstandard.org/namespaces/basic/2.1/",
		}

		super(NatureEndpoint, self).__init__(endpoint, prefixes, verbose)





	def getArticlesForSubject(self, sub_uri):

		"""
		eg 
		s = NatureEndpoint()
		tot = len(s.getArticlesForSubject("rna"))


		Related sparql query: 

		select *
		where {
			?x a npg:Article . 
			?x npg:hasSubject <http://ns.nature.com/subjects/molecular_biology>
		}

			EG SUBJECTS
			http://ns.nature.com/subjects/rnai
			http://ns.nature.com/subjects/developmental_biology
			http://ns.nature.com/subjects/gene_regulation
			http://ns.nature.com/subjects/non_coding_rnas
			http://ns.nature.com/subjects/theoretical_physics

		"""

		if sub_uri.startswith("http://"):
			subject = "<%s>" % sub_uri
		else:
			subject = "<http://ns.nature.com/subjects/%s>" % sub_uri

		results = self.query("""
			SELECT ?article
			WHERE { ?article a npg:Article . ?article npg:hasSubject %s}
		""" % subject)

		return self.convertAndPrune(results)







def main():
	# get parameters
	opts, args = parse_options()
	query, format, describe, alltriples, ontology = opts.query, opts.format, opts.describe, opts.alltriples, opts.ontology

	sTime = time.time()

	s = NatureEndpoint()

	url = s.endpoint

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









