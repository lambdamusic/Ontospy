.. OntoSPy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:43:29 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OntoSPy's documentation!
===================================

OntoSPy is an RDFLIb-based Python toolkit for inspecting RDF vocabularies.

.. warning::
    This documentation is still in draft mode.


In a nutshell
--------------

OntoSPy is a lightweight Python library and command line tool for inspecting and navigating vocabularies encoded using W3C Semantic Web standards (aka ontologies). 

The basic workflow is simple: load a graph by instantiating the ``Graph`` class with a file containing RDFS, OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via a handy command line application. This consists of an interactive environment (`ontospy --shell`) that allows to save ontologies into a local repository so that they can be quickly reloaded for inspection later on.     

.. note:: OntoSPy offers no ontology editing functionalities, nor it can be used to interrogate a corresponding knowledge base (eg a triplestore) although the library could be easily extended to do that.



Is OntoSPy for me? 
--------------

Here are some common usage scenarios:

- You have a bunch of RDF vocabularies you regularly need to interrogate, but you'd rather use the command line than a full-blown ontology editor like Protege.

- You want to quickly generate documentation for an ontology, either as simple html pages or via some more elaborate interactive visualization. 

- You are developing a Python application that needs to extract schema information from an RDF, SKOS or OWL vocabulary. 



Quick example
--------------

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
    


See also
--------------

- Homepage: http://www.michelepasin.org/projects/ontospy

- Github: https://github.com/lambdamusic/OntoSPy

- CheeseShop: https://pypi.python.org/pypi/ontospy 



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

