#!/usr/bin/env python

# encoding: utf-8

"""
ONTOSPY
Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.
More info in the __init__.py file.

"""



import rdflib	 # so we have it available as a namespace

from rdflib import ConjunctiveGraph, Namespace, exceptions
from rdflib import URIRef, RDFS, RDF, BNode

from utils import *

# CHECK http://stackoverflow.com/questions/65400/how-to-add-method-using-metaclass
# http://www.ibm.com/developerworks/linux/library/l-pymeta/index.html

# 
# >>> class ChattyType(type):
# ...     def __new__(cls, name, bases, dct):
# ...         print "Allocating memory for class", name
# ...         return type.__new__(cls, name, bases, dct)
# ...     def __init__(cls, name, bases, dct):
# ...         print "Init'ing (configuring) class", name
# ...         super(ChattyType, cls).__init__(name, bases, dct)

# 
# >>> class Bar:
# ...     __metaclass__ = ChattyType
# ...     def foomethod(self): print 'foo'



class OntoClass(object):
	"""Class that includes methods for querying an RDFS/OWL classes"""


	def __init__(self, name="", namespace="http://baseuri.com/resource#"):
		"""
		...
		"""
		super(OntoClass, self).__init__()

		self.name = name
		self.namespace = namespace

	def __repr__(self):
		return "<OntoClass object [%d] with uri: %s%s>" % (id(self), self.name, self.namespace)
	
	@classmethod	
	def instanceAddForClass():
		pass

	def all():  # = all instances
		pass

	@classmethod
	def subs():
		pass
	
	@classmethod	
	def supers():
		pass		
		


class OntoProperty(object):
	"""Class that includes methods for querying an RDFS/OWL properties"""


	def __init__(self, namespace, domain=None, range = None):
		"""
		...
		"""
		super(OntoProperty, self).__init__()

		self.namespace = namespace
		self.domain = domain
		self.range = range 

	def __repr__(self):
		return "<OntoProperty object [%d] with namespace: %s>" % (id(self), self.namespace)




	
		
		
class OntoInstance(object):
	"""Class that includes methods for querying an RDFS/OWL instances"""


	def __init__(self, namespace,):
		"""
		...
		"""
		super(OntoInstance, self).__init__()

		self.namespace = namespace

	def __repr__(self):
		return "<OntoInstance object [%d] with namespace: %s>" % (id(self), self.namespace)







