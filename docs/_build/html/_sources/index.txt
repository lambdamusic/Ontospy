.. OntoSPy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:43:29 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OntoSPy's documentation!
===================================

OntoSPy is an RDFLIb-based Python toolkit for inspecting RDF vocabularies.

- Pypi: https://pypi.python.org/pypi/ontospy 

- Github: https://github.com/lambdamusic/OntoSPy


In a nutshell
--------------

OntoSPy is a lightweight Python library and command line tool for inspecting and navigating vocabularies encoded using W3C Semantic Web standards (aka ontologies). 

The basic workflow is simple: load a graph by instantiating the ``Graph`` class with a file containing RDFS, OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!
    
.. .. warning::
..     This documentation is still in draft mode.
..


Is OntoSPy for me? 
--------------

If you have a bunch of RDF vocabularies you regularly need to interrogate, but don't want to use a full-blown ontology editor like Protege, then OntoSPy might be good for you. 

.. code-block:: shell

    > ontospy foaf.rdf  # tells you all there is to know about the foaf vocabulary
    ----------
    Loaded 630 triples from <foaf.rdf>
    started scanning...
    ----------
    Ontologies found: 1
    Classes found...: 15
    Properties found: 67
    Annotation......: 7
    Datatype........: 26
    Object..........: 34
    -----------
    # ..etc.. 
    
The same functionalities are accessible also via a handy command line application. This consists of an interactive environment (`ontospy --shell`) that allows to save ontologies into a local repository so that they can be quickly reloaded for inspection later on.  

.. note:: OntoSPy offers no ontology editing functionalities, nor it can be used to interrogate a corresponding knowledge base (eg a triplestore) although the library could be easily extended to do that.


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

