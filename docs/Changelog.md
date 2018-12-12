### Changelog

v 1.7.2
- refactoring of visualization library
- misc bug fixing

v 1.7.1
- bug fixing and improved shell command

v 1.7.0
- new: passing a directory as argument of ontospy, loads all RDF files in it (recursively)
- added dependency to 'click' library
- removed dependency on github3.py

v 1.6.9
- ontospy-shell uri => loads an interactive session only with that URI
- improved visualizations
- added Mardown export

v 1.6.8
- fixed bugs with Python3
- more visualizations outputs (3 columns, markdown)
- turtle lexer for nice printouts of source code
- ontospy -o option for exporting viz to a file

v 1.6.7
- added support for Python 3.0 (via pull request)

v 1.6.6
- fixed bug with ontospy.tests.load_local and ontospy.tests.load_remote
- removed 'display' command
- replaced 'download' command with 'import' [file, uri, repo, starter-pack]
- added 'info' command options: ['toplayer', 'parents', 'children', 'ancestors', 'descendants']
- added incremental search by passing a pattern
- serialize at ontology level now serializes the whole graph

v.1.6.5.6
- made the caching functionality version-dependent
- added 'download' command
- json serialization (via rdflib-jsonld)
- added bootstrap command for empty repos

v.1.6.5.5
- added 'visualize' command
- added delete, rename, shell commands