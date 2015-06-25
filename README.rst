OntoSPy
=======================

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.


Description
------------

OntoSPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic workflow is simple: load an ontology by instantiating the ``Ontology`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

See also:
- documentation: http://ontospy.readthedocs.org/en/latest/
- source: https://github.com/lambdamusic/OntoSPy


Example 
---------------------------------------------------

Import OntoSPy and instantiate the Graph object with the FOAF ontology::


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


