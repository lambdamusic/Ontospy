Command Line Usage
************************
A few examples of how to use OntoSPy from the command line. 

Currently these are the utility scripts available: 

- ``ontospy``: launch the interactive ontospy shell
- ``ontospy-manager``: manage your local ontospy installation 
- ``ontospy-sketch``: sketch a turtle model interactively (experimental) 


.. note::
    If you install OntosPy via one of the suggested methods, appropriate executables for your platform should be compiled automatically and added to `usr/local/bin` (on unix-based systems, or similar on windows). 

.. warning::
    This documentation is still in draft mode.

    



The ``ontospy`` command
*******************

.. code-block:: shell

    >ontospy http://xmlns.com/foaf/spec/

    # prints info about foaf resolving redirects etc..
    # etc..


For more info, use the -h option:

.. code-block:: shell

    > ontospy -h
    OntoSPy v1.6.5
    Usage: ontospy [graph-uri-or-location] [options]

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -l          LIBRARY: select ontologies saved in the local library
      -v          VERBOSE: show entities labels as well as URIs
      -e          EXPORT: export a model into another format (e.g. html)
      -g          GITHUB-GIST: export output as a Github Gist.
      -i          IMPORT: save a file/folder/url into the local library
      -w          WEB: save vocabularies registered on http://prefix.cc/popular.
                  
                  
Just calling ``ontospy`` without any argument launches the shell. The shell is an interactive environment that lets you import, load and inspect vocabularies. 

.. code-block:: python

    > ontospy
    
    ** OntoSPy Interactive Ontology Browser v1.6 **
    Local repository: </Users/michele.pasin/.ontospy>
    Type 'help' to get started. Use TAB to explore commands.
    <OntoSPy>: help

    Commands
    --------
    back  get  help  ls  next  quit  serialize  show  tree  zen           

    <OntoSPy>: ontology
    30 results in total: 
    [1]   7habits_centeredness.ttl
    [2]   7habits_main_schema.ttl
    [3]   bfo-1.1.owl
    [4]   bibo.owl
    [5]   blogs.ttl
    [6]   cito.rdf
    [7]   core
    [8]   fabio.rdf
    [9]   fea
    [10]   foaf.rdf
    [11]   frbr.rdf
    [12]   goodrelations.rdf
    [13]   mini_philosophy.owl
    [14]   musicontology.rdf
    [15]   npg-article-types-ontology.ttl
    [16]   npg-core-ontology.ttl
    [17]   oan
    [18]   philosophy-2006.owl
    [19]   philosophy-2007.owl
    [20]   philosurfical_2010.owl
    [21]   pizza.ttl
    [22]   semanticbible.owl
    [23]   skos.rdf
    [24]   sql.rdf
    [25]   subjects.ttl
    [26]   time.owl
    [27]   vann.rdf
    [28]   vcard.rdf
    [29]   void.rdf
    [30]   whisky.rdf
    --------------
    Please select one option by entering its number: 
    24
    Loaded /Users/michele.pasin/.ontospy/models/sql.rdf
    ----------------
    Ontologies......: 1
    Classes.........: 104
    Properties......: 11
    ..annotation....: 0
    ..datatype......: 0
    ..object........: 0
    Concepts(SKOS)..: 0
    ----------------
    http://ns.inria.fr/ast/sql#
    A vocabulary that allows SQL code abstract syntax trees to be published in RDF.
    <sql.rdf>: class predicate
    2 matching results: 
    [1]   http://ns.inria.fr/ast/sql#JoinPredicate
    [2]   http://ns.inria.fr/ast/sql#Predicate
    --------------
    Please select one option by entering its number: 
    2
    http://ns.inria.fr/ast/sql#Predicate
    Represents a collection of one or more expressions or subqueries, that may be combined with logical operators, and when evaluated returns one of the TRUE / FALSE / UNKNOWN truth values.
    ----------------
    Parents......: 1
    Children.....: 6
    Ancestors....: 1
    Descendants..: 12
    Domain of....: 0
    Range of.....: 0
    Instances....: 0
    ----------------
    <sql.rdf: Predicate>: serialize

    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://ns.inria.fr/ast/sql#Predicate> a rdfs:Class ;
        rdfs:label "Predicate"@en ;
        rdfs:comment "Represents a collection of one or more expressions or subqueries, that may be combined with logical operators, and when evaluated returns one of the TRUE / FALSE / UNKNOWN truth values."@en ;
        rdfs:isDefinedBy <http://ns.inria.fr/ast/sql#> ;
        rdfs:subClassOf <http://ns.inria.fr/ast/sql#ASTNode> .

    # etc......
    




The ``ontospy-manager`` command
*******************
This utility allows to run management operations on a local ontospy library installation. 

.. code-block:: python

    > ontospy-manager 
    OntoSPy v1.6.5
    Local library: </Users/michele.pasin/.ontospy>
    Usage: ontospy-manager <options>

    Options:
      --version        show program's version number and exit
      -h, --help       show this help message and exit
      -l, --list       Select ontologies saved in the local library.
      -u, --update     Update local library location.
      -c, --cache      Force caching of the local library (for faster loading)
      -e, --erase      Erase the local library by removing all existing files
      -i, --import     Import a file/folder/url into the local library.
      -w, --importweb  Import vocabularies registered on http://prefix.cc/popular.




