# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# this allows to load with 'import ontospy', and using 'ontospy.Ontospy'

from .VERSION import __version__, VERSION
from .core.ontospy import Ontospy
from .core.entities import RDF_Entity, Ontology, OntoClass, OntoProperty, OntoSKOSConcept, OntoShape
