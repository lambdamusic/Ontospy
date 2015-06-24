.. OntoSPy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:43:29 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OntoSPy's documentation!
===================================

OntoSPy is an RDFLIb-based Python toolkit for inspecting ontologies on the Semantic Web.

https://pypi.python.org/pypi/ontospy


In a nutshell
--------------

OntosPy allows you to extract all the schema information from an RDFS/OWL ontology, inspect it and use it query a corresponding knowledge base. 

The basic worflow is simple: load a graph by instantiating the ``Graph`` class; you get back an object that lets you interrogate the RDFS/OWL schema. That's all!

Ps: the library can be used in standalone mode too.

.. warning::
	This documentation is still largely inclomplete. In the meantime, please use the quickstart section for code examples. 


Installation
--------------

``pip install ontospy`` or ``easy_install ontospy``


Tests
---------------------------------
Go to the installation folder and run `test_load.py`. A selection of ontologies will be loaded and inspected. 

.. code-block:: python

	python ontospy/tests/test_load.py 
	-------------------
	OntoSPy  v1.5.0 
	-------------------

	TEST 1: Loading ontologies from ontospy/data/schemas/ folder.
	=================

	Loading... > bfo-1.1.owl
	----------
	Loaded 429 triples from <ontospy/data/schemas/bfo-1.1.owl>
	started scanning...
	----------
	Ontologies found: 1
	# etc....



Contents
--------------

.. toctree::
   :maxdepth: 2

   .. intro
   quickstart
   quickstart_cmdline
   
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

