# Changelog

Summary of changes.

## September 10, 2018: v1.9.5

-   testjsonld command: util to send a jsonld file to https://json-ld.org/playground/

## August 30, 2018: v1.9.4

-   refactor cli using subcommands
-   add utils to load RDF and serialize to another format
-   improve caching command (to clean up cached items folder)
-   print out ontospy version info only when VERBOSE = True
-   improve handling of JSONLD (issue with serializing jsonld https://github.com/RDFLib/rdflib-jsonld/issues/42)
-   rename OntoSpy to Ontospy
-   add schema.org domainIncludes and rangeIncludes properties for building domain and ranges (https://github.com/lambdamusic/Ontospy/pull/46)
-   add shaped properties test (https://github.com/lambdamusic/Ontospy/pull/47/commits/ce9c652bd58d42d2a4be4d2de381402561176e58_)

## June 18, 2018: v1.9.2

-   improved support for JSONLD \* https://github.com/RDFLib/rdflib/issues/436
-   add html5lib to requirements

## May 18, 2018: v1.9.1

-   improved ontospy.build\*entity_from_uri()
    -   can pass custom ontospy.RDF\*Entity class as argument
    -   example: see `tests/test_methods.test4`

## May 9, 2018: v1.9

Refactoring method names:

-   all 'extract*' methods renamed as 'build*' renamed as extract_all
-   build_entity_from_uri: extract all triples for a specific URI (even if not in model) and instantiate RDF_Entity() so that it can be queried further
-   x.rdfgraph renamed as x.rdflib_graph
-   x.serialize renamed as x.rdf_source
-   tidy up all tests code
-   ontospy properties returning entities: all renamed using the all\_\* pattern eg all_classes etc..

## March 21, 2018: v1.8.8

-   fix https://github.com/lambdamusic/Ontospy/issues/33
-   instances method for classes on-demand
-   simplified describe method
-   cli: no args shows help
-   fix reference to ontodocs
-   Merge pull request #37 from satra/patch-1

## June 1, 2017

merged dev into master

-   1.8.1: sparql support and renamed various methods etc…
-   added shapes

## April 20, 2017

-   released on Pypi 1.8

## April 16, 2017

ontospy-docs created (all documentation moved to another notes file)

-   review command line interaction
-   provide simple example from python
-   complete setup.py and installation scripts requirements etc..
-   rename to ontospy-viz?

## April 13, 2017

-   clean up init file! too many things there

```
In [2]: o = ontospy.
ontospy.BOOTSTRAP_ONTOLOGIES     ontospy.SafeConfigParser         ontospy.logging
ontospy.GLOBAL_DISABLE_CACHE     ontospy.VERSION                  ontospy.os
ontospy.ONTOSPY_LIBRARY_DEFAULT  ontospy.cPickle                  ontospy.printDebug
ontospy.ONTOSPY_LOCAL            ontospy.core                     ontospy.print_function
ontospy.ONTOSPY_LOCAL_CACHE      ontospy.hostname                 ontospy.socket
ontospy.Ontospy
```

## April 3, 2017

-   released v1.7.7 wihout VIZ stuff

## March 17, 2017

-   wiki online
-   removed dependency on readline
-   version 1.7.6 published

## February 27, 2017

-   allow multi export to be passed a custom folder
    -   so that we can create a predefined ‘sample set’ of ontologies for docs
-   do another multi export with selected set of ontologies
-   publish v1.7.4
-   publish new ontospy viz outputs
    -   take a selection of outputs from ontospy viz (only good ontologies)
    -   put online eg on my webfaction
        -   http://www.michelepasin.org/support/ontospy-examples/index.html

## February 5, 2017

-   published 1.7.3, various bug fixes to viz mainly

## February 3, 2017

-   published 1.7.2
-   made a release without js interactive viz, but address all problems related to basic viz eg html rendering etc…
-   add entities-tree top level link (with sublinks?)
-   need an index.html file for each viz, not dashboard
-   footer bk color for dark themes must be removed [slate, darkly]
-   improved domain/range panel
-   add label panel or somewhere.. (for class)
-   from class button still looks weird
    <file:///Users/michele.pasin/Desktop/test2/grid-ontology-v1rdf/class-facility.html>
-   find a way to shorten long URIs, either preview them or add on the fly prefix namespaces @for later
-   clicking on ontology name open original url
-   clicking on ontospy goes to https://github.com/lambdamusic/Ontospy
-   add tree to properties too
-   allow to click on owl:Thing too to go to top level, create page for it

*   it’d be useful to show label or smth like that <file:///Users/michele.pasin/Desktop/test/vivo-isf-public-16owlrdf/class-oboero_0000020.html>
*   maybe add a label under ‘obo:BFO_0000023’

-   add tooltip to family tree diagram
-   bestDescription should join all comment/desc props
    \*\* (test using BFO)
-   clean up legacy exports
-   test update scripts for other d3 viz (for testing etc..)
-   set verbose default = False !
-   static files copy only things on demand (eg d3 only)

## November 24, 2016

-   published 1.7.1 (see git for details)

## November 21, 2016

-   updated docs
-   tested for python 3

## November 16, 2016

-   removed dependency on github3.py
-   tested on python3

## November 13, 2016

-   self.graphuri should be different from the SOURCE of the graph!
    -   rethink this.. SOURCE should be a list
-   more refactoring in RDFLoader class

## November 10, 2016

-   cli launcher for viz: check that args are passed correctly
-   cli launcher for shell: check that args are passed correctly

## November 9, 2016

-   updated setup.py
-   fixed bugs with bin launchers
-   improved config.py for ontospy-viz
-   fixed bugs with viz

## November 4, 2016

-   renamed VERSION.py
-   updated main for ontospy so to use click
    -   complete refactorin of code
    -   add way to print out more info
-   moved 'manager' actions into main ontospy launcher
-   ontologies listed by default in 2 columns

## October 21, 2016

-   improved sparql-cli by upgrading to latest pygments
    -   works ok with local file being loaded in…

## October 7, 2016

[dev-refactor]

-   updated references for viz (seem to be working)

## September 28, 2016

[dev-refactor]

-   added config.json to store visualization info
-   simplified action_visualize
-   added way to copy static files too
-   changed OWL:Thing to owl:Thing

## September 27, 2016

[dev-refactor]

-   improved markdown export
-   applied all changes previously added to <dev> branch (eg slug)
    -   in theory dev branch is behind

## September 20, 2016

-   merged dev into master
    published v 1.6.9

## August 21, 2016

Ontospy graph changes

-   added hide_base_schemas = True to Graph builder
    -   selectively decides whether to query for rdfs:, owl: classes/predicates etc.. [updated query too]
    -   improved verbose options to hide everywhere

Turtlep-prompt.py

-   bootstrapped a way to load prompt completion dynamically from RDF files

## September 16, 2016

-   removed number from slug fielnames (markdown export etc..)

## August 26, 2016

-   ontospy -r <uri>: loads an interactive session only with that URI!

## August 23, 2016

-   fixed errors with Python3
-   started using git and dev branch to make changes
-   published PyPI 1.6.8.5

## August 19, 2016

-   published PyPI 1.6.8.3

## August 18, 2016

-   completed markdown export
-   added missing namespaces to entity-graphs

## August 15, 2016

-   make export into folder <ontouri>/<viztype>/files..
-   generate MD files - started: done basic template and ontology one - @todo class, prop etc... - can do a tree? yes use ``` and outsup simple termnial tree structure
-   published PyPI 1.6.8.1

## August 11, 2016

-   added pygments to dependencies - sudo pip install pygments -U [v 2.2 for turtle lexer]
-   Added turtle lexer to docs
-   removed domain/range from split view docs

## August 11, 2016

-   added viz_splitter_multi to viz selection routine - split logic so to handle multi file saving
-   added inferred properties to viz_splitter_multi - layout still not very good @todo improve

## August 10, 2016

-   'stats' method to ontograph object
-   .slug property to onto entity (filename-safe string)
-   moved all splitter templates to /splitter/.. - updated setup.py and django set up too
-   added all entities to splitter viz - removed all splitter to selection tool

## August 7, 2016

-   started testing adding namespaces to ontology entity, so to make ontology annotations look better - done and it seem to work ok
-   started splitting files for entity-based split output

## July 29, 2016

-   added search boxes
-   refined domain/range display of properties
-   updated diagram for entities with multiple parents

## July 28, 2016

-   improved new splitter view - http://methvin.com/splitter/ [old release] - https://github.com/e1ven/jQuery-Splitter [updated for latest jquery]

## July 27, 2016

-   added -o option for exporting to a file - eg python -m ontospy.ontospy -v -o ~/Desktop/

## July 26, 2016

-   added simple graph family tree - http://thecodeplayer.com/walkthrough/css3-family-tree
-   cleaned up a bit the basic visualization
-   did basic splitter version of viz

Other family tree cool examples
http://www.gingell.com/familytree/?tree=00001
https://dl.dropboxusercontent.com/u/4151695/html/jOrgChart/example/example.html [interactive]

## July 19, 2016

-   fixed bug with dendogram json links - various other layout improvements to dendogram
-   1.6.7.4 PYPI release

## July 6, 2016

improved notably support for python 3

-   raw_input fix
-   float number division fix
-   ConfigParser fix
-   unicode method fix
-   dict slicing fix

*   v. 1.6.7.3 PYPI release

## June 22, 2016

-   added 'viz_d3bubblechart'
-   updated VISUALIZATIONS_LIST catalog
-   refactored json tree building functions
-   added several other viz for experimenting

## June 19, 2016

-   added standard way to add/test viz - eg >python -m ontospy.viz.viz_html
-   simplified way VISUALIZATIONS_LIST are managed - just import, give unique name and add
-   simplified way test_run for viz is accedded
    -   func = locals()["run"] # main func dynamically  run_test_viz(func)
-   viz_d3packhierarchy: - basic working model for viz_d3packhierarchy

## June 19, 2016

-   added new folder [viz]
-   added new static files dir structure in there - added to manifest file
-   remove support for Python 2.6 or less
-   1.6.7.3

## June 18, 2016

-   manager: updated commands and dialogs too
-   ontospy: updated commands and shortcuts

## June 17, 2016

-   loading an onto via import uri doesnt update the ls command - fixed
-   fixed bug with printTriples returning warnings
-   removed -l list from manager command
-   updated list command so to show also dates etc..

## June 15, 2016

-   completed info inferred command
-   improved headings on info command

## June 14, 2016

-   updated \_get_prompt
-   improved print outs of info colors
-   improved messages on info parents/descendants etc..

## June 13, 2016

-   added domain_of_inferred = [] and range_of_inferred = [] to classes
-   improved \_printClassDomain and \_printClassRange in shell
-   v 1.6.7.2

## June 12, 2016

-   refactored actions file

## June 6, 2016

-   Installed nose for tests - sudo pip install nose
-   Added pull request for python 3.0
-   renamed to Ontospy
-   updated docs for v 1.6.7
-   PUBLISHED v6.7

## May 27, 2016

-   added import command for local files too [from shell] - import web - import local - import repo
-   serialize at ontology level should serialize the whole thing
-   PUBLISHED v6.6

## May 6, 2016

-   added GLOBAL_DISABLE_CACHE to init.py for testing cache-less
-   updated verbose output of ontology load
-   fixed error with display of domain/ranges not in ontospy entities - eg with schema.org 'dependencies'

*   removed 'display' command
*   added info options: ['toplayer', 'parents', 'children', 'ancestors', 'descendants']
*   added incremental search by passing a pattern

## April 26, 2016

-   cleaned up ontospy.py and moved stuff into init.py
-   fixed ontospy.tests.load_local and ontospy.tests.load_remote
-   test fails with http://purl.org/dc/terms/AgentClass - fixed
-   foaf fails with inspect - fixed
-   moved zen quotes outside

## April 25, 2016

-   improve inspect for ontologies - testing adding serialization section - other improvements
-   inspect ==\* info
-   added 'download' keyword facility

## April 24, 2016

-   improved download
-   removed shell and tree commands
-   added ls <..> tree

## April 24, 2016

-   Threading removed..
-   DOCS
    -   https://pymotw.com/2/threading/
    -   http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/
    -   http://www.ibm.com/developerworks/aix/library/au-threadingpython/

Problem seems to be pyparsing, which is called by the SPARQL plugin:

```
  File "/Library/Python/2.7/site-packages/rdflib/graph.py", line 1080, in query
    query_object, initBindings, initNs, **kwargs))
  File "/Library/Python/2.7/site-packages/rdflib/plugins/sparql/processor.py", line 72, in query
    parsetree = parseQuery(strOrQuery)
  File "/Library/Python/2.7/site-packages/rdflib/plugins/sparql/parser.py", line 1052, in parseQuery
    return Query.parseString(q, parseAll=True)
  File "/Library/Python/2.7/site-packages/pyparsing.py", line 1152, in parseString
    loc, tokens = self._parse( instring, 0 )
```

TIP:

-   http://pyparsing.wikispaces.com/share/view/644825

WORKAROUND:

-   added lock = threading.Lock() before generating graph instance
-   THis works... however there is no gain in time!!!
-   should look at using thread internally instead

## April 22, 2016

-   completed new inspect command

## April 21, 2016

-   first cut at better inspect command

## April 17, 2016

-   added better printdebug info, especially for bootstrap command
-   experimented with threads

## April 11, 2016

-   add JSON LD stuff - https://github.com/RDFLib/rdflib-jsonld
-   _file_ command (contains rename and delete)
-   fixed bug with missing '/' in filenames
-   added _bootstrap_ command for empty repos

*   shell: add ARG to 'download' a specific model
    -   eg download http://www.rkbexplorer.com/ontologies/acm

## April 8, 2016

-   updated prompt
-   updated self.description on ontology load (more informative)

*   importing via 'download' the ACM fails - but if you pass the URI manually it works <http://www.rkbexplorer.com/ontologies/acm>

## March 7, 2016

-   added extra help from console run

## March 4, 2016

-   added changelog on MD file

## March 3, 2016

-   added a version-based caching mechanism

## March 2, 2016

-   import from web feature expanded
-   added 'download' command
-   renamed 'quit' into 'q'

## March 1, 2016

-   screencast
-   various other improvements

## February 26, 2016

-   pyfiglet

## February 25, 2016

-   removed render module
-   add commands for delete, rename from within shell
-   add commands for load from uri
-   add command for visualize

## February 25, 2016

-   fixed label positioning for d3 tree

## February 22, 2016

-   templates: added /components subdir
-   slider version of d3 docs

## February 19, 2016

-   refactored
-   updated html viz

## February 18, 2016

-   updated documentation with new template
    -   https://textblob.readthedocs.org/en/dev/
-   small updates to shell

## February 12, 2016

-   show qname also for list
-   version 1.6.5.1
-   fixed error with all() method retuning complex objects
-   rationalized opts lists and help methods
-   refactored messages with help\_.. mechanism
-   added 'shell' command to shell
-   moved manager up one level...

## February 8, 2016

-   added a temporary namespace abbreviation bsaed on file name
-   renamd utils to manager
-   updated docs for 1.6.5
-   released v 1.6.5 on cheeseshop

## February 7, 2016

added domain/range to export html

## February 5, 2016

-   added domain/range info to classes and properties
-   completed display of 'stats' and 'overview'

## February 4, 2016

-   fixed bug with extra '/' in path
-   moved export stuff into -e (ran from main ontospy)
-   importer has become 'ontospy-utils'

## February 3, 2016

-   added a routine to test different RDF serializations - eg so to address http://pliny.cch.kcl.ac.uk/ontology/base.owl
-   show namespaces

## February 1, 2016

-   tree: no need to show IDs anymore - solves also inconsistency with N displayed within ls command
-   add find command - like ls, but with a pattern
-   updated print triples (defined locally)
-   refactored folder structure {core/, extras/}
-   renamed /importer and /exporter
-   printGenericTree>showtype
    -   [prob this is enough not to have to show top level items to trees]

## January 15, 2016

-   updated API: tree / ls

## November 22, 2015

fixed bug with \_selectFromList

## November 3, 2015

-   started working on jumping to shell directly..
-   fixed django loading error https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
-   fixed bug with printing 2 columns results in one column with odd etc...

## November 2, 2015

-   better support of library location updating
-   added delete operation

## November 1, 2015

```
*python -m ontospy.ontospy www.w3.org/ns/oa# -i
==> FAILS - fixed error with missing 'http'
```

-   added pprint2columns to shell ontology list
-   ontospy-match: hidden
-   ontospy-searchweb: moved to 'manager'

## October 31, 2015

-   added pprint2columns to select ontology function

## October 30, 2015

-   option to select a viz output
-   added basic d3 tree viz

## October 23, 2015

-   fixed bug with 'next'
-   make models dir selectable by user

## October 23, 2015

-   added ontospy-manager
-   simplified main ontospy a lot

## October 21, 2015

-   ontospy-doc
-   added option to select from local / cache
-   added domain/range (with some limitations due to not all classes being rendered in ontospy eg owl or rdf ones )
-   added save on github option

## October 20, 2015

-   viz: shows skos concepts too

## October 18, 2015

-   changed 'repo' into 'library'
-   removed cached column from report
-   updated extraction of triples so that blank nodes are followed through
    -   eg `python -m ontospy.tools.genviz ~/.ontospy/models/time.owl`
-   in shell, added commands for toplayer, ancestors etc.....

## October 15, 2015

-   first simple w3c like documentation page like `http://xmlns.com/foaf/spec/`

## October 14, 2015

-   added python -m ontospy.tools.callviz ~/.ontospy/models/philosurfical_2010.owl
-   added a first django based templating mechanism

## October 13, 2015

-   added hidden folder /.index/cache - updated code for creation
-   added server app
-   added simple test to generate a viz from a local file
    -   python -m ontospy.hacks.callviz

## October 12, 2015

-   fixed error with http://ecoinformatics.org/oboe/oboe.1.0/oboe-core.owl when doing --import

## October 11, 2015

-   tested out python webserver - idea: put all exports into folder which is then browsed as a server

## October 10, 2015

-   make the readthedocs documentation the main one - rst, mkdown.. make it very minimal!
-   fixed error with ontospy-web circular imports - now ontospy-web is only standalone

## October 9, 2015

-   updated how to and DOCUMENTATION import ontospy etc..

## October 1, 2015

-   refactored all the code - cleaned up internal modules loading
    _ https://docs.python.org/2/tutorial/modules.html
    _ http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
-   fixed bug with --web urllib request
-   moved docs to top level

## September 17, 2015

-   next command
-   various improvements
-   fixed error with pickling max recursion exceeded

## August 22, 2015

-   redirects handling for any ontospy loading

## August 21, 2015

-   added command to create/recreate all caches eg --rebuild
-   refined action_listlocal to include dates etc...
-   added actions for skos concepts

## August 18, 2015

-   added support for SKOS
-   updated command line options

## August 17, 2015

-   began adding localization for properties
-   @todo maybe serialize and triples should work only from within a currentEntity - so we can pass also args...

## August 13, 2015

-   setup: added colorama https://pypi.python.org/pypi/colorama

## August 6, 2015

-   added more shell functionalities

## August 3, 2015

-   added new local .ontospy folder for data
-   tried pickling stuff

```
In [1]: import cPickle
In [2]: o = Graph("/Users/michele.pasin/.ontospy/semanticbible.owl")
In [13]: cPickle.dump(o, open( "/Users/michele.pasin/Desktop/save.p", "wb" ) )

# then:
In [1]: import cPickle
In [2]: o = cPickle.load(open( "/Users/michele.pasin/Desktop/save.p", "rb"))
```

## June 25, 2015

-   fixed docs errors

## June 24, 2015

-   complete quick start examples in docs
-   added docs to https://readthedocs.org/projects/ontospy/
-   add new package to PyPi

## June 24, 2015

-   did a first cut of documentation
-   removed pizza.ttl by default
-   add option to list local ontologies
-   add command line command to list prefix.cc stuff

## June 18, 2015

-   new namespaces catalog script
-   tested import paths
-   installed in local and it seems to work!

## June 16, 2015

-   completed checking the old tests
-   fixed testing of lode and frbroo

## June 15, 2015

-   refactored
-   added new test for sparql endpoints
-   added more methods on Ontology class i.e. what do we want from it? - get all classes it defines - get all properties it defines

## June 12, 2015

-   test connecting to a sparql endpoint - how to query an endpoint? are the same sparql functions useful? - https://lawlesst.github.io/notebook/rdflib-stardog.html
-   started basic integration of sparql

## June 12, 2015

-   matcher: - match not only classes but also properties against each other - better command line arguments - verbose mode too

## June 9, 2015

-   command line add option for printing label

## June 8, 2015

-   get label method: - get the english one by default! - so try to the matching with CIDOC

*   added colors and labels to tree printing
*   matcher.py : pass two ontologies, match classes
*   fixed ERROR in foaf etc.. with recursive methods

## June 6, 2015

-   cleaned up namespaces
-   removed duplicates in foaf - due to entities being defined more than once with different Class predicate (e.g. RDF or OWL)

## June 5, 2015

-   added v.2 to github DEV branch - from now on use branches to do development! - master is still the most recent active version..
-   added all command line support
-   fixed error loading http://www.cidoc-crm.org/rdfs/cidoc_crm_v5.0.2.rdfs

## June 4, 2015

-   split up annotation props vs others using rdftype val
-   added timing info
-   get domain and ranges info for objprops - attached also to classes
-   added method to run sparql query
-   optimise the allsupers/subs methods -- they really slow down queries!
-   added PARENTS/CHILDREN as the immediate relatives - then DESCENDANTS/ANCESTORS which are calculated at run time - e.g. from class / -- get parent / --recurse up until top!

## June 3, 2015

-   all supers / all subs - still using the SPARQL stuff for now. Easier..
-   added tree info for properties too

## May 15, 2015 (and previous days)

-   improved ontospy2

## May 9, 2015

-   better API = load then scan to get ontologies

## May 8, 2015

-   progress with ontospy3 - can handle multiple ontologies - added test RDF file in folder

## May 5, 2015

-   started adding docs using sphynx

## April 7, 2015

-   Fixed issue with missing templates for webviz - added data folder to manifest file - changed location of viz file to home folder (cross platform)

## March 23, 2015

-   updated the import path and removed the `vocabs` library - now the best way to import should be this:

```
In [1]: from ontospy import ontospy

In [2]: ontospy.VERSION
Out[2]: '%prog v1.2.2'
```

-   added tests - python test_simple.py

## March 19, 2015

-   new version on pypi
-   command line options -e
-   fixed readme file
-   add VERSION info on a separate file picked up by setup.py

## March 9, 2015

-   on uri2nicestring method, if the uri matches exactly a namespace it is not shortened [issue deriving from NPG portal]

## February 27, 2015

-   UPDATED_PYPI

## January 20, 2015

-   updated uri2niceString : Literals are returned as quoted strings
-   updated generation of dict representation of classes: both pred and obj are shortened using uri2niceString
-   began work on ontospy v.2 - done ontology loading bit

## January 7, 2015

-   removed utilsRDF

## October 16, 2014

-   installed package on Pypi
-   added executable: 'sketchonto' (generated via distutils)

## October 11, 2014

-   sketch: added shortcuts - (sub == rdfs:subClassOf) (class == owl:Class)
-   sketch: added commands for a default_sketch

## September 19, 2014

-   added Sketch utility
-   added a dot file export mechanism - so that we can open this stuff quickly in omniGraffle - http://paco.to/2004/omnigraffle-and-graphviz - http://en.wikipedia.org/wiki/DOT_(graph_description_language)

```
EG with labels

digraph graphname {
     a -> b [label=instanceOf];
     b -> d [label=isA];
 }
```

## September 3, 2014

-   refactored ontology loading routine

## July 10, 2014

-   added webViz method that integrates d3 stuff - to be tested more! - added the tree view template too - but data format isn't finished yet (ps check also http://bl.ocks.org/mbostock/4063570) http://bl.ocks.org/mbostock/4339184

## January 16, 2014:

Ideally, here's what I want to do:

-   load an ontology e.g. a model
-   internalize the ontology, and be able to query a knowledge base (or the same ontology file) using that model - e.g. autocomplete on properties (=dont have to remember all the model details) - e.g. introspection kind of stuff
