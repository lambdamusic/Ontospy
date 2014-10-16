#!/usr/bin/env python

# encoding: utf-8

"""
Python Utils

Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""



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



