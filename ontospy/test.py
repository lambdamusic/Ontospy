#!/usr/bin/env python
# encoding: utf-8

# script used in development for testing

import ontospy
import rdflib



g = ontospy.Graph("data/schemas/cidoc_crm_v5.1-draft-2014March.rdfs")

c = g.getClass("E31_Document")[0]

print c

for x in c.ancestors():
	print x

print "*" * 10

for x in c.ancestors(noduplicates=False):
	print x