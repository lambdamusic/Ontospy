Command Line Usage
************************
This page shows how to use Ontospy from the command line. 

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
	Ontospy v1.6.7
	Usage: ontospy.py [graph-uri-or-location] [options]

	Options:
	  --version   show program's version number and exit
	  -h, --help  show this help message and exit
	  -l          LIBRARY: select ontologies saved in the local library
	  -v          VERBOSE: show entities labels as well as URIs
	  -b          BOOTSTRAP: save some sample ontologies into the local library
	  -i          IMPORT: save a file/folder/url into the local library
	  -w          IMPORT-FROM-REPO: import from an online directory
	  -e          EXPORT: export a model into another format (e.g. html)
	  -g          EXPORT-AS-GIST: export output as a Github Gist.

	Quick Examples:
	  > ontospy http://xmlns.com/foaf/spec/    # ==> prints info about FOAF
	  > ontospy http://xmlns.com/foaf/spec/ -i # ==> prints info and save local copy
	  > ontospy http://xmlns.com/foaf/spec/ -g # ==> exports ontology data into a github gist

	  For more, visit ontospy.readthedocs.org
 
 				  
Just calling ``ontospy`` without any argument launches the shell. The shell is an interactive environment that lets you import, load and inspect vocabularies. For more examples on how that works, take a look at this `video <http://quick.as/1yyyubjoy>`_:

.. raw:: html 

	<iframe name='quickcast' src='http://quick.as/embed/1yyyubjoy' scrolling='no' frameborder='0' width='100%' allowfullscreen></iframe><script src='http://quick.as/embed/script/1.60'></script>


Alternatively, you can also pass a valid graph URI as an argument to the ``ontospy`` command in order to print out useful ontology information:					

.. code-block:: shell

	> ontospy http://www.ifomis.org/bfo/1.1

	# prints info about BFO resolving redirects etc..
	
	Ontospy v1.6.5.1
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
	### ...etc....



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
	Ontospy v1.6.7
	Usage: ontospy-manager [options]

	Options:
	  --version   show program's version number and exit
	  -h, --help  show this help message and exit
	  -l          LIST: show ontologies saved in the local library.
	  -c          CACHE: force caching of the local library (for faster loading)
	  -u          UPDATE: enter new path for the local library.
	  -d          DELETE: remove a single ontology file from the local library.
	  -e          ERASE: reset the local library (delete all files)




