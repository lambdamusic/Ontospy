Command Line Usage
************************
This page shows how to use Ontospy from the command line. 

These are the commands available: 

- ``ontospy``: used to launch the Ontospy parser.
- ``ontospy-shell``: used to launch the Ontospy command line interface.
- ``ontospy-viz``: used to the launch the Ontospy visualization library.


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

	Usage: ontospy [OPTIONS] [SOURCES]...

	  Ontospy is a command line inspector for RDF/OWL knowledge models.

	  Examples:

	  Inspect a local RDF file:

	  > ontospy /path/to/mymodel.rdf

	  List ontologies available in the local library:

	  > ontospy -l

	  Open FOAF vocabulary and save it to the local library:

	  > ontospy http://xmlns.com/foaf/spec/ -s

	  More info: <ontospy.readthedocs.org>

	Options:
	  -b, --bootstrap  BOOTSTRAP: bootstrap the local library.
	  -c, --cache      CACHE: force caching of the local library (for faster
					   loading).
	  -d, --delete     DELETE: remove an ontology from the local library.
	  -l, --library    LIBRARY: list ontologies saved in the local library.
	  -s, --save       SAVE: save a file/folder/url into the local library.
	  -r, --reset      RESET: delete all files in the local library.
	  -u, --update     UPDATE: enter new path for the local library.
	  -v, --verbose    VERBOSE: show entities labels as well as URIs.
	  -w, --web        WEB: import ontologies from remote repositories.
	  -h, --help       Show this message and exit.

Just calling ``ontospy`` without any argument has the effect of listing out all RDF models saved in the local library. The first time you run it, there are none obviously so you might want to run the ``ontospy -b`` option to get started.

Alternatively, you can also pass a valid graph URI as an argument to the ``ontospy`` command in order to print out useful ontology information:					

.. code-block:: shell

	> ontospy http://www.ifomis.org/bfo/1.1

	# prints info about BFO resolving redirects etc..
	
	Ontospy v1.7
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

.. note::
	You can pass the Ontospy command either  a single file or a folder path. In the second case it'll try to load any RDF file found in that path (recursively). For example, the second option can be handy if you have a knowledge model which is split into multiple files.


The ``ontospy-shell`` command
------------------------

.. code-block:: shell

	> ontospy-shell -h
	Usage: ontospy-shell [OPTIONS] [SOURCE]...

	  This application launches the OntoSpy interactive shell.

	  Note: if a local path or URI of an RDF model is provided, that gets loaded
	  into the shell by default. E.g.:

	  > ontospy-shell path/to/mymodel.rdf

	Options:
	  -h, --help  Show this message and exit.

Calling ``ontospy-shell`` without any argument launches the shell. The shell is an interactive environment that lets you import, load and inspect vocabularies. For more examples on how that works, take a look at this `video <https://vimeo.com/169707591>`_:

.. raw:: html

	<iframe src="https://player.vimeo.com/video/169707591" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

Note: you can pass an argument in order to pre-load an RDF graph into the interactive session.



The ``ontospy-viz`` command
------------------------

This utility allows to generate documentation for an RDF vocabulary, using visualization algorithms that create simple HTML pages, Markdown files, or more complex javascript interactive charts based on D3.js.

.. code-block:: shell

	> ontospy-viz -h
	Usage: ontospy-viz [OPTIONS] [SOURCE]...

	  This application launches the OntoSpy visualization tool.

	  Example:      > ontospy-viz path/to/mymodel.rdf

	  Note: if the location of an RDF model is not provided, a selection can be
	  made from the contents of the local ontospy library folder.

	Options:
	  -o, --outputpath TEXT  Output path (default: home folder)
	  -h, --help             Show this message and exit.

Some of the export options are still quite experimental, so it's advisable to try out more than one if you're not happy with the results.

.. code-block:: shell

	1) Javadoc
	2) Markdown
	3) Split Columns
	4) Dendogram
	5) Pack Hierarchy
	6) Bubble Chart
	7) Cluster Tree
	8) Bar Hierarchy
	9) Partition Table
	10) Tree Pie