#!/usr/bin/env python
# ,*, coding: utf,8 ,*,

"""
Summary

the vocabularies used for autocompletion used in turtle prompt

"""


# note: I've added this as text so to avoid problems with relative paths during imports..

rdfsschema = """
# baseURI: http://www.w3.org/2000/01/rdf-schema

# c14n-version: 3
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
rdfs:
  rdf:type owl:Ontology ;
  dc:title "The RDF Schema vocabulary (RDFS)" ;
  rdfs:seeAlso <http://www.w3.org/2000/01/rdf-schema-more> ;
.
rdfs:Class
  rdf:type rdfs:Class ;
  rdfs:comment "The class of classes." ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "Class" ;
  rdfs:subClassOf rdfs:Resource ;
.
rdfs:Container
  rdf:type rdfs:Class ;
  rdfs:comment "The class of RDF containers." ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "Container" ;
  rdfs:subClassOf rdfs:Resource ;
.
rdfs:ContainerMembershipProperty
  rdf:type rdfs:Class ;
  rdfs:comment "The class of container membership properties, rdf:_1, rdf:_2, ...,all of which are sub-properties of :member." ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "ContainerMembershipProperty" ;
  rdfs:subClassOf rdf:Property ;
.
rdfs:Datatype
  rdf:type rdfs:Class ;
  rdfs:comment "The class of RDF datatypes." ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "Datatype" ;
  rdfs:subClassOf rdfs:Class ;
.
rdfs:Literal
  rdf:type rdfs:Class ;
  rdfs:comment "The class of literal values, eg. textual strings and integers." ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "Literal" ;
  rdfs:subClassOf rdfs:Resource ;
.
rdfs:Resource
  rdf:type rdfs:Class ;
  rdfs:comment "The class resource, everything." ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "Resource" ;
.
rdfs:comment
  rdf:type rdf:Property ;
  rdfs:comment "A description of the subject resource." ;
  rdfs:domain rdfs:Resource ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "comment" ;
  rdfs:range rdfs:Literal ;
.
rdfs:domain
  rdf:type rdf:Property ;
  rdfs:comment "A domain of the subject property." ;
  rdfs:domain rdf:Property ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "domain" ;
  rdfs:range rdfs:Class ;
.
rdfs:isDefinedBy
  rdf:type rdf:Property ;
  rdfs:comment "The defininition of the subject resource." ;
  rdfs:domain rdfs:Resource ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "isDefinedBy" ;
  rdfs:range rdfs:Resource ;
  rdfs:subPropertyOf rdfs:seeAlso ;
.
rdfs:label
  rdf:type rdf:Property ;
  rdfs:comment "A human-readable name for the subject." ;
  rdfs:domain rdfs:Resource ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "label" ;
  rdfs:range rdfs:Literal ;
.
rdfs:member
  rdf:type rdf:Property ;
  rdfs:comment "A member of the subject resource." ;
  rdfs:domain rdfs:Resource ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "member" ;
  rdfs:range rdfs:Resource ;
.
rdfs:range
  rdf:type rdf:Property ;
  rdfs:comment "A range of the subject property." ;
  rdfs:domain rdf:Property ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "range" ;
  rdfs:range rdfs:Class ;
.
rdfs:seeAlso
  rdf:type rdf:Property ;
  rdfs:comment "Further information about the subject resource." ;
  rdfs:domain rdfs:Resource ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "seeAlso" ;
  rdfs:range rdfs:Resource ;
.
rdfs:subClassOf
  rdf:type rdf:Property ;
  rdfs:comment "The subject is a subclass of a class." ;
  rdfs:domain rdfs:Class ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "subClassOf" ;
  rdfs:range rdfs:Class ;
.
rdfs:subPropertyOf
  rdf:type rdf:Property ;
  rdfs:comment "The subject is a subproperty of a property." ;
  rdfs:domain rdf:Property ;
  rdfs:isDefinedBy rdfs: ;
  rdfs:label "subPropertyOf" ;
  rdfs:range rdf:Property ;
.



"""

rdfschema = [
    ("rdf:Property", "the class of properties"),
    ("rdf:Statement",
     "the class of statements: rdf:Statement, rdf:subject, rdf:predicate, rdf:object are used for reification"),
    ("rdf:type", "an instance of rdf:Property used to state that a resource is an instance of a class"),
    ("rdf:subject", " the subject of the subject RDF statement"),
    ("rdf:predicate", " the predicate of the subject RDF statement"),
    ("rdf:object", " the object of the subject RDF statement"),
]


# taken from https://github.com/RDFLib/OWL-RL/blob/master/RDFClosure/OWL.py

owlschema = [
    ("owl:annotatedSource", ""),
    ("owl:annotatedTarget", ""),
    ("owl:annotatedProperty", ""),
    ("owl:allValuesFrom", ""),
    ("owl:assertionProperty", ""),
    ("owl:backwardCompatibleWith", ""),
    ("owl:cardinality", ""),
    ("owl:complementOf", ""),
    ("owl:BottomDataProperty", ""),
    ("owl:BottomObjectProperty", ""),
    ("owl:datatypeComplementOf", ""),
    ("owl:deprecated", ""),
    ("owl:differentFrom", ""),
    ("owl:disjointUnionOf", ""),
    ("owl:disjointClasses", ""),
    ("owl:disjointWith", ""),
    ("owl:distinctMembers", ""),
    ("owl:equivalentClass", ""),
    ("owl:equivalentProperty", ""),
    ("owl:hasKey", ""),
    ("owl:hasValue", ""),
    ("owl:hasSelf", ""),
    ("owl:imports", ""),
    ("owl:incompatibleWith", ""),
    ("owl:intersectionOf", ""),
    ("owl:inverseOf", ""),
    ("owl:maxCardinality", ""),
    ("owl:maxQualifiedCardinality", ""),
    ("owl:members", ""),
    ("owl:minCardinality", ""),
    ("owl:minQualifiedCardinality", ""),
    ("owl:onClass", ""),
    ("owl:onDataRange", ""),
    ("owl:onDatatype", ""),
    ("owl:oneOf", ""),
    ("owl:onProperty", ""),
    ("owl:onProperties", ""),
    ("owl:predicate", ""),
    ("owl:priorVersion", ""),
    ("owl:propertyChainAxiom", ""),
    ("owl:propertyDisjointWith", ""),
    ("owl:qualifiedCardinality", ""),
    ("owl:sameAs", ""),
    ("owl:someValuesFrom", ""),
    ("owl:sourceIndividual", ""),
    ("owl:subject", ""),
    ("owl:targetIndividual", ""),
    ("owl:targetValue", ""),
    ("owl:TopDataProperty", ""),
    ("owl:TopObjectProperty", ""),
    ("owl:unionOf", ""),
    ("owl:versionInfo", ""),
    ("owl:versionIRI", ""),
    ("owl:withRestrictions", ""),
    
    ("owl:AllDisjointProperties", ""),
    ("owl:AllDifferent", ""),
    ("owl:AllDisjointClasses", ""),
    ("owl:Annotation", ""),
    ("owl:AnnotationProperty", ""),
    ("owl:AsymmetricProperty", ""),
    ("owl:Axiom", ""),
    ("owl:Class", ""),
    ("owl:DataRange", ""),
    ("owl:DatatypeProperty", ""),
    ("owl:DeprecatedClass", ""),
    ("owl:DeprecatedProperty", ""),
    ("owl:FunctionalProperty", ""),
    ("owl:InverseFunctionalProperty", ""),
    ("owl:IrreflexiveProperty", ""),
    ("owl:NamedIndividual", ""),
    ("owl:NegativePropertyAssertion", ""),
    ("owl:Nothing", ""),
    ("owl:ObjectProperty", ""),
    ("owl:Ontology", ""),
    ("owl:OntologyProperty", ""),
    ("owl:ReflexiveProperty", ""),
    ("owl:Restriction", ""),
    ("owl:Thing", ""),
    ("owl:SelfRestriction", ""),
    ("owl:SymmetricProperty", ""),
    ("owl:TransitiveProperty", ""),
]

