# Ontospy

Python library and command-line interface for inspecting and visualizing RDF models.


#### Links

-   [Pypi](https://pypi.org/project/ontospy/)
-   [Github](https://github.com/lambdamusic/ontospy)
-   [Docs](http://lambdamusic.github.io/Ontospy/)
-   [YouTube Video](https://youtu.be/MkKrtVHi_Ks)

# Description

Ontospy is a lightweight Python library and command line tool for inspecting and visualizing vocabularies encoded using W3C Semantic Web standards, that is, RDF or any of its dialects (RDFS, OWL, SKOS).

The basic workflow is simple: load a graph by instantiating the `Ontospy` class with a file containing RDFS, OWL or SKOS definitions. You get back a object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via a command line application (`ontospy`). This is an interactive environment (like a repl) that allows to load ontologies from a local repository, interrogate them and cache them so that they can be quickly reloaded for inspection later on.

[![Downloads](https://pepy.tech/badge/ontospy)](https://pepy.tech/project/ontospy)


## Generating ontology documentation

Ontospy can be used to generate HTML documentation for an ontology pretty easily. E.g. see the [Schema.org](https://lambdamusic.github.io/ontospy-examples/schema_org_topbraidttl/index.html) ontology, or [FOAF](https://lambdamusic.github.io/ontospy-examples/foafrdf/index.html) ontology.

This functionality relies on a module called _ontodocs_, which used to be maintained as a separate library but is now distributed with ontospy as an add-on:

-   `pip install ontospy[HTML]`

For more examples of the kind of documentation that can be generated out-of-the-box, [take a look at this page](https://lambdamusic.github.io/ontospy-examples/index.html).

## Status

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

I have little time to spend on this project these days, so I'm mainly focusing on bug fixes and maintenance. Happy to review PRs if you want to add more functionalities! 

## Development

```
# git clone the repo first
$ mkvirtualenv ontospy
$ pip install -r requirements.txt
$ pip install -e .
```

## Documentation

http://lambdamusic.github.io/Ontospy/
