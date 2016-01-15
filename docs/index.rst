.. OntoSPy documentation master file, created by
   sphinx-quickstart on Tue May  5 16:43:29 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OntoSPy's documentation!
===================================

OntoSPy is a lightweight Python library and command line tool for browsing and querying models encoded using W3C Semantic Web standards (aka vocabularies or ontologies). 

Useful links: 

- CheeseShop: https://pypi.python.org/pypi/ontospy 

- Github: https://github.com/lambdamusic/OntoSPy

- Homepage: http://www.michelepasin.org/projects/ontospy


.. warning::
    This documentation is still in draft mode.


In a nutshell
--------------

OntosPy can be used either as a standalone command line tool or as a Python package. 

Standalone: type `ontospy -h` from the command line to see what functionalities are available. This includes also an interactive shell environment that allows to save ontologies into a local repository so that they can be quickly reloaded for inspection later on.

Python package: the basic workflow is simple; load a graph by instantiating the ``Graph`` class with a file containing RDFS, OWL or SKOS definitions. You get back an object that lets you interrogate the ontology. That's all!



Is OntoSPy for me? 
--------------

Here are some common usage scenarios:

- You have a bunch of RDF vocabularies you regularly need to interrogate, but do not want to load a full-blown ontology editor like Protege.

- You need to generate documentation for an ontology, either as simple html pages or via some more elaborate interactive visualization. 

- You are developing a Python application that needs to extract schema information from an RDF, SKOS or OWL vocabulary. 

.. note:: OntoSPy offers no ontology editing functionalities currenlty, nor it can be used to interrogate a corresponding knowledge base (e.g. a triplestore).


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

