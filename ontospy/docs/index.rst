.. OntoSPy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:43:29 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OntoSPy's documentation!
===================================

OntoSPy is an RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.

<<<<<<< HEAD
<<<<<<< HEAD
OntosPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic worflow is simple: load an ontology by instantiating the ``Ontology`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

Ps: the library can be used in standalone mode too.


Contents:
=======
https://pypi.python.org/pypi/ontospy

=======
>>>>>>> stg

In a nutshell
--------------

OntosPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

Originally, I developed this in order to get the hang of the Python RDFLib library (note: it was previously called OntoInspector and hosted on BitBucket). RDFLib provides a number of useful primitives for working with RDF graphs; however it lacks an API aimed at interrogating and modifying a graph based on its defined schema - aka the ontology.

The basic worflow is simple: load a graph by instantiating the ``Graph`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

Ps: the library can be used in standalone mode too.

.. warning::
	This documentation is still in draft mode. 


See also
--------------

- Homepage on Pypi: https://pypi.python.org/pypi/ontospy 

- Homepage on Github: https://github.com/lambdamusic/OntoSPy


Contents
--------------
>>>>>>> stg

.. toctree::
   :maxdepth: 2

<<<<<<< HEAD
   intro
=======
   installation
   quickstart
   quickstart_cmdline
   tests
>>>>>>> stg
   
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

