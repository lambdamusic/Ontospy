

import ontospy

o = ontospy.Graph("/Users/michele.pasin/Dropbox/Ontologies/NPG/npg-domain-ontology/data/article-types/article-types.ttl")


for x in o.skosConcepts:
	print "-------", x, "-------"
	x.printStats()
	
o.printSkosTree()