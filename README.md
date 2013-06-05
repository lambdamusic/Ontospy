OntosPy
=======

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.

#### Version: 
1.1


####Dependencies:
- RDFlib <http://www.rdflib.net/> (tested on versions 2.4 and 3.0).



Description
=======

Originally, I developed this script in order to get the hang of the Python RDFLib library (note: it was previously called OntoInspector and hosted on BitBucket). RDFLib provides a number of useful primitives for working with RDF graphs; however it lacks an API aimed at interrogating and modifying a graph based on its defined schema - aka the ontology. 

OntosPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic worflow is simple: load an ontology by instantiating the ``Ontology`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

Ps: the library can be used in standalone mode too.




Changelog
=======

2013-06-02
- refactored, fixed a few bugs

2013-05-31
- added methods for properties

2013-05-27
- fixed ontoTree so to include OWL.Thing
- added alpha sorting to __buildClassTree
- split ontologyURI() and ontologyPrettyURI
- modified __ontologyURI so to include DC.identifier metadata
- updated ontologyAnnotations method: now multiple annotations are returned correctly
- added ontologyPhysicalLocation property

2013-05-24
- addded propertyRepresentation method
- fixed <classAllSupers> and <classAllSubs>: added wrapper so to preserve tree order
- added classRangeFor and classDomainFor; classProperties is now more generic;
- changed entityComment and entityLabel to pull out all results by default
- supers and subs methods: added parameter for sorting so to preserve tree order
- changed ontologyURI method to private; ignoring blank nodes now
- added the public -ontologyClassTree- property (previously called __classTree)
- added the FAMOUS ONTOLOGIES variables for loading stuff more easily
	eg: o = ontospy.Ontology(ontospy.FAMOUS_ONTOLOGIES.FRBR)


2013-05-09
- changed the default verbose option 


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

