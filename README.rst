OntoSpy
=======================

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.


Description
------------


OntoSpy is a lightweight Python library and command line tool for inspecting and visualizing vocabularies encoded using W3C Semantic Web standards, that is, RDF or any of its dialects (RDFS, OWL, SKOS).

The basic workflow is simple: load a graph by instantiating the ``Ontospy`` class with a file containing RDFS, OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via a command line application (`ontospy-shell`). This is an interactive environment (like a repl) that allows to load ontologies from a local repository, interrogate them and cache them so that they can be quickly reloaded for inspection later on.


Documentation
---------------
http://ontospy.readthedocs.org/en/latest/

See also: https://github.com/lambdamusic/OntoSPy

