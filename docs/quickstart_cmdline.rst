Command Line Tools
************************
A few examples of how to use the command line utilities that come with OntoSPy. 

Currently these are the utility scripts available: 

- ``ontospy``: load a graph and show schema information
- ``ontospy-docs``: generates html documentation  
- ``ontospy-shell``: launch the interactive ontospy shell  
- ``ontospy-web``: discover commonly used ontologies listed on prefix.cc 
- ``ontospy-match``: bootstrap mappings between two vocabularies
- ``ontospy-sketch``: sketch a turtle model interactively


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


Getting help
---------------------------------------------

.. code-block:: shell

	> ontospy -h
	OntoSPy v1.6.1
	Usage: ontospy <ontology-file-or-uri> [options]

	Options:
	  --version   show program's version number and exit
	  -h, --help  show this help message and exit
	  --shell     Interactive explorer of the ontologies in the local repository
	  --repo      List ontologies in the local repository
	  --import    Imports file/folder/url into the local repository
	  --cache     Rebuild the cache for the local repository
	  --reset     Resets the local repository by removing all existing files
	  -a          Print the ontology annotations/metadata.
	  -c          Print the class taxonomy.
	  -p          Print the property taxonomy.
	  -s          Print the SKOS taxonomy.
	  -l          Print entities labels as well as URIs (used with -c or -p or
	              -s).
                  
                  

Print options  
---------------------------------------------
E.g. print only the class tree and show rdfs:labels 

.. code-block:: shell

    > ontospy foaf.rdf -c -l
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
    Metadata:

    http://xmlns.com/foaf/0.1/
    => http://purl.org/dc/elements/1.1/title
    .... Friend of a Friend (FOAF) vocabulary
    => http://www.w3.org/1999/02/22-rdf-syntax-ns#type
    .... http://www.w3.org/2002/07/owl#Ontology
    => http://purl.org/dc/elements/1.1/description
    .... The Friend of a Friend (FOAF) RDF vocabulary, described using W3C RDF Schema and the Web Ontology Language.

    Class Taxonomy
    ----------
    http://www.w3.org/2000/10/swap/pim/contact#Person ("Person")
    ----foaf:Person ("Person")
    http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing ("Spatial Thing")
    ----foaf:Person ("Person")
    foaf:Agent ("Agent")
    ----foaf:Group ("Group")
    ----foaf:Organization ("Organization")
    ----foaf:Person ("Person")
    foaf:Document ("Document")
    ----foaf:Image ("Image")
    ----foaf:PersonalProfileDocument ("PersonalProfileDocument")
    foaf:LabelProperty ("Label Property")
    foaf:OnlineAccount ("Online Account")
    ----foaf:OnlineChatAccount ("Online Chat Account")
    ----foaf:OnlineEcommerceAccount ("Online E-commerce Account")
    ----foaf:OnlineGamingAccount ("Online Gaming Account")
    foaf:Project ("Project")
    ----------
    Time:	   2.77s


The ``ontospy-docs`` command
*******************
This utility allows to generate html documentation for any ontology. 

.. code-block:: python
    > ontospy-docs 
    OntoSPy v1.6.2.2
    Local library: </Users/michele.pasin/.ontospy>
    Usage: ontospy-doc <uri>

    Options:
      --version      show program's version number and exit
      -h, --help     show this help message and exit
      -l, --library  Select an ontology from local library.
      -g, --gist     Save output as a Github Gist.

Just pass it a URI, or use the -l option to load one of the models previously saved in the local library. 

The -g option allows to save the documentation file as a github gist. 




The ``ontospy-shell`` command
*******************
The shell is an interactive environment that lets you import, load and inspect vocabularies. 

.. code-block:: python

    > ontospy-shell
    
    ** OntoSPy Interactive Ontology Documentation Environment v1.6.1 **
    Local repository: </Users/michele.pasin/.ontospy>
    Type 'help' to get started. Use TAB to explore commands.
    <OntoSPy>: help

    Commands
    --------
    annotations  currentEntity    help      quit       tree   
    class        currentOntology  ontology  serialize  triples
    concept      delete           property  summary    up     
    next         zen            

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
    



The ``ontospy-web`` command
*******************

Show a list of vocabularies registered on http://prefix.cc


.. code-block:: shell

    > ontospy-web -h

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -a, --all   Show all entries found by querying http://prefix.cc/popular/all.
      -q QUERY    A query string used to match the catalog entries.


Pass an argument to show only ontology that match it:

.. code-block:: shell

    > ontospy-web -q agent
    ----------
    Reading source...
    ----------
    Loaded 6497 triples from <http://prefix.cc/popular/all.file.vann>
    started scanning...
    ----------
    Ontologies found: 1624
    Classes found...: 0
    Properties found: 0
    Annotation......: 0
    Datatype........: 0
    Object..........: 0
    ----------
    3 results found.
    agents  ==>  http://eulersharp.sourceforge.net/2003/03swap/agent#
    swanag  ==>  http://purl.org/swan/1.2/agents/
    agent  ==>  http://eulersharp.sourceforge.net/2003/03swap/agent#
    ----------
    Time:      10.04s






The ``ontospy-match`` command
*******************

Match two models (in development)

.. code-block:: python

    > ontospy-match -h
    Usage: 

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTPUTFILE, --outputfile=OUTPUTFILE
                            The name of the output csv file.
      -v, --verbose         Verbose mode: prints results on screen too.

                            

    
    > ontospy-match data/schemas/foaf.rdf data/schemas/bibo.owl 
    Match classes or properties? [c|p]: c
    ----------
    Loaded 630 triples from <data/schemas/foaf.rdf>
    started scanning...
    ----------
    Ontologies found: 1
    Classes found...: 15
    Properties found: 67
    Annotation......: 7
    Datatype........: 26
    Object..........: 34
    ----------
    Loaded 1215 triples from <data/schemas/bibo.owl>
    started scanning...
    ----------
    Ontologies found: 1
    Classes found...: 65
    Properties found: 117
    Annotation......: 12
    Datatype........: 54
    Object..........: 51
    ----------
    Now matching...
    31 candidates found.
    ----------
    Time:	   7.14s

    # results are saved by default in same folder
    



