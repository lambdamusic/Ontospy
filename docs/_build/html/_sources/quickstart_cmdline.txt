Command Line Usage
************************
This page shows how to use OntoSPy from the command line. 

These are the commands available: 

- ``ontospy``: used to launch the interactive ontospy shell, or to query a graph.
- ``ontospy-manager``: used to manage your local ontospy installation.
- ``ontospy-sketch``: (experimental) sketch a turtle model interactively.


.. note::
	If you install OntosPy via one of the suggested methods, appropriate executables for your platform should be compiled automatically and added to `usr/local/bin` (by default on unix-based systems). 

.. .. warning::
..	   This documentation is still in draft mode.
..
..



The ``ontospy`` command
------------------------

A good place to start is the -h option:

.. code-block:: shell

	> ontospy -h
	OntoSPy v1.6.5
	Usage: ontospy [graph-uri-or-location] [options]

	Options:
	  --version	  show program's version number and exit
	  -h, --help  show this help message and exit
	  -l		  LIBRARY: select ontologies saved in the local library
	  -v		  VERBOSE: show entities labels as well as URIs
	  -e		  EXPORT: export a model into another format (e.g. html)
	  -g		  GITHUB-GIST: export output as a Github Gist.
	  -i		  IMPORT: save a file/folder/url into the local library
	  -w		  WEB: save vocabularies registered on http://prefix.cc/popular.
 
 				  
Just calling ``ontospy`` without any argument launches the shell. The shell is an interactive environment that lets you import, load and inspect vocabularies. 

.. code-block:: shell

	> ontospy	
	OntoSPy v1.6.5.1
	Local library: </Users/michele.pasin/Dropbox/ontologies/ontospy-library/>
	******
	***
	* OntoSPy Interactive Ontology Browser v1.6.5.1 *
	***
	******
	Type 'help' to get started, TAB to explore commands.

	<OntoSPy>: help

	Commands available (type `help <command>` to get help):
	-------------------------------------------------------
	back  display  get	help  inspect  ls  next	 quit  serialize  shell	 tree  zen

	<OntoSPy>: help ls
	List available graphs or entities.
	==> Usage: ls [ontologies|classes|properties|concepts]
	<OntoSPy>: ls ontologies
	30 items available:
	--------------
	[1] base.owl.ttl					  
	[2] bfo-1.1.owl						  
	[3] cidoc_crm_v5.0.2.rdfs			  
	[4] cidoc_crm_v5.0.2_STANDALONE.rdfs  
	[5] cito.rdf						  
	[6] cohere8-online.owl				  
	[7] conflict1.owl					  
	[8] Countries.owl					  
	[9] dcterms.rdf						  
	[10] discourse-relationships.owl	  
	[11] DOLCE-Lite_397.owl				  
	[12] fabio.rdf						  
	[13] family.swrl.owl				  
	[14] finance_th_web.owl				  
	[15] foaf.rdf						  
	[16] food.rdf						  
	[17] frapo.owl						  
	[18] frbr.rdf						  
	[19] generations.owl				  
	[20] gold-2010.owl					  
	[21] goodrelations.rdf				  
	[22] hucit.owl						  
	[23] human_activities.owl.xml		  
	[24] InstructionalObjects.xml		  
	[25] ka.owl							  
	[26] keys.owl						  
	[27] koala.owl						  
	[28] laki.rdf						  
	[29] lexinfo.owl					  
	[30] mini_philosophy.owl			  
	--------------
	Please select one option by entering its number:
	2
	Loaded graph: </Users/michele.pasin/Dropbox/ontologies/ontospy-library/bfo-1.1.owl>
	----------------
	Ontologies......: 1
	Classes.........: 39
	Properties......: 9
	..annotation....: 9
	..datatype......: 0
	..object........: 0
	Concepts(SKOS)..: 0
	----------------
	==> Ontology URI: <http://www.ifomis.org/bfo/1.1>
	----------------
	<bfo-1.1.owl>:

	# etc.. 
	# now you can interrogate the BFO ontology by typing `ls classes` etc..
	

Pass a valid graph URI as an argument to print out useful ontology information:					

.. code-block:: shell

	> ontospy http://www.ifomis.org/bfo/1.1

	# prints info about BFO resolving redirects etc..
	
	OntoSPy v1.6.5.1
	Local library: </Users/michele.pasin/Dropbox/ontologies/ontospy-library/>
	----------
	.. trying rdf serialization: <xml>
	..... success!
	----------
	Loaded 429 triples from <https://raw.githubusercontent.com/BFO-ontology/BFO/releases/1.1.1/bfo.owl>
	started scanning...
	----------
	Ontologies found...: 1
	Classes found......: 39
	Properties found...: 9
	Annotation.........: 9
	Datatype...........: 0
	Object.............: 0
	SKOS Concepts......: 0
	----------

	Ontology Annotations
	-----------
	http://www.ifomis.org/bfo/1.1
	=> http://purl.org/dc/elements/1.1/source
	.... Pierre Grenon: "BFO in a Nutshell: A Bi-categorial Axiomatization of BFO and Comparison with DOLCE"
	=> http://purl.org/dc/elements/1.1/language
	.... en
	=> http://purl.org/dc/elements/1.1/title
	.... Basic Formal Ontology (BFO)
	=> http://www.w3.org/1999/02/22-rdf-syntax-ns#type
	.... http://www.w3.org/2002/07/owl#Ontology
	=> http://purl.org/dc/elements/1.1/source
	.... Barry Smith: "Against Fantology"
	=> http://purl.org/dc/elements/1.1/rights
	.... http://creativecommons.org/licenses/by/3.0
	=> http://purl.org/dc/elements/1.1/source
	.... Pierre Grenon, Barry Smith and Louis Goldberg: "Biodynamic Ontology: Applying BFO in the Biomedical Domain"
	=> http://www.w3.org/2002/07/owl#versionInfo
	.... 1.1.1
	=> http://purl.org/dc/elements/1.1/source
	.... Barry Smith: "Basic Tools of Formal Ontology"
	=> http://purl.org/dc/elements/1.1/contributor
	.... Pierre Grenon
	=> http://purl.org/dc/elements/1.1/contributor
	.... Andrew Spear
	=> http://purl.org/dc/elements/1.1/publisher
	.... Institute for Formal Ontology and Medical Information Science (IFOMIS)
	=> http://purl.org/dc/elements/1.1/contributor
	.... Alan Ruttenberg
	=> http://purl.org/dc/elements/1.1/source
	.... Pierre Grenon: "Spatio-temporality in Basic Formal Ontology: SNAP and SPAN, Upper-Level Ontology, and Framework for Formalization"
	=> http://purl.org/dc/elements/1.1/source
	.... Barry Smith: "Beyond Concepts: Ontology as Reality Representation"
	=> http://purl.org/dc/elements/1.1/creator
	.... Holger Stenzhorn
	=> http://purl.org/dc/elements/1.1/identifier
	.... http://www.ifomis.org/bfo/1.1
	=> http://purl.org/dc/elements/1.1/source
	.... Pierre Grenon: "Nuts in BFO's Nutshell: Revisions to the Bi-categorial Axiomatization of BFO"
	=> http://purl.org/dc/elements/1.1/format
	.... application/rdf+xml
	=> http://purl.org/dc/elements/1.1/source
	.... Pierre Grenon and Barry Smith: "SNAP and SPAN: Towards Geospatial Dynamics"
	=> http://purl.org/dc/elements/1.1/source
	.... Barry Smith and Pierre Grenon: "The Cornucopia of Formal Ontological Relations"


	Class Taxonomy
	----------
	bfo:Entity
	----snap:Continuant
	--------snap:DependentContinuant
	------------snap:GenericallyDependentContinuant
	------------snap:SpecificallyDependentContinuant
	----------------snap:Quality
	----------------snap:RealizableEntity
	--------------------snap:Disposition
	--------------------snap:Function
	--------------------snap:Role
	--------snap:IndependentContinuant
	------------snap:MaterialEntity
	----------------snap:FiatObjectPart
	----------------snap:Object
	----------------snap:ObjectAggregate
	------------snap:ObjectBoundary
	------------snap:Site
	--------snap:SpatialRegion
	------------snap:OneDimensionalRegion
	------------snap:ThreeDimensionalRegion
	------------snap:TwoDimensionalRegion
	------------snap:ZeroDimensionalRegion
	----span:Occurrent
	--------span:ProcessualEntity
	------------span:FiatProcessPart
	------------span:Process
	------------span:ProcessAggregate
	------------span:ProcessBoundary
	------------span:ProcessualContext
	--------span:SpatiotemporalRegion
	------------span:ConnectedSpatiotemporalRegion
	----------------span:SpatiotemporalInstant
	----------------span:SpatiotemporalInterval
	------------span:ScatteredSpatiotemporalRegion
	--------span:TemporalRegion
	------------span:ConnectedTemporalRegion
	----------------span:TemporalInstant
	----------------span:TemporalInterval
	------------span:ScatteredTemporalRegion

	Property Taxonomy
	----------
	dc:contributor
	dc:creator
	dc:format
	dc:identifier
	dc:language
	dc:publisher
	dc:rights
	dc:source
	dc:title

	----------
	Time:	   3.42s








The ``ontospy-manager`` command
------------------------

This utility allows to run management operations on a local ontospy library installation. 

.. code-block:: shell

	> ontospy-manager 
	OntoSPy v1.6.5
	Local library: </Users/michele.pasin/.ontospy>
	Usage: ontospy-manager <options>

	Options:
	  --version     show program's version number and exit
	  -h, --help    show this help message and exit
	  -l, --list    List ontologies saved in the local library.
	  -u, --update  Update path of local library.
	  -d, --delete  Delete ontologies from the local library.
	  -c, --cache   Force caching of the local library (for faster loading)
	  -e, --erase   Erase the local library by removing all existing files




