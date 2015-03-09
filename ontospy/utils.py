#!/usr/bin/env python

# encoding: utf-8

"""
Python and RDF Utils for ontospy

Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""


from rdflib import RDFS, RDF, BNode
import rdflib
from vocabs import OWL, DUBLINCORE as DC
DEFAULT_LANGUAGE = "en"



# ===========
# rdf utils
# ===========



def isBlankNode(aClass):
	""" small utility that checks if a class is a blank node """
	if type(aClass) == BNode:
		return True
	else:
		return False



def sortByNamespacePrefix(urisList, nsList):
	"""
		Given an ordered list of namespaces prefixes, order a list of uris based on that. 
		Eg 
		
		In [7]: ll
		Out[7]: 
		[rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
		 rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
		 rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
		 rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')]

		In [8]: sortByNamespacePrefix(ll, [OWL.OWLNS, RDFS])
		Out[8]: 
		[rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'),
		 rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
		 rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
		 rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')]
		 
	"""
	exit = []
	urisList = sort_uri_list_by_name(urisList)
	for ns in nsList:
		innerexit = []
		for uri in urisList:
			if str(uri).startswith(str(ns)):
				innerexit += [uri]
		exit += innerexit

	# add remaining uris (if any)
	for uri in urisList:
		if uri not in exit:
			exit += [uri]
						
	return exit





def sort_uri_list_by_name(uri_list, bypassNamespace=False):
	""" 
	 Sorts a list of uris 
	 
	 bypassNamespace: 
		based on the last bit (usually the name after the namespace) of a uri
		It checks whether the last bit is specified using a # or just a /, eg:
			 rdflib.URIRef('http://purl.org/ontology/mo/Vinyl'),
			 rdflib.URIRef('http://purl.org/vocab/frbr/core#Work')

	 """
	def get_last_bit(uri_string):
		try:
			x = uri_string.split("#")[1]
		except:
			x = uri_string.split("/")[-1]
		return x

	try:
		if bypassNamespace:
			return sorted(uri_list, key=lambda x: get_last_bit(x.__str__()))
		else:
			return sorted(uri_list)
	except:
		# TODO: do more testing.. maybe use a unicode-safe method instead of __str__
		print "Error in <sort_uri_list_by_name>: possibly a UnicodeEncodeError"
		return uri_list







def guess_fileformat(aUri):
	"""
	Simple file format guessing (using rdflib format types) based on the suffix

	see rdflib.parse [https://rdflib.readthedocs.org/en/latest/using_graphs.html]

	"""
	if aUri.endswith(".xml"):
		return "xml"
	elif aUri.endswith(".nt"):
		return "nt"
	elif aUri.endswith(".n3") or aUri.endswith(".ttl"):
		return "n3"
	elif aUri.endswith(".trix"):
		return "trix"
	elif aUri.endswith(".rdfa"):
		return "rdfa"
	else:  # defaults to XML
		return "xml"




def inferNamespacePrefix(aUri):
	""" 
	From a URI returns the last bit and simulates a namespace prefix when rendering the ontology.

	eg from <'http://www.w3.org/2008/05/skos#'> it returns the 'skos' string 
	"""
	stringa = aUri.__str__()
	try:
		prefix = stringa.replace("#", "").split("/")[-1]
	except:
		prefix = ""
	return prefix



def splitNameFromNamespace(aUri):
	""" 
	From a URI returns a tuple (namespace, uri-last-bit)

	Eg
	from <'http://www.w3.org/2008/05/skos#something'> 
		==> ('something', 'http://www.w3.org/2008/05/skos')
	from <'http://www.w3.org/2003/01/geo/wgs84_pos'> we extract
		==> ('wgs84_pos', 'http://www.w3.org/2003/01/geo/')

	"""
	stringa = aUri.__str__()
	try:
		ns = stringa.split("#")[0]
		name = stringa.split("#")[1]
	except:
		ns = stringa.rsplit("/", 1)[0]
		name = stringa.rsplit("/", 1)[1]
	return (name, ns)





def isBlankNode(aClass):
	""" small utility that checks if a class is a blank node """
	if type(aClass) == BNode:
		return True
	else:
		return False




def uri2niceString(aUri, namespaces = None):
	""" 
	From a URI, returns a nice string representation that uses also the namespace symbols
	Cuts the uri of the namespace, and replaces it with its shortcut (for base, attempts to infer it or leaves it blank)

	Namespaces are a list 
	
	[('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
	('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
	(u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
	('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
	('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
	(u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))]
	
	2015-03-09: if a uri has no local component (eg 'bibo:') it's returned in full. 
	
	"""
	if not namespaces:
		namespaces = []
		
	if type(aUri) == rdflib.term.URIRef:	
		# we have a URI: try to create a qName
		stringa = aUri.toPython()  
		for aNamespaceTuple in namespaces:
			try: # check if it matches the available NS
				prefix = aNamespaceTuple[0]
				fulluri = aNamespaceTuple[1].__str__()
			
			
				if stringa.find(fulluri) == 0:
					if len(fulluri) == len(stringa):
						#if the namespace has no local component, dont' shorten it (eg avoid things like 'bibo:')
						stringa = fulluri  
					elif prefix: # for base NS, it's empty
						stringa = prefix + ":" + stringa[len(fulluri):]
					else:
						new_prefix = inferNamespacePrefix(aNamespaceTuple[1])
						if new_prefix:
							stringa = new_prefix + ":" + stringa[len(fulluri):]
						else:
							stringa = "base:" + stringa[len(fulluri):]
			except:
				stringa = "error"
				
	elif type(aUri) == rdflib.term.Literal:
		stringa = "\"%s\"" % aUri  # no string casting so to prevent encoding errors
	else:
		if type(aUri) == type(u''):
			stringa = aUri
		else:
			stringa = aUri.toPython()			
	return stringa




def OLD_uri2niceString(aUri, namespaces = None):
	""" 
	From a URI, returns a nice string representation that uses also the namespace symbols
	Cuts the uri of the namespace, and replaces it with its shortcut (for base, attempts to infer it or leaves it blank)

	Namespaces are a list 
	
	[('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
	('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
	(u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
	('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
	('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
	(u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))]
	
	"""
	if not namespaces:
		namespaces = []
		
	if type(aUri) == rdflib.term.URIRef:	
		# we have a URI: try to create a qName
		stringa = aUri.toPython()  
		for aNamespaceTuple in namespaces:
			try: # check if it matches the available NS
				if stringa.find(aNamespaceTuple[1].__str__()) == 0:
					if aNamespaceTuple[0]: # for base NS, it's empty
						stringa = aNamespaceTuple[0] + ":" + stringa[len(aNamespaceTuple[1].__str__()):]
					else:
						prefix = inferNamespacePrefix(aNamespaceTuple[1])
						if prefix:
							stringa = prefix + ":" + stringa[len(aNamespaceTuple[1].__str__()):]
						else:
							stringa = "base:" + stringa[len(aNamespaceTuple[1].__str__()):]
			except:
				stringa = "error"
				
	elif type(aUri) == rdflib.term.Literal:
		stringa = "\"%s\"" % aUri  # no string casting so to prevent encoding errors
	else:
		if type(aUri) == type(u''):
			stringa = aUri
		else:
			stringa = aUri.toPython()			
	return stringa
	
	
	
	

def niceString2uri(aUriString, namespaces = None):
	""" 
	From a string representing a URI possibly with the namespace qname, returns a URI instance. 
	
	gold:Citation  ==> rdflib.term.URIRef(u'http://purl.org/linguistics/gold/Citation')
	
	Namespaces are a list 
	
	[('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
	('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
	(u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
	('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
	('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
	(u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))]
	
	"""
	
	if not namespaces:
		namespaces = []
	
	for aNamespaceTuple in namespaces:
		if aNamespaceTuple[0] and aUriString.find(aNamespaceTuple[0].__str__() + ":") == 0:
			aUriString_name = aUriString.split(":")[1]
			return rdflib.term.URIRef(aNamespaceTuple[1] + aUriString_name)

	# we dont handle the 'base' URI case 
	return rdflib.term.URIRef(aUriString)
	
	
	
	
	
	
		

###########

# GENERIC METHODS FOR ANY RDF RESOURCE (ENTITIES) FROM AN RDF GRAPH

###########


def entityTriples(rdfGraph, anEntity, excludeProps=False, excludeBNodes = False, orderProps=[RDF, RDFS, OWL.OWLNS, DC.DCNS]):
	"""		
	Returns the pred-obj for any given resource, excluding selected ones..
	
	Sorting: by default results are sorted alphabetically and according to namespaces: [RDF, RDFS, OWL.OWLNS, DC.DCNS]
	"""
	temp = []
	if not excludeProps:
		excludeProps = []
	
	# extract predicate/object
	for x,y,z in rdfGraph.triples((anEntity, None, None)):
		if excludeBNodes and isBlankNode(z):
			continue
		if y not in excludeProps:
			temp += [(y, z)]

	# sorting
	if type(orderProps) == type([]):
		orderedUris = sortByNamespacePrefix([y for y,z in temp], orderProps) # order props only
		orderedUris = [(n+1, x) for n, x in enumerate(orderedUris)]	 # create form: [(1, 'something'),(2,'bobby'),(3,'suzy'),(4,'crab')]
		rank = dict((key, rank) for (rank, key) in orderedUris) # create dict to pass to sorted procedure
		temp = sorted(temp, key=lambda tup: rank.get(tup[0]))
	elif orderProps:  # default to alpha sorting unless False
		temp = sorted(temp, key=lambda tup: tup[0])

	# if niceURI:
	#	temp = [(uri2niceString(ontology, y), z) for y,z in temp]

	return temp




def entityLabel(rdfGraph, anEntity, language = DEFAULT_LANGUAGE, getall = True):
	"""		
	Returns the rdfs.label value of an entity (class or property), if existing. 
	Defaults to DEFAULT_LANGUAGE. Returns the RDF.Literal resource

	Args:
	language: 'en', 'it' etc.. 
	getall: returns a list of all labels rather than a string 

	"""

	if getall: 
		temp = []
		for o in rdfGraph.objects(anEntity, RDFS.label):
			temp += [o]
		return temp
	else:
		for o in rdfGraph.objects(anEntity, RDFS.label):
			if getattr(o, 'language') and  getattr(o, 'language') == language:
				return o
		return ""




def entityComment(rdfGraph, anEntity, language = DEFAULT_LANGUAGE, getall = True):
	"""		
	Returns the rdfs.comment value of an entity (class or property), if existing. 
	Defaults to DEFAULT_LANGUAGE. Returns the RDF.Literal resource

	Args:
	language: 'en', 'it' etc.. 
	getall: returns a list of all labels rather than a string 

	"""

	if getall: 
		temp = []
		for o in rdfGraph.objects(anEntity, RDFS.comment):
			temp += [o]
		return temp
	else:
		for o in rdfGraph.objects(anEntity, RDFS.comment):
			if getattr(o, 'language') and  getattr(o, 'language') == language:
				return o
		return ""








# ===========
# generic python utils
# ===========




def remove_duplicates(seq, idfun=None):
	""" removes duplicates from a list, order preserving, as found in
	http://www.peterbe.com/plog/uniqifiers-benchmark
	"""
	if seq:
		if idfun is None:
			def idfun(x): return x
		seen = {}
		result = []
		for item in seq:
			marker = idfun(item)
			# in old Python versions:
			# if seen.has_key(marker)
			# but in new ones:
			if marker in seen: continue
			seen[marker] = 1
			result.append(item)
		return result
	else:
		return []






def printDebug(s):
	try:
		print s
	except: 
		pass





def pprinttable(rows):
	"""
	Pretty prints a table via python
	http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables

	Example

	>>> from collections import namedtuple
	>>> Row = namedtuple('Row',['first','second','third'])
	>>> data = Row(1,2,3)
	>>> data
	Row(first=1, second=2, third=3)
	>>> pprinttable([data])
	 first = 1
	second = 2
	 third = 3
	>>> pprinttable([data,data])
	first | second | third
	------+--------+------
		1 |		 2 |	 3
		1 |		 2 |	 3

	"""
	if len(rows) > 1:
		headers = rows[0]._fields
		lens = []
		for i in range(len(rows[0])):
			lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
		formats = []
		hformats = []
		for i in range(len(rows[0])):
			if isinstance(rows[0][i], int):
				formats.append("%%%dd" % lens[i])
			else:
				formats.append("%%-%ds" % lens[i])
			hformats.append("%%-%ds" % lens[i])
		pattern = " | ".join(formats)
		hpattern = " | ".join(hformats)
		separator = "-+-".join(['-' * n for n in lens])
		print hpattern % tuple(headers)
		print separator
		for line in rows:
			print pattern % tuple(line)
	elif len(rows) == 1:
		row = rows[0]
		hwidth = len(max(row._fields,key=lambda x: len(x)))
		for i in range(len(row)):
			print "%*s = %s" % (hwidth,row._fields[i],row[i])



