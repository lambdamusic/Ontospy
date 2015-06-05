OntoSPy
=======================

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.


Description
------------

OntoSPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic workflow is simple: load an ontology by instantiating the ``Ontology`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

For more up to date documentation, please visit https://github.com/lambdamusic/OntoSPy


Example
---------------------------------------------------

Import ontoSPy and instantiate the Ontology object with the FOAF ontology::


	In [1]: from ontospy.ontospy import *

	In [2]: onto = Ontology("http://xmlns.com/foaf/spec/20100809.rdf")

	In [3]: onto.toplayer
	Out[3]:
	[rdflib.URIRef('http://xmlns.com/foaf/0.1/Agent'),
	 rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#Class'),
	 rdflib.URIRef('http://www.w3.org/2004/02/skos/core#Concept'),
	 rdflib.URIRef('http://xmlns.com/foaf/0.1/Document'),
	 rdflib.URIRef('http://xmlns.com/foaf/0.1/LabelProperty'),
	 rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#Literal'),
	 rdflib.URIRef('http://www.w3.org/2000/10/swap/pim/contact#Person'),
	 rdflib.URIRef('http://xmlns.com/foaf/0.1/Project'),
	 rdflib.URIRef('http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing'),
	 rdflib.URIRef('http://www.w3.org/2002/07/owl#Thing')]

	In [4]: onto.printClassTree()
	foaf:Agent
	----foaf:Group
	----foaf:Organization
	----foaf:Person
	rdfs:Class
	http://www.w3.org/2004/02/skos/core#Concept
	foaf:Document
	----foaf:Image
	----foaf:PersonalProfileDocument
	foaf:LabelProperty
	rdfs:Literal
	http://www.w3.org/2000/10/swap/pim/contact#Person
	----foaf:Person
	foaf:Project
	http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing
	----foaf:Person
	owl:Thing
	----foaf:OnlineAccount
	--------foaf:OnlineChatAccount
	--------foaf:OnlineEcommerceAccount
	--------foaf:OnlineGamingAccount


