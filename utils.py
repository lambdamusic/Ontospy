#!/usr/bin/env python

# encoding: utf-8

"""
OntosPy Utils

Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.
More info in the __init__.py file.

"""


from rdflib import URIRef, RDFS, RDF, BNode




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





def sort_uri_list_by_name(uri_list):
	""" 
	 Sorts a list of uris based on the last bit (usually the name) of a uri
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
		return sorted(uri_list, key=lambda x: get_last_bit(x.__str__()))
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



