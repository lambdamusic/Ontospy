Quick Start - Python
************************
For the ones who have little time.

.. warning::
  This documentation is not up to date.

    


Inspecting a graph
+++++++++++++++++++++++++++++++

Load the graph
-------------------------------

.. code-block:: python

	In [1]: import ontospy
	INFO:rdflib:RDFLib Version: 4.2.0

	In [2]: g = ontospy2.Graph("npgcore_latest.ttl")
	Loaded 3478 triples
	Ontologies found: 1
    

	
Get a class
---------------------------------------------

.. code-block:: python

    In [1]: g.getClass(uri='http://www.w3.org/2000/01/rdf-schema#Resource')
    Out[1]: <Class *http://www.w3.org/2000/01/rdf-schema#Resource*>

    In [2]: g.getClass(10)
    Out[2]: <Class *http://purl.org/ontology/bibo/AcademicArticle*>	

    In [3]: g.getClass(match="person")
    Out[3]: 
    [<Class *http://purl.org/ontology/bibo/PersonalCommunicationDocument*>,
     <Class *http://purl.org/ontology/bibo/PersonalCommunication*>,
     <Class *http://xmlns.com/foaf/0.1/Person*>]



Pretty Print Triples
---------------------------------------------

.. code-block:: python

    In [8]: g.getClass(173).triplesPrint()
       => http://www.w3.org/2003/06/sw-vocab-status/ns#term_status
          stable
       => http://www.w3.org/2000/01/rdf-schema#label
          solo music artist
       => http://purl.org/ontology/mo/level
          1
       => http://www.w3.org/2000/01/rdf-schema#subClassOf
          http://purl.org/ontology/mo/MusicArtist
       => http://www.w3.org/2000/01/rdf-schema#subClassOf
          http://xmlns.com/foaf/0.1/Person
       => http://www.w3.org/2000/01/rdf-schema#isDefinedBy
          http://purl.org/ontology/mo/
       => http://www.w3.org/2000/01/rdf-schema#comment
          Single person whose musical creative work shows sensitivity and imagination.
       => http://www.w3.org/1999/02/22-rdf-syntax-ns#type
          http://www.w3.org/2002/07/owl#Class



Serialize an entity
---------------------------------------------

.. code-block:: python

    In [9]: print g.getClass(173).serialize()
    @prefix ns1: <http://purl.org/ontology/mo/> .
    @prefix ns2: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ns1:SoloMusicArtist a <http://www.w3.org/2002/07/owl#Class> ;
        rdfs:label "solo music artist" ;
        ns1:level "1" ;
        rdfs:comment "Single person whose musical creative work shows sensitivity and imagination." ;
        rdfs:isDefinedBy ns1: ;
        rdfs:subClassOf ns1:MusicArtist,
            <http://xmlns.com/foaf/0.1/Person> ;
        ns2:term_status "stable" .



Descendands and ancestors for a class
---------------------------------------------

.. code-block:: python

    In [8]: c = g.getClass(144)

    In [10]: c.descendants()
    Out[10]: []

    In [11]: c.ancestors()
    Out[11]: 
    [<Class *http://ns.nature.com/terms/Contributor*>,
     <Class *http://ns.nature.com/terms/DocumentComponent*>,
     <Class *http://ns.nature.com/terms/Publication*>,
     <Class *http://ns.nature.com/terms/AbstractEntity*>,
     <Class *http://ns.nature.com/terms/Thing*>]



Access a quick description of a class or property
---------------------------------------------

.. code-block:: python

    In [13]: c.describe()
    Parents......: 1
    Children.....: 0
    Ancestors....: 5
    Descendants..: 0
    Domain of....: 0
    Range of.....: 1
    http://ns.nature.com/terms/ExternalContributor
    => http://www.w3.org/2004/02/skos/core#historyNote
    .... [skos:definition - 2014-12-15] A document component detailing a contributor (personal or corporate) to an external work.
    => http://ns.nature.com/terms/graphLabel
    .... npgg:external-contributors
    => http://www.w3.org/2000/01/rdf-schema#isDefinedBy
    .... http://ns.nature.com/terms/
    => http://www.w3.org/2000/01/rdf-schema#label
    .... Term: npg:ExternalContributor
    => http://ns.nature.com/terms/isTerm
    .... true
    => http://www.w3.org/2004/02/skos/core#prefLabel
    .... External Contributor
    => http://www.w3.org/2004/02/skos/core#definition
    .... The :ExternalContributor class represents a contributor from an article which is externally published. The :ExternalContributor class subclasses the :Contributor class.
    => http://ns.nature.com/terms/namespace
    .... http://ns.nature.com/external-contributors/
    => http://ns.nature.com/terms/type
    .... external-contributors
    => http://ns.nature.com/terms/label
    .... external-contributors
    => http://ns.nature.com/terms/isVocabulary
    .... false
    => http://ns.nature.com/terms/hasGraph
    .... http://ns.nature.com/graphs/external-contributors
    => http://www.w3.org/1999/02/22-rdf-syntax-ns#type
    .... http://www.w3.org/2002/07/owl#Class
    => http://www.w3.org/2000/01/rdf-schema#subClassOf
    .... http://ns.nature.com/terms/Contributor




Getting data from multiple ontologies
++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    In [30]: g2 = ontospy.Graph("data/schemas/npgmusic_mix.ttl")
    ----------
    Loaded 3225 triples from <data/schemas/npgmusic_mix.ttl>
    started scanning...
    ----------
    Ontologies found: 2
    Classes found...: 109
    Properties found: 301
    Annotation......: 10
    Datatype........: 107
    Object..........: 184

    In [31]: for o in g2.ontologies:
       ....:     print o, len(o.classes)
       ....:     
    <OntoSPy: Ontology object for uri *http://ns.nature.com/terms/*> 49
    <OntoSPy: Ontology object for uri *http://purl.org/ontology/mo/*> 54



Querying a SPARQL endpoint
---------------------------------------------

.. code-block:: python

    In [12]: g = ontospy.Graph("http://data.semanticweb.org/sparql", endpoint=True)
    started scanning...
    ----------
    Ontologies found: 20
    Classes found...: 105
    Properties found: 53
    Annotation......: 5
    Datatype........: 18
    Object..........: 30

    In [13]: g.pri
    g.printClassTree     g.printPropertyTree  

    In [13]: g.printClassTree()
    [656] http://swrc.ontoware.org/ontology#ResearchTopic
    [657] http://www.w3.org/2002/12/cal/ical#Vcalendar
    [658] http://www.w3.org/2002/12/cal/ical#Vevent
    [608] ----http://data.semanticweb.org/ns/swc/ontology#OrganisedEvent
    [566] --------http://data.semanticweb.org/ns/swc/ontology#AcademicEvent
    [585] ------------http://data.semanticweb.org/ns/swc/ontology#ConferenceEvent
    [610] ------------http://data.semanticweb.org/ns/swc/ontology#PanelEvent
    [633] ------------http://data.semanticweb.org/ns/swc/ontology#SessionEvent
    [590] ----------------http://data.semanticweb.org/ns/swc/ontology#DemoSession
    [613] ----------------http://data.semanticweb.org/ns/swc/ontology#PaperSession
    [618] ----------------http://data.semanticweb.org/ns/swc/ontology#PosterSession
    # etc.....


Query via Sparql
---------------------------------------------

Note: this returns raw URIRef instances (from rdflib), not OntoSPY ones!

.. code-block:: python

    In [1]: import ontospy2
    INFO:rdflib:RDFLib Version: 4.2.0

    In [2]: g = ontospy2.Graph("data/foaf.rdf")
    Loaded 630 triples
    started scanning...
    Ontologies found: 1
    Classes	   found: 28
    Properties found: 145
    ...Annotation   : 7
    ...Datatype     : 27
    ...Object       : 49

    In [3]: g.sparql("select distinct ?c where {?x a ?c}")
    Out[3]: 
    [(rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#DatatypeProperty')),
     (rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty')),
     (rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#Class')),
     (rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')),
     (rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#Class')),
     (rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#InverseFunctionalProperty')),
     (rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#Ontology')),
     (rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#AnnotationProperty')),
     (rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#FunctionalProperty'))]
 

