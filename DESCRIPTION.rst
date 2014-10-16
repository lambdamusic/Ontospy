OntosPy
=======================

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.


Description
------------

Originally, I developed this script in order to get the hang of the Python RDFLib library (note: it was previously called OntoInspector and hosted on BitBucket). RDFLib provides a number of useful primitives for working with RDF graphs; however it lacks an API aimed at interrogating and modifying a graph based on its defined schema - aka the ontology. 

OntosPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic worflow is simple: load an ontology by instantiating the ``Ontology`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

Ps: the library can be used in standalone mode too.




Example
---------------------------------------------------

Import ontospy and instantiate the Ontology object with the FOAF ontology::


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


	In [5]: document = onto.classFind("document")

	In [6]: document
	Out[6]:
	[rdflib.URIRef('http://xmlns.com/foaf/0.1/Document'),
	 rdflib.URIRef('http://xmlns.com/foaf/0.1/PersonalProfileDocument')]

	In [7]: document = document[0]

	In [8]: document
	Out[8]: rdflib.URIRef('http://xmlns.com/foaf/0.1/Document')

	In [9]: onto.classAllSubs(document)
	Out[9]:
	[rdflib.URIRef('http://xmlns.com/foaf/0.1/Image'),
	 rdflib.URIRef('http://xmlns.com/foaf/0.1/PersonalProfileDocument')]

	In [10]: onto.classAllSupers(document)
	Out[10]: []

	In [11]: onto.entityComment(document)
	Out[11]: rdflib.Literal('A document.', language=None, datatype=None)



Sketch.py: bootstrapping a Turtle model
-----------------------------------------
The library includes a little utility called `sketch.py`. 

This is meant to be used from the command line (Tip: make this file executable: chmod +x sketch.py) and essentially loads up an interactive python environment where you can quickly sketch out an RDF model via the Turtle syntax::

	[michele.pasin]@here:~/code/python>sketch.py 
	Good morning. Ready to Turtle away. Type docs() for help.
	In [1]: docs()

	====Sketch v 0.2====

	add()  ==> add statements to the graph
	...........SHORTCUTS:
	...........'class' = owl:Class
	...........'sub' = rdfs:subClassOf
	...........TURTLE SYNTAX:  http://www.w3.org/TR/turtle/

	show() ==> shows the graph. Can take an OPTIONAL argument for the format.
	...........eg one of['xml', 'n3', 'turtle', 'nt', 'pretty-xml', dot']

	clear()	 ==> clears the graph
	...........all triples are removed

	omnigraffle() ==> creates a dot file and opens it with omnigraffle
	...........First you must set Omingraffle as your system default app for dot files!

	quit() ==> exit

	====Have fun!====


	In [2]: add()
	Multi-line input. Enter ### when finished.
	:person a class
	:mike a :person
	:person sub :agent
	:organization sub :agent
	:worksIn rdfs:domain :person
	:worksIn rdfs:range :organization
	:mike :worksIn :DamageInc
	:DamageInc a :organization

	In [3]: show()
	@prefix : <http://this.sketch#> .
	@prefix bibo: <http://purl.org/ontology/bibo/> .
	@prefix foaf: <http://xmlns.com/foaf/0.1/> .
	@prefix npg: <http://ns.nature.com/terms/> .
	@prefix npgg: <http://ns.nature.com/graphs/> .
	@prefix npgx: <http://ns.nature.com/extensions/> .
	@prefix owl: <http://www.w3.org/2002/07/owl#> .
	@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
	@prefix xml: <http://www.w3.org/XML/1998/namespace> .
	@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

	:mike a :person ;
	    :worksIn :DamageInc .

	:worksIn rdfs:domain :person ;
	    rdfs:range :organization .

	:DamageInc a :organization .

	:organization rdfs:subClassOf :agent .

	:person a owl:Class ;
	    rdfs:subClassOf :agent .



	In [4]: show("xml")
	<?xml version="1.0" encoding="UTF-8"?>
	<rdf:RDF
	   xmlns="http://this.sketch#"
	   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
	>
	  <rdf:Description rdf:about="http://this.sketch#mike">
	    <rdf:type rdf:resource="http://this.sketch#person"/>
	    <worksIn rdf:resource="http://this.sketch#DamageInc"/>
	  </rdf:Description>
	  <rdf:Description rdf:about="http://this.sketch#organization">
	    <rdfs:subClassOf rdf:resource="http://this.sketch#agent"/>
	  </rdf:Description>
	  <rdf:Description rdf:about="http://this.sketch#DamageInc">
	    <rdf:type rdf:resource="http://this.sketch#organization"/>
	  </rdf:Description>
	  <rdf:Description rdf:about="http://this.sketch#person">
	    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Class"/>
	    <rdfs:subClassOf rdf:resource="http://this.sketch#agent"/>
	  </rdf:Description>
	  <rdf:Description rdf:about="http://this.sketch#worksIn">
	    <rdfs:domain rdf:resource="http://this.sketch#person"/>
	    <rdfs:range rdf:resource="http://this.sketch#organization"/>
	  </rdf:Description>
	</rdf:RDF>

	In [5]: omnigraffle()
	### saves a dot file and tries to open it with your default editor
	### if you're on a mac and have omnigraffle - that could be the one!

	In [6]: quit()