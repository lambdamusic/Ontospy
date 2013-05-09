#!/usr/bin/env python
# encoding: utf-8


"""
Based on from http://terse-words.blogspot.co.uk/2012/01/get-real-data-from-semantic-web.html


##################
# 
#  USAGE

python dbpedia.py -q "select * where {?z a owl:Class} LIMIT 100"

or

python dbpedia.py -o

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





class DBpediaEndpoint(SparqlEndpoint):
    
    def __init__(self, prefixes={}, verbose=False):
        endpoint = "http://dbpedia.org/sparql"

        prefixes = {
            "dbpedia-owl": "http://dbpedia.org/ontology/",
            "dbpedia2": "http://dbpedia.org/property/",
            "dbpedia": "http://dbpedia.org/",
            "yago" : "http://dbpedia.org/class/yago/" ,
        }

        super(DBpediaEndpoint, self).__init__(endpoint, prefixes, verbose)





def main():
    # get parameters
    opts, args = parse_options()
    query, format, describe, alltriples, ontology = opts.query, opts.format, opts.describe, opts.alltriples, opts.ontology

    sTime = time.time()

    s = DBpediaEndpoint()

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
        for l in results:
            print l
    elif format == "XML":
        print results.toxml()
    else:
        print results


    # print some stats.... 
    eTime = time.time()
    tTime = eTime - sTime
    print "-" * 10
    print "Time:       %0.2fs" %  tTime
    
    try:
        # most prob this works only with JSON results, but you get the idea!
        print "Found:      %d" % len(results)
        print "Stats:      (%d/s after %0.2fs)" % (
                  int(math.ceil(float(len(results)) / tTime)), tTime)
    except:
        pass

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e




 # OLD TEST QUERY       

    # s = DBpediaEndpoint()
    # resource_uri = "http://dbpedia.org/resource/Foobar"
    
    # results = s.query("""
    #     SELECT ?o
    #     WHERE { <%s> dbpedia-owl:abstract ?o .
    #     FILTER(langMatches(lang(?o), "EN")) }
    # """ % resource_uri, "JSON")


