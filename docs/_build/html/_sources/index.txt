.. OntoSPy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:43:29 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OntoSPy's documentation!
===================================

OntoSPy is an RDFLIb-based Python toolkit for inspecting ontologies encoded using one of the W3C Semantic Web standards.


In a nutshell
--------------

OntoSPy is a lightweight Python library and command line tool for inspecting and navigating vocabularies encoded using W3C Semantic Web standards (aka ontologies). 

In a nutshell: if you have a bunch of RDF schemas you regularly need to interrogate, but don't want to use a full-blown ontology editor like Protege, then OntoSPy might be good for you. 

The basic workflow is simple: load a graph by instantiating the ``Graph`` class with a file containing RDFS/OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via the command line by using the  `ontospy` application. This includes also an interactive environment (`ontospy --shell`) that allows to import ontologies into a local repository so that they can be quickly opened for inspection later on.  

.. note::
	OntoSPy offers no ontology editing functionalities, nor it can be used to interrogate a corresponding knowledge base (eg a triplestore) although the library could be easily extended to do that. 
    
.. .. warning::
..     This documentation is still in draft mode.
..

See also
--------------

- Homepage on Pypi: https://pypi.python.org/pypi/ontospy 

- Homepage on Github: https://github.com/lambdamusic/OntoSPy


Contents
--------------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   quickstart_cmdline
   tests
   
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

