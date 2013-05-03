OntosPy
=======

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.
Version: 0.1


####Dependencies:
rdflib <http://www.rdflib.net/>
Tested on 2.4 and 3.0


####Credits: 
todo



What?
=======

Originally, I developed this in order to get the hang of the RdfLib library (note: it was previously called OntoInspector).

You can pass an OWL or RDFS ontology to the Ontology class, and it'll give you a bunch of useful information about it. That's all!

The file can be used in standalone mode too.




Changelog
=======


26 March 2013

- added inheritance to spy.classProperties
- improved compare script


25 March 2013 

- changed names of methods.. now all camelcased and more intuitive
- added module to compare two ontologies



Example: loading and querying the foaf ontology
-----------------------


	In [1]: from ontospy import *

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

