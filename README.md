OntoSPy
=======

RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.


Description
=======

OntoSPy is a lightweight Python library and command line tool for inspecting and visualizing vocabularies encoded using W3C Semantic Web standards (aka ontologies). 

The basic workflow is simple: load a graph by instantiating the ``Graph`` class with a file containing RDFS, OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via a handy command line application (`ontospy`). This is an interactive environment (like a repl) that allows to load ontologies from a local repository, interrogate them and cache them so that they can be quickly reloaded for inspection later on. 


Documentation
---------------
http://ontospy.readthedocs.org/en/latest/

See also: https://pypi.python.org/pypi/ontospy



Changelog
---------------

v.1.6.5.6
- made the caching functionality version-dependent 
- added 'download' command
- json serialization (via rdflib-jsonld)
- added *bootstrap* command for empty repos
 

v.1.6.5.5
- added 'visualize' command
- added delete, rename, shell commands 