Quick Start - Command Line
************************
A few examples of how to use the command line utilities that come with OntoSPy. 

Note: if you install OntosPy via one of the suggested methods, appropriate executables for your platform should be compiled automatically and added to `usr/local/bin` (on unix-based systems, or similar on windows). 

Currenlty the utility scripts available are 4: 

- ``ontospy``: load a graph and show schema information.
- ``ontospy-catalog``: discover commonly used ontologies. 
- ``ontospy-match``: bootstrap mappings between two models.
- ``ontospy-sketch``: sketch a turtle model interactively.

  
.. warning::
    This documentation is still in draft mode. 



The ``ontospy`` utility
+++++++++++++++++++++++++++++++

>python ontospy.py http://xmlns.com/foaf/spec/

# resolves redirects and prints info


Include labels in property tree
---------------------------------------------

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




The ``ontospy-catalog`` utility
+++++++++++++++++++++++++++++++

Show a list of ontologies from the web


.. code-block:: shell

    python tools/catalog.py
    Usage: python ontospy/tools/catalog.py

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -a, --all   Show all entries found by querying http://prefix.cc/popular/all.
      -q QUERY    A query string used to match the catalog entries.


Pass an argument to show only ontology that match it:

.. code-block:: shell

    python tools/catalog.py -q agent
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






The ``ontospy-match`` utility
+++++++++++++++++++++++++++++++

Match two models (in development)

.. code-block:: python

    ontospy> python tools/matcher.py data/schemas/foaf.rdf data/schemas/bibo.owl 
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
    
    > python tools/matcher.py -h
    Usage: 

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTPUTFILE, --outputfile=OUTPUTFILE
                            The name of the output csv file.
      -c CONFIDENCE, --confidence=CONFIDENCE
                            @TODO 0.1-0.9 degree of confidence for similarity
                            matching.
                            



