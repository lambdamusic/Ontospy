OntoSPy
=======================

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.


Description
------------


OntoSPy is a lightweight Python library and command line tool for inspecting and navigating vocabularies encoded using W3C Semantic Web standards (aka ontologies). 

In a nutshell: if you have a bunch of RDF schemas you regularly need to interrogate, but don't want to use a full-blown ontology editor like Protege, then OntoSPy might be good for you. 

The basic workflow is simple: load a graph by instantiating the ``Graph`` class with a file containing RDFS/OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via the command line by using the  `ontospy` application. This includes also an interactive environment (`ontospy --shell`) that allows to import ontologies into a local repository so that they can be quickly opened for inspection later on. 

Note: OntoSPy offers no ontology editing functionalities, nor it can be used to interrogate a corresponding knowledge base (eg a triplestore) although the library could be easily extended to do that. 

See also:
- documentation: http://ontospy.readthedocs.org/en/latest/
- source: https://github.com/lambdamusic/OntoSPy


Version 
---------------------------------------------------
1.6 (Oct 2016)

Check the ``ontospy/_version.py`` file for more details.


Example 
---------------------------------------------------

Here's a simple example to get you started, but please refer to the online documentation for more up to date stuff: http://ontospy.readthedocs.org/en/latest/ 

Import OntoSPy and instantiate the Graph object with the FOAF ontology::


	In [1]: import ontospy
	INFO:rdflib:RDFLib Version: 4.2.0

	In [2]: g = ontospy.Graph("http://xmlns.com/foaf/0.1/")
	----------
	Loaded 631 triples from <http://xmlns.com/foaf/0.1/>
	started scanning...
	----------
	Ontologies found...: 1
	Classes found......: 14
	Properties found...: 67
	Annotation.........: 7
	Datatype...........: 26
	Object.............: 34
	SKOS Concepts......: 0
	----------

	In [3]: g.classes
	Out[3]: 
	[<Class *http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing*>,
	 <Class *http://xmlns.com/foaf/0.1/Agent*>,
	 <Class *http://xmlns.com/foaf/0.1/Document*>,
	 <Class *http://xmlns.com/foaf/0.1/Group*>,
	 <Class *http://xmlns.com/foaf/0.1/Image*>,
	 <Class *http://xmlns.com/foaf/0.1/LabelProperty*>,
	 <Class *http://xmlns.com/foaf/0.1/OnlineAccount*>,
	 <Class *http://xmlns.com/foaf/0.1/OnlineChatAccount*>,
	 <Class *http://xmlns.com/foaf/0.1/OnlineEcommerceAccount*>,
	 <Class *http://xmlns.com/foaf/0.1/OnlineGamingAccount*>,
	 <Class *http://xmlns.com/foaf/0.1/Organization*>,
	 <Class *http://xmlns.com/foaf/0.1/Person*>,
	 <Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>,
	 <Class *http://xmlns.com/foaf/0.1/Project*>]

	In [4]: g.properties
	Out[4]: 
	[<Property *http://xmlns.com/foaf/0.1/account*>,
	 <Property *http://xmlns.com/foaf/0.1/accountName*>,
	 <Property *http://xmlns.com/foaf/0.1/accountServiceHomepage*>,
	 <Property *http://xmlns.com/foaf/0.1/age*>,
	 <Property *http://xmlns.com/foaf/0.1/aimChatID*>,
	 <Property *http://xmlns.com/foaf/0.1/based_near*>,
	 <Property *http://xmlns.com/foaf/0.1/birthday*>,
	 <Property *http://xmlns.com/foaf/0.1/currentProject*>,
	 <Property *http://xmlns.com/foaf/0.1/depiction*>,
	 <Property *http://xmlns.com/foaf/0.1/depicts*>,
	 <Property *http://xmlns.com/foaf/0.1/dnaChecksum*>,
	 <Property *http://xmlns.com/foaf/0.1/familyName*>,
	 <Property *http://xmlns.com/foaf/0.1/family_name*>,
	 <Property *http://xmlns.com/foaf/0.1/firstName*>,
	 <Property *http://xmlns.com/foaf/0.1/focus*>,
	 <Property *http://xmlns.com/foaf/0.1/fundedBy*>,
	 <Property *http://xmlns.com/foaf/0.1/geekcode*>,
	 <Property *http://xmlns.com/foaf/0.1/gender*>,
	 <Property *http://xmlns.com/foaf/0.1/givenName*>,
	 <Property *http://xmlns.com/foaf/0.1/holdsAccount*>,
	 <Property *http://xmlns.com/foaf/0.1/homepage*>,
	 <Property *http://xmlns.com/foaf/0.1/icqChatID*>,
	 <Property *http://xmlns.com/foaf/0.1/img*>,
	 <Property *http://xmlns.com/foaf/0.1/interest*>,
	 <Property *http://xmlns.com/foaf/0.1/isPrimaryTopicOf*>,
	 <Property *http://xmlns.com/foaf/0.1/jabberID*>,
	 <Property *http://xmlns.com/foaf/0.1/knows*>,
	 <Property *http://xmlns.com/foaf/0.1/lastName*>,
	 <Property *http://xmlns.com/foaf/0.1/logo*>,
	 <Property *http://xmlns.com/foaf/0.1/made*>,
	 <Property *http://xmlns.com/foaf/0.1/maker*>,
	 <Property *http://xmlns.com/foaf/0.1/mbox*>,
	 <Property *http://xmlns.com/foaf/0.1/mbox_sha1sum*>,
	 <Property *http://xmlns.com/foaf/0.1/member*>,
	 <Property *http://xmlns.com/foaf/0.1/membershipClass*>,
	 <Property *http://xmlns.com/foaf/0.1/msnChatID*>,
	 <Property *http://xmlns.com/foaf/0.1/myersBriggs*>,
	 <Property *http://xmlns.com/foaf/0.1/name*>,
	 <Property *http://xmlns.com/foaf/0.1/nick*>,
	 <Property *http://xmlns.com/foaf/0.1/openid*>,
	 <Property *http://xmlns.com/foaf/0.1/page*>,
	 <Property *http://xmlns.com/foaf/0.1/pastProject*>,
	 <Property *http://xmlns.com/foaf/0.1/phone*>,
	 <Property *http://xmlns.com/foaf/0.1/plan*>,
	 <Property *http://xmlns.com/foaf/0.1/primaryTopic*>,
	 <Property *http://xmlns.com/foaf/0.1/publications*>,
	 <Property *http://xmlns.com/foaf/0.1/schoolHomepage*>,
	 <Property *http://xmlns.com/foaf/0.1/sha1*>,
	 <Property *http://xmlns.com/foaf/0.1/skypeID*>,
	 <Property *http://xmlns.com/foaf/0.1/status*>,
	 <Property *http://xmlns.com/foaf/0.1/surname*>,
	 <Property *http://xmlns.com/foaf/0.1/theme*>,
	 <Property *http://xmlns.com/foaf/0.1/thumbnail*>,
	 <Property *http://xmlns.com/foaf/0.1/tipjar*>,
	 <Property *http://xmlns.com/foaf/0.1/title*>,
	 <Property *http://xmlns.com/foaf/0.1/topic*>,
	 <Property *http://xmlns.com/foaf/0.1/topic_interest*>,
	 <Property *http://xmlns.com/foaf/0.1/weblog*>,
	 <Property *http://xmlns.com/foaf/0.1/workInfoHomepage*>,
	 <Property *http://xmlns.com/foaf/0.1/workplaceHomepage*>,
	 <Property *http://xmlns.com/foaf/0.1/yahooChatID*>,
	 <Property *http://purl.org/dc/elements/1.1/date*>,
	 <Property *http://purl.org/dc/elements/1.1/description*>,
	 <Property *http://purl.org/dc/elements/1.1/title*>,
	 <Property *http://www.w3.org/2003/06/sw-vocab-status/ns#term_status*>,
	 <Property *http://xmlns.com/wot/0.1/assurance*>,
	 <Property *http://xmlns.com/wot/0.1/src_assurance*>]

	In [5]: g.printClassTree()
	[1]    http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing
	[12]   ----_file_:Person
	[2]    _file_:Agent
	[4]    ----_file_:Group
	[11]   ----_file_:Organization
	[12]   ----_file_:Person
	[3]    _file_:Document
	[5]    ----_file_:Image
	[13]   ----_file_:PersonalProfileDocument
	[6]    _file_:LabelProperty
	[7]    _file_:OnlineAccount
	[8]    ----_file_:OnlineChatAccount
	[9]    ----_file_:OnlineEcommerceAccount
	[10]   ----_file_:OnlineGamingAccount
	[14]   _file_:Project


	In [6]: g.toplayer
	Out[6]: 
	[<Class *http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing*>,
	 <Class *http://xmlns.com/foaf/0.1/Agent*>,
	 <Class *http://xmlns.com/foaf/0.1/Document*>,
	 <Class *http://xmlns.com/foaf/0.1/LabelProperty*>,
	 <Class *http://xmlns.com/foaf/0.1/OnlineAccount*>,
	 <Class *http://xmlns.com/foaf/0.1/Project*>]

	In [7]: g.getClass("document")
	Out[7]: 
	[<Class *http://xmlns.com/foaf/0.1/Document*>,
	 <Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>]

	In [8]: d = _[0]

	In [9]: print(d.serialize())
	@prefix ns1: <http://www.w3.org/2002/07/owl#> .
	@prefix ns2: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .
	@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix xml: <http://www.w3.org/XML/1998/namespace> .
	@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

	<http://xmlns.com/foaf/0.1/Document> a rdfs:Class,
	        ns1:Class ;
	    rdfs:label "Document" ;
	    rdfs:comment "A document." ;
	    rdfs:isDefinedBy <http://xmlns.com/foaf/0.1/> ;
	    ns1:disjointWith <http://xmlns.com/foaf/0.1/Organization>,
	        <http://xmlns.com/foaf/0.1/Project> ;
	    ns1:equivalentClass <http://schema.org/CreativeWork> ;
	    ns2:term_status "stable" .



	In [10]: d.parents()
	Out[10]: []

	In [11]: d.children()
	Out[11]: 
	[<Class *http://xmlns.com/foaf/0.1/Image*>,
	 <Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>]



