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

## Generating ontology documentation

Ontospy can be used to generate HTML documentation for an ontology pretty easily. E.g. see the [Schema.org](http://www.michelepasin.org/support/ontospy-examples/schema_org_topbraidttl/index.html) ontology, or [FOAF](http://www.michelepasin.org/support/ontospy-examples/foafrdf/index.html) ontology.

This functionality relies on a module called _ontodocs_, which used to be maintained as a separate library but is now distributed with ontospy as an add-on:

-   `pip install ontospy[HTML]`

For more examples of the kind of documentation that can be generated out-of-the-box, [take a look at this page](http://www.michelepasin.org/support/ontospy-examples/index.html).

## More info

http://lambdamusic.github.io/Ontospy/
