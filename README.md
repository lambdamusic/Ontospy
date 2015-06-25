OntoSPy
=======

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.
https://pypi.python.org/pypi/ontospy


#### Version: 
Check the ``ontospy/_version.py`` file


####Installation:
Manual: download this packages and type ``python setup.py install`` 

Web: get it from the Python Package Index: 
``easy_install ontospy``
or
``pip install ontospy``


####Dependencies:
- <http://www.rdflib.net/> (tested on versions 2.4 and 3.0).



Description
=======

OntosPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic workflow is simple: load a graph instantiating the ``Graph`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

The library can be used in standalone mode too.


Documentation
---------------
http://ontospy.readthedocs.org/en/latest/



Examples
----------

These are some basic examples that should be enough to get you started. More extensive documentation will be made available soon!


####Inspecting an ontology from the command line

You can use the `ontospy` script from a terminal to print out basic info about any RDF model. 

	> ontospy <ontology-uri>

More options are available; use `-h` to list them all:
	
	> ontospy -h


####Loading and querying the FOAF model from Python


	In [1]: from ontospy import ontospy

	In [2]: g = ontospy.Graph("http://xmlns.com/foaf/spec/20100809.rdf")
	----------
	Loaded 631 triples from <http://xmlns.com/foaf/spec/20100809.rdf>
	started scanning...
	----------
	Ontologies found: 1
	Classes found...: 14
	Properties found: 67
	Annotation......: 7
	Datatype........: 26
	Object..........: 34

	In [3]: g.toplayer
	Out[3]: 
	[<Class *http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing*>,
	 <Class *http://xmlns.com/foaf/0.1/Agent*>,
	 <Class *http://xmlns.com/foaf/0.1/Document*>,
	 <Class *http://xmlns.com/foaf/0.1/LabelProperty*>,
	 <Class *http://xmlns.com/foaf/0.1/OnlineAccount*>,
	 <Class *http://xmlns.com/foaf/0.1/Project*>]


	In [4]: g.printClassTree()
	[1]   http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing
	[12]  ----foaf:Person
	[2]   foaf:Agent
	[4]   ----foaf:Group
	[11]  ----foaf:Organization
	[12]  ----foaf:Person
	[3]   foaf:Document
	[5]   ----foaf:Image
	[13]  ----foaf:PersonalProfileDocument
	[6]   foaf:LabelProperty
	[7]   foaf:OnlineAccount
	[8]   ----foaf:OnlineChatAccount
	[9]   ----foaf:OnlineEcommerceAccount
	[10]  ----foaf:OnlineGamingAccount
	[14]  foaf:Project

	In [5]: doc = g.getClass(3)

	In [6]: doc
	Out[6]: <Class *http://xmlns.com/foaf/0.1/Document*>

	In [7]: doc.describe()
	Parents......: 0
	Children.....: 2
	Ancestors....: 0
	Descendants..: 2
	Domain of....: 3
	Range of.....: 12
	Instances....: 0
	http://xmlns.com/foaf/0.1/Document
	=> http://www.w3.org/2000/01/rdf-schema#comment
	.... A document.
	=> http://www.w3.org/2002/07/owl#disjointWith
	.... http://xmlns.com/foaf/0.1/Project
	=> http://www.w3.org/2000/01/rdf-schema#isDefinedBy
	.... http://xmlns.com/foaf/0.1/
	=> http://www.w3.org/2002/07/owl#disjointWith
	.... http://xmlns.com/foaf/0.1/Organization
	=> http://www.w3.org/2000/01/rdf-schema#label
	.... Document
	=> http://www.w3.org/2002/07/owl#equivalentClass
	.... http://schema.org/CreativeWork
	=> http://www.w3.org/2003/06/sw-vocab-status/ns#term_status
	.... stable
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2000/01/rdf-schema#Class
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2002/07/owl#Class

	In [8]: doc.descendants()
	Out[8]: 
	[<Class *http://xmlns.com/foaf/0.1/Image*>,
	 <Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>]


	In [9]: for c in doc.descendants():
	   		     c.describe()
	        
	Parents......: 1
	Children.....: 0
	Ancestors....: 1
	Descendants..: 0
	Domain of....: 2
	Range of.....: 3
	Instances....: 0
	http://xmlns.com/foaf/0.1/Image
	=> http://www.w3.org/2000/01/rdf-schema#comment
	.... An image.
	=> http://www.w3.org/2003/06/sw-vocab-status/ns#term_status
	.... stable
	=> http://www.w3.org/2002/07/owl#equivalentClass
	.... http://schema.org/ImageObject
	=> http://www.w3.org/2000/01/rdf-schema#subClassOf
	.... http://xmlns.com/foaf/0.1/Document
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2002/07/owl#Class
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2000/01/rdf-schema#Class
	=> http://www.w3.org/2000/01/rdf-schema#isDefinedBy
	.... http://xmlns.com/foaf/0.1/
	=> http://www.w3.org/2000/01/rdf-schema#label
	.... Image
	Parents......: 1
	Children.....: 0
	Ancestors....: 1
	Descendants..: 0
	Domain of....: 0
	Range of.....: 0
	Instances....: 0
	http://xmlns.com/foaf/0.1/PersonalProfileDocument
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2002/07/owl#Class
	=> http://www.w3.org/2000/01/rdf-schema#label
	.... PersonalProfileDocument
	=> http://www.w3.org/2000/01/rdf-schema#subClassOf
	.... http://xmlns.com/foaf/0.1/Document
	=> http://www.w3.org/2003/06/sw-vocab-status/ns#term_status
	.... testing
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2000/01/rdf-schema#Class
	=> http://www.w3.org/2000/01/rdf-schema#comment
	.... A personal profile RDF document.



#### Creating a Turtle sketch @check

The library includes a little utility called `sketch.py`. 

This is a (still rather rudimentary) interactive environment aimed at facilitating the initial development of RDF models.

It is meant to be used from the command line (tip: make this file executable: `chmod +x sketch.py`) and requires you to type in RDF statements using the Turtle serialization. 

*Note*: if you install ontosPy using easy_install or pip, an  executable is automatically created and added to `usr/local/bin` (on unix-based systems). You can run it by typing `sketchonto`. 

	[lambdamusic]@here:~/code/python>sketch.py 
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
