#!/usr/bin/env python
# encoding: utf-8

##################
#  Thu May 12 15:32:26 BST 2011
#  OWL vocabulary 
#  michelepasin.org
##################


from rdflib import Namespace

OWLNS = Namespace("http://www.w3.org/2002/07/owl#")


AllDifferent = 	OWLNS["AllDifferent"]
allValuesFrom = OWLNS["allValuesFrom"]
AnnotationProperty	= OWLNS["AnnotationProperty"]
cardinality = OWLNS["cardinality"]
Class = OWLNS["Class"]
complementOf = OWLNS["complementOf"]
DataRange = OWLNS["DataRange"]
DatatypeProperty = OWLNS["DatatypeProperty"]
DeprecatedClass = OWLNS["DeprecatedClass"]
DeprecatedProperty = OWLNS["DeprecatedProperty"]
differentFrom = OWLNS["differentFrom"]
disjointWith = OWLNS["disjointWith"]
distinctMembers = OWLNS["distinctMembers"]
equivalentClass = OWLNS["equivalentClass"]
equivalentProperty = OWLNS["equivalentProperty"]
FunctionalProperty = OWLNS["FunctionalProperty"]
hasValue = OWLNS["hasValue"]
imports = OWLNS["imports"]
incompatibleWith = OWLNS["incompatibleWith"]
intersectionOf = OWLNS["intersectionOf"]
InverseFunctionalProperty = OWLNS["InverseFunctionalProperty"]
inverseOf = OWLNS["inverseOf"]
maxCardinality = OWLNS["maxCardinality"]
minCardinality = OWLNS["minCardinality"]
Nothing = OWLNS["Nothing"]
ObjectProperty = OWLNS["ObjectProperty"]
oneOf = OWLNS["oneOf"]
onProperty = OWLNS["onProperty"]
Ontology = OWLNS["Ontology"]
OntologyProperty = OWLNS["OntologyProperty"]
priorVersion = OWLNS["priorVersion"]
Restriction = OWLNS["Restriction"]
sameAs = OWLNS["sameAs"]
someValuesFrom = OWLNS["someValuesFrom"]
Thing = OWLNS["Thing"]
TransitiveProperty = OWLNS["TransitiveProperty"]
unionOf = OWLNS["unionOf"]
versionInfo = OWLNS["versionInfo"]