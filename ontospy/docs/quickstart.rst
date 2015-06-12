Quick Start
************************
For the ones who have little time


Running the tests
++++++++++++++++++++++++++++++++++++++++++++
Make sure you're in the ontospy root folder 

.. code-block:: python

    [michele.pasin]@Tartaruga:~/ontospy>python tests/test_simple.py 
    -------------------
    OntosPy version:  %prog v2.0.0 
    -------------------

    TEST 1: Loading ontologies from data/schemas/ folder.
    =================
    ...etc......
    
    

Inspect a graph
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

	In [1]: import ontospy2
	INFO:rdflib:RDFLib Version: 4.2.0

	In [2]: g = ontospy2.Graph("npgcore_latest.ttl")
	Loaded 3478 triples
	Ontologies found: 1
    

	
Get a class
++++++++++++++++++++++++++++++++++++++++++++

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
++++++++++++++++++++++++++++++++++++++++++++

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
++++++++++++++++++++++++++++++++++++++++++++

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




Query via Sparql
++++++++++++++++++++++++++++++++++++++++++++

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
 


Descendands and ancestors
++++++++++++++++++++++++++++++++++++++++++++

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
++++++++++++++++++++++++++++++++++++++++++++

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



Include labels in property tree
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: shell

    > ontospy.py data/schemas/foaf.rdf -c -l
    ----------
    Loaded 630 triples from <data/schemas/foaf.rdf>
    started scanning...
    ----------
    Ontologies found: 1
    Classes found...: 15
    Properties found: 67
    Annotation......: 7
    Datatype........: 26
    Object..........: 34
    -----------
    Metadata:

    http://xmlns.com/foaf/0.1/
    => http://purl.org/dc/elements/1.1/title
    .... Friend of a Friend (FOAF) vocabulary
    => http://www.w3.org/1999/02/22-rdf-syntax-ns#type
    .... http://www.w3.org/2002/07/owl#Ontology
    => http://purl.org/dc/elements/1.1/description
    .... The Friend of a Friend (FOAF) RDF vocabulary, described using W3C RDF Schema and the Web Ontology Language.

    Class Taxonomy
    ----------
    http://www.w3.org/2000/10/swap/pim/contact#Person ("Person")
    ----foaf:Person ("Person")
    http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing ("Spatial Thing")
    ----foaf:Person ("Person")
    foaf:Agent ("Agent")
    ----foaf:Group ("Group")
    ----foaf:Organization ("Organization")
    ----foaf:Person ("Person")
    foaf:Document ("Document")
    ----foaf:Image ("Image")
    ----foaf:PersonalProfileDocument ("PersonalProfileDocument")
    foaf:LabelProperty ("Label Property")
    foaf:OnlineAccount ("Online Account")
    ----foaf:OnlineChatAccount ("Online Chat Account")
    ----foaf:OnlineEcommerceAccount ("Online E-commerce Account")
    ----foaf:OnlineGamingAccount ("Online Gaming Account")
    foaf:Project ("Project")
    ----------
    Time:	   2.77s





Match two models (in development)
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    ontospy> python tools/matcher.py data/schemas/foaf.rdf data/schemas/bibo.owl 
    Match classes or properties? [c|p]: c
    ----------
    Loaded 630 triples from <data/schemas/foaf.rdf>
    started scanning...
    ----------
    Ontologies found: 1
    Classes found...: 15
    Properties found: 67
    Annotation......: 7
    Datatype........: 26
    Object..........: 34
    ----------
    Loaded 1215 triples from <data/schemas/bibo.owl>
    started scanning...
    ----------
    Ontologies found: 1
    Classes found...: 65
    Properties found: 117
    Annotation......: 12
    Datatype........: 54
    Object..........: 51
    ----------
    Now matching...
    31 candidates found.
    ----------
    Time:	   7.14s

    # results are saved by default in same folder
    
    > python tools/matcher.py -h
    Usage: 

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTPUTFILE, --outputfile=OUTPUTFILE
                            The name of the output csv file.
      -c CONFIDENCE, --confidence=CONFIDENCE
                            @TODO 0.1-0.9 degree of confidence for similarity
                            matching.
                            




Querying a SPARQL endpoint
++++++++++++++++++++++++++++++++++++++++++++

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
    [641] ------------http://data.semanticweb.org/ns/swc/ontology#TalkEvent
    [589] ----------------http://data.semanticweb.org/ns/swc/ontology#DemoPresentation
    [598] ----------------http://data.semanticweb.org/ns/swc/ontology#IndustrialTalk
    [602] ----------------http://data.semanticweb.org/ns/swc/ontology#KeynoteTalk
    [612] ----------------http://data.semanticweb.org/ns/swc/ontology#PaperPresentation
    [617] ----------------http://data.semanticweb.org/ns/swc/ontology#PosterPresentation
    [650] ----------------http://data.semanticweb.org/ns/swc/ontology#WelcomeTalk
    [643] ------------http://data.semanticweb.org/ns/swc/ontology#TrackEvent
    [599] ----------------http://data.semanticweb.org/ns/swc/ontology#IndustrialTrack
    [628] ----------------http://data.semanticweb.org/ns/swc/ontology#ResearchTrack
    [646] ------------http://data.semanticweb.org/ns/swc/ontology#TutorialEvent
    [651] ------------http://data.semanticweb.org/ns/swc/ontology#WorkshopEvent
    [607] --------http://data.semanticweb.org/ns/swc/ontology#NonAcademicEvent
    [572] ------------http://data.semanticweb.org/ns/swc/ontology#BreakEvent
    [580] ----------------http://data.semanticweb.org/ns/swc/ontology#CoffeeBreak
    [597] ----------------http://data.semanticweb.org/ns/swc/ontology#FreeTimeBreak
    [604] ----------------http://data.semanticweb.org/ns/swc/ontology#MealBreak
    [583] ------------http://data.semanticweb.org/ns/swc/ontology#ConferenceClosingEvent
    [586] ------------http://data.semanticweb.org/ns/swc/ontology#ConferenceOpeningEvent
    [605] ------------http://data.semanticweb.org/ns/swc/ontology#MealEvent
    [584] ----------------http://data.semanticweb.org/ns/swc/ontology#ConferenceDinner
    [635] ------------http://data.semanticweb.org/ns/swc/ontology#SocialEvent
    [584] ----------------http://data.semanticweb.org/ns/swc/ontology#ConferenceDinner
    [595] ----------------http://data.semanticweb.org/ns/swc/ontology#Excursion
    [627] ----------------http://data.semanticweb.org/ns/swc/ontology#Reception
    [659] http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing
    [567] ----http://data.semanticweb.org/ns/swc/ontology#AccommodationPlace
    [581] ----http://data.semanticweb.org/ns/swc/ontology#CommunalPlace
    [587] ----http://data.semanticweb.org/ns/swc/ontology#ConferenceVenuePlace
    [606] ----http://data.semanticweb.org/ns/swc/ontology#MeetingRoomPlace
    [615] ----http://data.semanticweb.org/ns/swc/ontology#Place
    [593] --------http://data.semanticweb.org/ns/swc/ontology#DrinkingPlace
    [594] --------http://data.semanticweb.org/ns/swc/ontology#EatingPlace
    [660] http://xmlns.com/foaf/0.1/Document
    [570] ----http://data.semanticweb.org/ns/swc/ontology#ArgumentativeDocument
    [611] --------http://data.semanticweb.org/ns/swc/ontology#Paper
    [639] ------------http://data.semanticweb.org/ns/swc/ontology#SystemDemonstration
    [640] ------------http://data.semanticweb.org/ns/swc/ontology#SystemDescription
    [654] ------------http://swrc.ontoware.org/ontology#InProceedings
    [601] ----------------http://data.semanticweb.org/ns/swc/ontology#InvitedPaper
    [616] --------http://data.semanticweb.org/ns/swc/ontology#Poster
    [634] --------http://data.semanticweb.org/ns/swc/ontology#SlideSet
    [622] ----http://data.semanticweb.org/ns/swc/ontology#Proceedings
    [655] --------http://swrc.ontoware.org/ontology#Proceedings
    [623] ----http://data.semanticweb.org/ns/swc/ontology#Programme
    [661] http://xmlns.com/foaf/0.1/Group
    [662] http://xmlns.com/foaf/0.1/Organization
    [663] http://xmlns.com/foaf/0.1/Person
    [664] http://xmlns.com/foaf/0.1/Project
    [665] http://xmlns.com/wordnet/1.6/Announcement
    [573] ----http://data.semanticweb.org/ns/swc/ontology#Call
    [574] --------http://data.semanticweb.org/ns/swc/ontology#CallForDemos
    [575] --------http://data.semanticweb.org/ns/swc/ontology#CallForPapers
    [576] --------http://data.semanticweb.org/ns/swc/ontology#CallForParticipation
    [577] --------http://data.semanticweb.org/ns/swc/ontology#CallForPosters
    [578] --------http://data.semanticweb.org/ns/swc/ontology#CallForProposals
    [666] http://xmlns.com/wordnet/1.6/Document
    [571] ----http://data.semanticweb.org/ns/swc/ontology#Artefact
    [611] --------http://data.semanticweb.org/ns/swc/ontology#Paper
    [639] ------------http://data.semanticweb.org/ns/swc/ontology#SystemDemonstration
    [640] ------------http://data.semanticweb.org/ns/swc/ontology#SystemDescription
    [654] ------------http://swrc.ontoware.org/ontology#InProceedings
    [601] ----------------http://data.semanticweb.org/ns/swc/ontology#InvitedPaper
    [616] --------http://data.semanticweb.org/ns/swc/ontology#Poster
    [622] --------http://data.semanticweb.org/ns/swc/ontology#Proceedings
    [655] ------------http://swrc.ontoware.org/ontology#Proceedings
    [623] --------http://data.semanticweb.org/ns/swc/ontology#Programme
    [634] --------http://data.semanticweb.org/ns/swc/ontology#SlideSet
    [667] http://xmlns.com/wordnet/1.6/Event-1
    [608] ----http://data.semanticweb.org/ns/swc/ontology#OrganisedEvent
    [566] --------http://data.semanticweb.org/ns/swc/ontology#AcademicEvent
    [585] ------------http://data.semanticweb.org/ns/swc/ontology#ConferenceEvent
    [610] ------------http://data.semanticweb.org/ns/swc/ontology#PanelEvent
    [633] ------------http://data.semanticweb.org/ns/swc/ontology#SessionEvent
    [590] ----------------http://data.semanticweb.org/ns/swc/ontology#DemoSession
    [613] ----------------http://data.semanticweb.org/ns/swc/ontology#PaperSession
    [618] ----------------http://data.semanticweb.org/ns/swc/ontology#PosterSession
    [641] ------------http://data.semanticweb.org/ns/swc/ontology#TalkEvent
    [589] ----------------http://data.semanticweb.org/ns/swc/ontology#DemoPresentation
    [598] ----------------http://data.semanticweb.org/ns/swc/ontology#IndustrialTalk
    [602] ----------------http://data.semanticweb.org/ns/swc/ontology#KeynoteTalk
    [612] ----------------http://data.semanticweb.org/ns/swc/ontology#PaperPresentation
    [617] ----------------http://data.semanticweb.org/ns/swc/ontology#PosterPresentation
    [650] ----------------http://data.semanticweb.org/ns/swc/ontology#WelcomeTalk
    [643] ------------http://data.semanticweb.org/ns/swc/ontology#TrackEvent
    [599] ----------------http://data.semanticweb.org/ns/swc/ontology#IndustrialTrack
    [628] ----------------http://data.semanticweb.org/ns/swc/ontology#ResearchTrack
    [646] ------------http://data.semanticweb.org/ns/swc/ontology#TutorialEvent
    [651] ------------http://data.semanticweb.org/ns/swc/ontology#WorkshopEvent
    [607] --------http://data.semanticweb.org/ns/swc/ontology#NonAcademicEvent
    [572] ------------http://data.semanticweb.org/ns/swc/ontology#BreakEvent
    [580] ----------------http://data.semanticweb.org/ns/swc/ontology#CoffeeBreak
    [597] ----------------http://data.semanticweb.org/ns/swc/ontology#FreeTimeBreak
    [604] ----------------http://data.semanticweb.org/ns/swc/ontology#MealBreak
    [583] ------------http://data.semanticweb.org/ns/swc/ontology#ConferenceClosingEvent
    [586] ------------http://data.semanticweb.org/ns/swc/ontology#ConferenceOpeningEvent
    [605] ------------http://data.semanticweb.org/ns/swc/ontology#MealEvent
    [584] ----------------http://data.semanticweb.org/ns/swc/ontology#ConferenceDinner
    [635] ------------http://data.semanticweb.org/ns/swc/ontology#SocialEvent
    [584] ----------------http://data.semanticweb.org/ns/swc/ontology#ConferenceDinner
    [595] ----------------http://data.semanticweb.org/ns/swc/ontology#Excursion
    [627] ----------------http://data.semanticweb.org/ns/swc/ontology#Reception
    [668] http://xmlns.com/wordnet/1.6/Menu
    [669] http://xmlns.com/wordnet/1.6/Role-1
    [630] ----http://data.semanticweb.org/ns/swc/ontology#Role
    [568] --------http://data.semanticweb.org/ns/swc/ontology#AdditionalReviewer
    [569] --------http://data.semanticweb.org/ns/swc/ontology#Administrator
    [579] --------http://data.semanticweb.org/ns/swc/ontology#Chair
    [582] --------http://data.semanticweb.org/ns/swc/ontology#ConferenceChair
    [588] --------http://data.semanticweb.org/ns/swc/ontology#Delegate
    [591] --------http://data.semanticweb.org/ns/swc/ontology#DemosChair
    [592] --------http://data.semanticweb.org/ns/swc/ontology#DogfoodTsar
    [596] --------http://data.semanticweb.org/ns/swc/ontology#ExhibitionChair
    [600] --------http://data.semanticweb.org/ns/swc/ontology#IndustryChair
    [603] --------http://data.semanticweb.org/ns/swc/ontology#LocalOrganiser
    [609] --------http://data.semanticweb.org/ns/swc/ontology#OrganisingCommitteeMember
    [614] --------http://data.semanticweb.org/ns/swc/ontology#PhDSymposiumChair
    [619] --------http://data.semanticweb.org/ns/swc/ontology#PostersChair
    [620] --------http://data.semanticweb.org/ns/swc/ontology#Presenter
    [621] --------http://data.semanticweb.org/ns/swc/ontology#PrintedProceedingsChair
    [624] --------http://data.semanticweb.org/ns/swc/ontology#ProgrammeChair
    [625] --------http://data.semanticweb.org/ns/swc/ontology#ProgrammeCommitteeMember
    [626] --------http://data.semanticweb.org/ns/swc/ontology#PublicityChair
    [629] --------http://data.semanticweb.org/ns/swc/ontology#Reviewer
    [631] --------http://data.semanticweb.org/ns/swc/ontology#SWChallengeChair
    [632] --------http://data.semanticweb.org/ns/swc/ontology#SessionChair
    [637] --------http://data.semanticweb.org/ns/swc/ontology#SponsorshipChair
    [638] --------http://data.semanticweb.org/ns/swc/ontology#SubmissionsChair
    [642] --------http://data.semanticweb.org/ns/swc/ontology#TrackChair
    [644] --------http://data.semanticweb.org/ns/swc/ontology#Treasurer
    [645] --------http://data.semanticweb.org/ns/swc/ontology#Tutor
    [647] --------http://data.semanticweb.org/ns/swc/ontology#TutorialPresenter
    [648] --------http://data.semanticweb.org/ns/swc/ontology#TutorialsChair
    [649] --------http://data.semanticweb.org/ns/swc/ontology#Webmaster
    [652] --------http://data.semanticweb.org/ns/swc/ontology#WorkshopOrganiser
    [653] --------http://data.semanticweb.org/ns/swc/ontology#WorkshopsChair
    [670] http://xmlns.com/wordnet/1.6/Sponsorship
    [636] ----http://data.semanticweb.org/ns/swc/ontology#Sponsorship