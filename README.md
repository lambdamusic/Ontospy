# Ontospy

Python library and command-line interface for inspecting and visualizing RDF models.


#### Links

-   [Pypi](https://pypi.org/project/ontospy/)
-   [Github](https://github.com/lambdamusic/ontospy)
-   [Docs](http://lambdamusic.github.io/Ontospy/)
-   [Changelog](http://lambdamusic.github.io/Ontospy/pages/changelog.html)
-   [YouTube](https://youtu.be/MkKrtVHi_Ks)

# Description

Ontospy is a lightweight Python library and command line tool for inspecting and visualizing vocabularies encoded using W3C Semantic Web standards, that is, RDF or any of its dialects (RDFS, OWL, SKOS).

The basic workflow is simple: load a graph by instantiating the `Ontospy` class with a file containing RDFS, OWL or SKOS definitions. You get back a object that lets you interrogate the ontology. That's all!

The same functionalities are accessible also via a command line application. This is an interactive environment (like a repl) that allows to load ontologies from a local repository, interrogate them and cache them so that they can be quickly reloaded for inspection later on.

[![Downloads](https://pepy.tech/badge/ontospy)](https://pepy.tech/project/ontospy)


## Generating ontology documentation

Ontospy can be used to generate HTML documentation for an ontology pretty much out-of-the-box. 

See the website [Examples of ontology documentation generated via Ontospy](https://lambdamusic.github.io/ontospy-examples/index.html), or jump straight to the sample [CIDOC-CRM](https://lambdamusic.github.io/ontospy-examples/cidoccrm_ecrm-2022-11owlxml/index.html) or [FOAF](https://lambdamusic.github.io/ontospy-examples/foafrdf/index.html) documentation pages.

> From version 2.0, the documentation generation libraries are installed by default with Ontospy. Previously, third party dependencies (e.g. Django) had to be installed separately. 

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
