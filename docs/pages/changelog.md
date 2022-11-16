# Changelog

Summary of changes.

## Nov, 2022: v 2.1.0

- D3 visualizations improvements
    - Split pages for different object types
    - Refactor code

## Oct, 2022: v 2.0.0

Full release of version 2. The main library API is the same, but various internals have changed hence this release may be backward-incompatible for users that have custom extensions using Ontospy's source. 

- Remove all Django dependencies, replaced with [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/intro/#installation)
- Rename `ontodocs` module to `gendocs`
- Drop support for python2 
- Remove `setup.cfg` and universal build (only py3)
- Refactor code / clean up 
- Refactor `setup.py` 

## May, 2022: v 2.0.0-alpha

An alpha release of 2.0.0. More refactoring and code improvement is planned before the full 2.0.0 release!

- Merged additional SHACL support branch [pull-107](https://github.com/lambdamusic/Ontospy/pull/107)
- Fix error loading JSONLD graphs [issue-1416](https://github.com/lambdamusic/Ontospy/issues/102)
- Replace lov.okfn.org [issue-110](https://github.com/lambdamusic/Ontospy/issues/110)

## December, 2021: v 1.9.9.4

- Remove deprecated `Ontospy.__computeTopLayer`
- Refactor `Ontospy.get_class` and related methods so to have less duplicated code
  - Added `Ontospy.get_shapes`
- Refactor `Ontospy.nextClass` and related methods so to have less duplicated code
- Refactor `Ontospy.ontologyClassTree` and related methods so to have less duplicated code
- Improve `Ontospy.get_shapes` so that it enforces URI uniqueness only among shapes URIs. This sets the ground for [pull-107](https://github.com/lambdamusic/Ontospy/pull/107).  
- Refactor tests code and clean up tests rdf folder
  - Add `uco_monolithic.ttl` and `scigraph` for shapes tests

## December, 2021: v 1.9.9.3

- Fix bug: https://github.com/lambdamusic/Ontospy/issues/105

## November, 2021: v 1.9.9.2

- Add ability to extract individuals (instances) 
  - `-i` option from command line
  - `hide_individuals=False` parameter in `Ontospy`
- All gendocs visualizations updated so to handle instances
- Improve handling of multi-ontology graphs: ontologies list ordered alphabetically by default
- Add `format` parameter to `scan` command
- Fix for `--verbose` option 

## September, 2021: v 1.9.9

- add `pref_title` and `pref_language` options to ontospy
- update CLI to accept these parameters for documentation generation 
    * eg `ontospy gendocs -l --preflabel label` 
- improve all viz templates to use user provided titles 
- add `|linebreaks` to bestDescription method for better rendering
- various code improvements for tests


## July, 2019: v1.9.8.3

-  `gendocs` option: `no browser` prevents opening html viz in browser 
-  `gendocs -l` added as shortcut of `--lib`


## December, 2018: v1.9.8.1

-   ad hoc ordering of commands
-   examine becomes `scan`

## December, 2018: v1.9.8

-   small bug fixes
-   refactor action visualize / activated 'alpha' dataviz
    -   allow to pass viztype from command line
-   implicit/explicit classes and predicates switch `-x`
    -   this is useful to inspect a small RDF snippet for example too see what predicates are being used
-   option to show raw RDF data `-r`
-   improvements to `shell` command
-   namespaces printed out by default

## December, 2018: v1.9.7

-   removed support for Python 2
-   fixed issue with serialization print
-   comments all go to sterr by default
    => eg now easier to to `ontospy serialize foaf.rdf json-ld > ~/foaf.json`
-   embedded ontodocs plugin within main source code
    -   requires install with `[HTML]` flag
-   `utils` and `quickdocs` commands added to CLI
-   CLI: all commands when called default to HELP
-   fix bug for retrieving ontologies from online repos

## November, 2018: v1.9.6

-   refactoring and tested integration with ontodocs
-   allow calling dataviz (ontodocs) from CLI
-   bug fixing

## November, 2018: v1.9.5.2

-   bug fix for scan command

## October, 2018: v1.9.5.1

-   bug fix with urllib.parse.quote (python3)

## September, 2018: v1.9.5

-   `testjsonld` command: util to send a jsonld file to https://json-ld.org/playground/

## August, 2018: v1.9.4

-   refactor cli using subcommands
-   add utils to load RDF and serialize to another format
-   improve caching command (to clean up cached items folder)
-   print out ontospy version info only when VERBOSE = True
-   improve handling of JSONLD (issue with serializing jsonld https://github.com/RDFLib/rdflib-jsonld/issues/42)
-   rename OntoSpy to Ontospy
-   add schema.org domainIncludes and rangeIncludes properties for building domain and ranges (https://github.com/lambdamusic/Ontospy/pull/46)
-   add shaped properties test (https://github.com/lambdamusic/Ontospy/pull/47/commits/ce9c652bd58d42d2a4be4d2de381402561176e58_)

## June, 2018: v1.9.2

-   improved support for JSONLD \* https://github.com/RDFLib/rdflib/issues/436
-   add html5lib to requirements

## May, 2018: v1.9.1

-   improved ontospy.build\*entity_from_uri()
    -   can pass custom ontospy.RDF\*Entity class as argument
    -   example: see `tests/test_methods.test4`

## May, 2018: v1.9

Refactoring method names:

-   all 'extract*' methods renamed as 'build*' renamed as extract_all
-   build_entity_from_uri: extract all triples for a specific URI (even if not in model) and instantiate RDF_Entity() so that it can be queried further
-   x.rdfgraph renamed as x.rdflib_graph
-   x.serialize renamed as x.rdf_source
-   tidy up all tests code
-   ontospy properties returning entities: all renamed using the all\_\* pattern eg all_classes etc..

## March, 2018: v1.8.8

-   fix https://github.com/lambdamusic/Ontospy/issues/33
-   instances method for classes on-demand
-   simplified describe method
-   cli: no args shows help
-   fix reference to ontodocs
-   Merge pull request #37 from satra/patch-1

## June, 2017: v1.8.1

-   sparql support and renamed various methods etc…
-   added shapes

## April, 2017: v 1.8

- ontospy-docs created (all documentation moved to another notes file)
-   review command line interaction
-   provide simple example from python
-   complete setup.py and installation scripts requirements etc..
-   rename to ontospy-viz?
-   clean up init file! too many things there

## April, 2017: v1.7.7 

- remove VIZ stuff

## March, 2017: v1.7.6

-   wiki online
-   removed dependency on readline for non-shell usage

## February, 2017: v1.7.4

-   allow multi export to be passed a custom folder
    -   so that we can create a predefined ‘sample set’ of ontologies for docs
-   do another multi export with selected set of ontologies
-   publish new ontospy viz outputs
    -   take a selection of outputs from ontospy viz (only good ontologies)
    -   put online 
-   made a release without js interactive viz, but address all problems related to basic viz eg html rendering etc…
-   add entities-tree top level link (with sublinks?)
-   need an index.html file for each viz, not dashboard
-   footer bk color for dark themes must be removed [slate, darkly]
-   improved domain/range panel
-   add label panel or somewhere.. (for class)
-   from class button still looks weird
-   find a way to shorten long URIs, either preview them or add on the fly prefix namespaces @for later
-   clicking on ontology name open original url
-   clicking on ontospy goes to https://github.com/lambdamusic/Ontospy
-   add tree to properties too
-   allow to click on owl:Thing too to go to top level, create page for it
-   add tooltip to family tree diagram
-   bestDescription should join all comment/desc props
    \*\* (test using BFO)
-   clean up legacy exports
-   test update scripts for other d3 viz (for testing etc..)
-   set verbose default = False !
-   static files copy only things on demand (eg d3 only)

## November, 2016: v1.7.1

-   published 1.7.1 (see git for details)
-   updated docs
-   tested for python 3
-   removed dependency on github3.py
-   tested on python3
-   self.graphuri should be different from the SOURCE of the graph!
-   more refactoring in RDFLoader class
-   cli launcher for viz: check that args are passed correctly
-   cli launcher for shell: check that args are passed correctly
-   updated setup.py
-   fixed bugs with bin launchers
-   improved config.py for ontospy-viz
-   fixed bugs with viz
-   renamed VERSION.py
-   updated main for ontospy so to use click
    -   complete refactorin of code
    -   add way to print out more info
-   moved 'manager' actions into main ontospy launcher
-   ontologies listed by default in 2 columns
-   improved sparql-cli by upgrading to latest pygments
    -   works ok with local file being loaded in…


## September, 2016: v1.6.9

-   improved markdown export
-   applied all changes previously added to <dev> branch (eg slug)
    -   in theory dev branch is behind
-   added config.json to store visualization info
-   simplified action_visualize
-   added way to copy static files too
-   changed OWL:Thing to owl:Thing
-  Ontospy graph changes
-   added hide_base_schemas = True to Graph builder
    -   selectively decides whether to query for rdfs:, owl: classes/predicates etc.. [updated query too]
    -   improved verbose options to hide everywhere
- Turtlep-prompt.py
-   bootstrapped a way to load prompt completion dynamically from RDF files
-   removed number from slug fielnames (markdown export etc..)
-   ontospy -r <uri>: loads an interactive session only with that URI!


## August, 2016: v1.6.8

-   completed markdown export
-   added missing namespaces to entity-graphs
-   make export into folder <ontouri>/<viztype>/files..
-   generate MD files - started: done basic template and ontology one - @todo class, prop etc... - can do a tree? yes use ``` and outsup simple termnial tree structure
-   added pygments to dependencies - sudo pip install pygments -U [v 2.2 for turtle lexer]
-   Added turtle lexer to docs
-   removed domain/range from split view docs
-   added viz_splitter_multi to viz selection routine - split logic so to handle multi file saving
-   added inferred properties to viz_splitter_multi - layout still not very good @todo improve
-   'stats' method to ontograph object
-   .slug property to onto entity (filename-safe string)
-   moved all splitter templates to /splitter/.. - updated setup.py and django set up too
-   added all entities to splitter viz - removed all splitter to selection tool
-   started testing adding namespaces to ontology entity, so to make ontology annotations look better - done and it seem to work ok
-   started splitting files for entity-based split output
-   added search boxes
-   refined domain/range display of properties
-   updated diagram for entities with multiple parents
-   improved new splitter view - http://methvin.com/splitter/ [old release] - https://github.com/e1ven/jQuery-Splitter [updated for latest jquery]
-   added -o option for exporting to a file - eg python -m ontospy.ontospy -v -o ~/Desktop/
-   added simple graph family tree - http://thecodeplayer.com/walkthrough/css3-family-tree
-   cleaned up a bit the basic visualization
-   did basic splitter version of viz


## July, 2016: v1.6.7

-   fixed bug with dendogram json links - various other layout improvements to dendogram
-   raw_input fix
-   float number division fix
-   ConfigParser fix
-   unicode method fix
-   dict slicing fix
-   added 'viz_d3bubblechart'
-   updated VISUALIZATIONS_LIST catalog
-   refactored json tree building functions
-   added several other viz for experimenting
-   added standard way to add/test viz - eg >python -m ontospy.viz.viz_html
-   simplified way VISUALIZATIONS_LIST are managed - just import, give unique name and add
-   simplified way test_run for viz is accedded
    -   func = locals()["run"] # main func dynamically run_test_viz(func)
-   viz_d3packhierarchy: - basic working model for viz_d3packhierarchy
-   added new folder [viz]
-   added new static files dir structure in there - added to manifest file
-   remove support for Python 2.6 or less
-   manager: updated commands and dialogs too
-   ontospy: updated commands and shortcuts
-   loading an onto via import uri doesnt update the ls command - fixed
-   fixed bug with printTriples returning warnings
-   removed -l list from manager command
-   updated list command so to show also dates etc..
-   completed info inferred command
-   improved headings on info command
-   updated \_get_prompt
-   improved print outs of info colors
-   improved messages on info parents/descendants etc..
-   added domain_of_inferred = [] and range_of_inferred = [] to classes
-   improved \_printClassDomain and \_printClassRange in shell


## May, 2016: v1.6.6

-   added import command for local files too [from shell] - import web - import local - import repo
-   serialize at ontology level should serialize the whole thing
-   added GLOBAL_DISABLE_CACHE to init.py for testing cache-less
-   updated verbose output of ontology load
-   fixed error with display of domain/ranges not in ontospy entities - eg with schema.org 'dependencies'
*   removed 'display' command
*   added info options: ['toplayer', 'parents', 'children', 'ancestors', 'descendants']
*   added incremental search by passing a pattern
-   cleaned up ontospy.py and moved stuff into init.py
-   fixed ontospy.tests.load_local and ontospy.tests.load_remote
-   test fails with http://purl.org/dc/terms/AgentClass - fixed
-   foaf fails with inspect - fixed
-   moved zen quotes outside
-   improve inspect for ontologies - testing adding serialization section - other improvements
-   inspect ==\* info
-   added 'download' keyword facility
-   improved download
-   removed shell and tree commands
-   added ls <..> tree
-   Threading removed..
-   completed new inspect command
-   added better printdebug info, especially for bootstrap command
-   experimented with threads
-   add JSON LD stuff - https://github.com/RDFLib/rdflib-jsonld
-   _file_ command (contains rename and delete)
-   fixed bug with missing '/' in filenames
-   added _bootstrap_ command for empty repos
*   shell: add ARG to 'download' a specific model
    -   eg download http://www.rkbexplorer.com/ontologies/acm
-   added extra help from console run
-   added changelog on MD file
-   added a version-based caching mechanism
-   import from web feature expanded
-   added 'download' command
-   renamed 'quit' into 'q'
-   screencast
-   various other improvements
-   pyfiglet
-   removed render module
-   add commands for delete, rename from within shell
-   add commands for load from uri
-   add command for visualize


## February, 2016: v1.6.5

-   updated documentation with new template
    -   https://textblob.readthedocs.org/en/dev/
-   small updates to shell
-   show qname also for list
-   fixed error with all() method retuning complex objects
-   rationalized opts lists and help methods
-   refactored messages with help\_.. mechanism
-   added 'shell' command to shell
-   moved manager up one level...
-   added a temporary namespace abbreviation bsaed on file name
-   renamd utils to manager
-   added domain/range info to classes and properties
-   completed display of 'stats' and 'overview'
-   fixed bug with extra '/' in path
-   moved export stuff into -e (ran from main ontospy)
-   importer has become 'ontospy-utils'
-   added a routine to test different RDF serializations - eg so to address http://pliny.cch.kcl.ac.uk/ontology/base.owl
-   show namespaces
-   tree: no need to show IDs anymore - solves also inconsistency with N displayed within ls command
-   add find command - like ls, but with a pattern
-   updated print triples (defined locally)
-   refactored folder structure {core/, extras/}
-   renamed /importer and /exporter
-   printGenericTree>showtype
    -   [prob this is enough not to have to show top level items to trees]
-   updated API: tree / ls
-   fixed django loading error https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
-   fixed bug with printing 2 columns results in one column with odd etc...
-   better support of library location updating
-   added delete operation
-   added pprint2columns to select ontology function
-   option to select a viz output
-   added basic d3 tree viz
-   fixed bug with 'next'
-   make models dir selectable by user
-   added ontospy-manager
-   simplified main ontospy a lot

## October, 2015: v1.6.4

-   ontospy-doc
-   added option to select from local / cache
-   added domain/range (with some limitations due to not all classes being rendered in ontospy eg owl or rdf ones )
-   added save on github option
-   viz: shows skos concepts too
-   changed 'repo' into 'library'
-   removed cached column from report
-   updated extraction of triples so that blank nodes are followed through
    -   eg `python -m ontospy.tools.genviz ~/.ontospy/models/time.owl`
-   in shell, added commands for toplayer, ancestors etc.....
-   first simple w3c like documentation page like `http://xmlns.com/foaf/spec/`
-   added python -m ontospy.tools.callviz ~/.ontospy/models/philosurfical_2010.owl
-   added a first django based templating mechanism
-   added hidden folder /.index/cache - updated code for creation
-   added server app
-   added simple test to generate a viz from a local file
    -   python -m ontospy.hacks.callviz
-   fixed error with http://ecoinformatics.org/oboe/oboe.1.0/oboe-core.owl when doing --import
-   tested out python webserver - idea: put all exports into folder which is then browsed as a server
-   make the readthedocs documentation the main one - rst, mkdown.. make it very minimal!
-   fixed error with ontospy-web circular imports - now ontospy-web is only standalone
-   updated how to and DOCUMENTATION import ontospy etc..
-   refactored all the code - cleaned up internal modules loading
    _ https://docs.python.org/2/tutorial/modules.html
    _ http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
-   fixed bug with --web urllib request
-   moved docs to top level
-   next command
-   various improvements
-   fixed error with pickling max recursion exceeded
-   redirects handling for any ontospy loading

## August, 2015, v1.6.3

-   added command to create/recreate all caches eg --rebuild
-   refined action_listlocal to include dates etc...
-   added actions for skos concepts
-   added support for SKOS
-   updated command line options
-   began adding localization for properties
-   @todo maybe serialize and triples should work only from within a currentEntity - so we can pass also args...
-   setup: added colorama https://pypi.python.org/pypi/colorama
-   added more shell functionalities
-   added new local .ontospy folder for data
-   tried pickling stuff


## June, 2015, v1.6

-   fixed docs errors
-   complete quick start examples in docs
-   added docs to https://readthedocs.org/projects/ontospy/
-   add new package to PyPi
-   did a first cut of documentation
-   removed pizza.ttl by default
-   add option to list local ontologies
-   add command line command to list prefix.cc stuff
-   new namespaces catalog script
-   tested import paths
-   installed in local and it seems to work!
-   completed checking the old tests
-   fixed testing of lode and frbroo
-   added new test for sparql endpoints
-   added more methods on Ontology class i.e. what do we want from it? - get all classes it defines - get all properties it defines
-   test connecting to a sparql endpoint - how to query an endpoint? are the same sparql functions useful? - https://lawlesst.github.io/notebook/rdflib-stardog.html
-   started basic integration of sparql
-   matcher: - match not only classes but also properties against each other - better command line arguments - verbose mode too
-   command line add option for printing label
-   get label method: - get the english one by default! - so try to the matching with CIDOC
*   added colors and labels to tree printing
*   matcher.py : pass two ontologies, match classes
*   fixed ERROR in foaf etc.. with recursive methods
-   cleaned up namespaces
-   removed duplicates in foaf - due to entities being defined more than once with different Class predicate (e.g. RDF or OWL)
-   added v.2 to github DEV branch - from now on use branches to do development! - master is still the most recent active version..
-   added all command line support
-   fixed error loading http://www.cidoc-crm.org/rdfs/cidoc_crm_v5.0.2.rdfs
-   split up annotation props vs others using rdftype val
-   added timing info
-   get domain and ranges info for objprops - attached also to classes
-   added method to run sparql query
-   optimise the allsupers/subs methods -- they really slow down queries!
-   added PARENTS/CHILDREN as the immediate relatives - then DESCENDANTS/ANCESTORS which are calculated at run time - e.g. from class / -- get parent / --recurse up until top!


## Mar, 2015, v1.1

-   all supers / all subs - still using the SPARQL stuff for now. Easier..
-   added tree info for properties too
-   better API = load then scan to get ontologies
-   progress with ontospy3 - can handle multiple ontologies - added test RDF file in folder
-   started adding docs using sphynx
-   Fixed issue with missing templates for webviz - added data folder to manifest file - changed location of viz file to home folder (cross platform)
-   updated the import path and removed the `vocabs` library - now the best way to import should be this:
-   added tests - python test_simple.py
-   on uri2nicestring method, if the uri matches exactly a namespace it is not shortened [issue deriving from NPG portal]

## January, 2015, v1.0

-   updated uri2niceString : Literals are returned as quoted strings
-   updated generation of dict representation of classes: both pred and obj are shortened using uri2niceString
-   began work on ontospy v.2 - done ontology loading bit
-   removed utilsRDF

## October, 2014, v0.8

-   installed package on Pypi
-   added executable: 'sketchonto' (generated via distutils)
-   sketch: added shortcuts - (sub == rdfs:subClassOf) (class == owl:Class)
-   sketch: added commands for a default_sketch
-   added Sketch utility
-   added a dot file export mechanism - so that we can open this stuff quickly in omniGraffle - http://paco.to/2004/omnigraffle-and-graphviz - http://en.wikipedia.org/wiki/DOT_(graph_description_language)
-   refactored ontology loading routine

## July, 2014: v0.5

-   added webViz method that integrates d3 stuff - to be tested more! - added the tree view template too - but data format isn't finished yet (ps check also http://bl.ocks.org/mbostock/4063570) http://bl.ocks.org/mbostock/4339184

## Jan, 2014: v0.1

Ideally, here's what I want to do:

-   load an ontology e.g. a model
-   internalize the ontology, and be able to query a knowledge base (or the same ontology file) using that model - e.g. autocomplete on properties (=dont have to remember all the model details) - e.g. introspection kind of stuff
