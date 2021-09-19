![logo](static/logo_sm.jpg)

## Index

- [Index](#index)
- [Welcome to Ontospy's Documentation!](#welcome-to-ontospys-documentation)
- [In a Nutshell](#in-a-nutshell)
- [Installation](#installation)
- [Quick Example](#quick-example)
- [Is Ontospy for Me?](#is-ontospy-for-me)
- [Generating Ontology Documentation](#generating-ontology-documentation)
- [Miscellaneous Tips](#miscellaneous-tips)
- [Quick Links](#quick-links)

## Welcome to Ontospy's Documentation!

Ontospy is a lightweight Python library and command line tool for working with vocabularies encoded in the [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) family of languages.

> Note: this documentation is still a work-in-progress

## In a Nutshell

Ontospy can be used either as an interactive command line interface (a
[repl](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>)) or as a Python package.

Calling the `ontospy` command from a terminal window launches a utility for scanning a knowledge model encoded in RDF (or any of its dialects e.g. RDFS, OWL or SKOS).

For example, if you pass a valid graph URI:

```bash
$ ontospy scan http://purl.org/spar/frbr
```

Ontospy will extract and print out any ontology-related information contained in that graph.

Many other options are available, in particular Ontospy allows to load/save ontologies from/to a local repository so that they can be cached and quickly reloaded for inspection later on. All without leaving your terminal window!

[![OntospyVideo](static/ontospyvideo_sm.jpg)](https://youtu.be/MkKrtVHi_Ks)

## Installation

Prerequisites:

-   Python (3.x)
-   A python package manager: [setuptools](https://pypi.python.org/pypi/setuptools) or [pip](https://pip.pypa.io/en/stable/installing/).

Once you have a package manager installed, simply install Ontospy from the Python Package Index. There are three library versions you can choose from.

**Lightweight Version**

If you want less library dependencies (eg because you want to include Ontospy in another project and don't care about html documentation), you can simply install the core library only:

```bash
$ pip install ontospy
```

The python library, its dependencies and all of its command-line executables will be installed. The only thing which is left out is the documentation-generation feature.

**Lightweight Version plus Shell**

The 'shell' or interactive command line interface requires the [readline](https://pypi.org/project/readline/) module, a set of functions for use by applications that allow users to edit command lines as they are typed in.  

This module is optionally installed with Ontospy like this:

```bash
$ pip install ontospy[SHELL]
```

**Full Version**

If you want to use ontospy to automatically create some [HTML documentation](<(#generating-ontology-documentation)>) for an ontology, you should install the FULL version of the library like this:

```bash
$ pip install ontospy[FULL]
```

The full version includes more files (eg html templates) and it has a larger footprint as it relies on Django and other libraries. 


**Upgrading**

If you’re upgrading from an older version, make sure you use the -U flag:

```bash
$ pip install ontospy -U
```

## Quick Example

If used as a Python package, the basic workflow is the following: load a graph by instantiating the `Ontospy` class with a file containing RDFS, OWL or SKOS definitions; you get back an object that lets you interrogate the ontology. That's all!

Let's take a look at the [Friend Of A Friend](http://semanticweb.org/wiki/FOAF) vocabulary.


```python
In [1]: import ontospy

In [2]: ontospy.__version__
Out[2]: '1.9.8'

In [3]: model = ontospy.Ontospy("http://xmlns.com/foaf/0.1/", verbose=True)
Reading: <http://xmlns.com/foaf/0.1/>
.. trying rdf serialization: <xml>
..... success!
----------
Loaded 631 triples.
----------
RDF sources loaded successfully: 1 of 1.
..... 'http://xmlns.com/foaf/0.1/'
----------
Scanning entities...
----------
Ontologies.........: 1
Classes............: 15
Properties.........: 67
..annotation.......: 7
..datatype.........: 26
..object...........: 34
Concepts (SKOS)....: 0
Shapes (SHACL).....: 0
----------

In [4]: model.all_classes
Out[4]:
[<Class *http://xmlns.com/foaf/0.1/Agent*>,
<Class *http://xmlns.com/foaf/0.1/Document*>,
<Class *http://xmlns.com/foaf/0.1/Group*>,
<Class *http://xmlns.com/foaf/0.1/Image*>,
<Class *http://xmlns.com/foaf/0.1/LabelProperty*>,
<Class *http://xmlns.com/foaf/0.1/OnlineAccount*>,
<Class *http://xmlns.com/foaf/0.1/OnlineChatAccount*>,
<Class *http://xmlns.com/foaf/0.1/OnlineEcommerceAccount*>,
<Class *http://xmlns.com/foaf/0.1/OnlineGamingAccount*>,
<Class *http://xmlns.com/foaf/0.1/Organization*>,
<Class *http://xmlns.com/foaf/0.1/Person*>,
<Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>,
<Class *http://xmlns.com/foaf/0.1/Project*>,
<Class *http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing*>,
<Class *http://www.w3.org/2004/02/skos/core#Concept*>]

In [5]: model.all_properties_object
Out[5]:
[<Property *http://xmlns.com/foaf/0.1/account*>,
<Property *http://xmlns.com/foaf/0.1/accountServiceHomepage*>,
<Property *http://xmlns.com/foaf/0.1/based_near*>,
<Property *http://xmlns.com/foaf/0.1/currentProject*>,
<Property *http://xmlns.com/foaf/0.1/depiction*>,
<Property *http://xmlns.com/foaf/0.1/depicts*>,
<Property *http://xmlns.com/foaf/0.1/focus*>,
<Property *http://xmlns.com/foaf/0.1/fundedBy*>,
<Property *http://xmlns.com/foaf/0.1/holdsAccount*>,
<Property *http://xmlns.com/foaf/0.1/homepage*>,
<Property *http://xmlns.com/foaf/0.1/img*>,
<Property *http://xmlns.com/foaf/0.1/interest*>,
<Property *http://xmlns.com/foaf/0.1/isPrimaryTopicOf*>,
<Property *http://xmlns.com/foaf/0.1/knows*>,
<Property *http://xmlns.com/foaf/0.1/logo*>,
<Property *http://xmlns.com/foaf/0.1/made*>,
<Property *http://xmlns.com/foaf/0.1/maker*>,
<Property *http://xmlns.com/foaf/0.1/mbox*>,
<Property *http://xmlns.com/foaf/0.1/member*>,
<Property *http://xmlns.com/foaf/0.1/openid*>,
<Property *http://xmlns.com/foaf/0.1/page*>,
<Property *http://xmlns.com/foaf/0.1/pastProject*>,
<Property *http://xmlns.com/foaf/0.1/phone*>,
<Property *http://xmlns.com/foaf/0.1/primaryTopic*>,
<Property *http://xmlns.com/foaf/0.1/publications*>,
<Property *http://xmlns.com/foaf/0.1/schoolHomepage*>,
<Property *http://xmlns.com/foaf/0.1/theme*>,
<Property *http://xmlns.com/foaf/0.1/thumbnail*>,
<Property *http://xmlns.com/foaf/0.1/tipjar*>,
<Property *http://xmlns.com/foaf/0.1/topic*>,
<Property *http://xmlns.com/foaf/0.1/topic_interest*>,
<Property *http://xmlns.com/foaf/0.1/weblog*>,
<Property *http://xmlns.com/foaf/0.1/workInfoHomepage*>,
<Property *http://xmlns.com/foaf/0.1/workplaceHomepage*>]

In [6]: model.printClassTree()
foaf:Agent
----foaf:Group
----foaf:Organization
----foaf:Person
foaf:Document
----foaf:Image
----foaf:PersonalProfileDocument
foaf:LabelProperty
foaf:OnlineAccount
----foaf:OnlineChatAccount
----foaf:OnlineEcommerceAccount
----foaf:OnlineGamingAccount
foaf:Project
http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing
----foaf:Person
skos:Concept

In [7]: model.toplayer_classes
Out[7]:
[<Class *http://xmlns.com/foaf/0.1/Agent*>,
<Class *http://xmlns.com/foaf/0.1/Document*>,
<Class *http://xmlns.com/foaf/0.1/LabelProperty*>,
<Class *http://xmlns.com/foaf/0.1/OnlineAccount*>,
<Class *http://xmlns.com/foaf/0.1/Project*>,
<Class *http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing*>,
<Class *http://www.w3.org/2004/02/skos/core#Concept*>]

In [8]: model.get_class('document')
Out[8]:
[<Class *http://xmlns.com/foaf/0.1/Document*>,
<Class *http://xmlns.com/foaf/0.1/PersonalProfileDocument*>]

In [9]: c1 = _[1]

In [10]: print(c1.rdf_source())
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix vann: <http://purl.org/vocab/vann/> .
@prefix void: <http://rdfs.org/ns/void#> .
@prefix vs: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .
@prefix wot: <http://xmlns.com/wot/0.1/> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

foaf:PersonalProfileDocument a rdfs:Class,
        owl:Class ;
    rdfs:label "PersonalProfileDocument" ;
    rdfs:comment "A personal profile RDF document." ;
    rdfs:subClassOf foaf:Document ;
    vs:term_status "testing" .


In [11]: c1.parents()
Out[11]: [<Class *http://xmlns.com/foaf/0.1/Document*>]

In [12]: c1.children()
Out[12]: []
```


## Is Ontospy for Me?

Here are some reasons why you should use it:

-   You are developing a Python application that needs to extract schema information from an RDF, SKOS or OWL vocabulary.
-   You have a bunch of RDF vocabularies you regularly need to interrogate, but do not want to load a full-blown ontology editor like Protege.
-   You need to quickly generate documentation for an ontology, either as simple html pages or via some more elaborate interactive visualization.
-   You love the command line and would never leave it no matter what.

> note: Ontospy does not offer any ontology-editing features

## Generating Ontology Documentation

Ontospy allows to generate documentation for an RDF vocabulary, using visualization algorithms that create simple HTML pages, Markdown files, or more complex javascript interactive charts based on D3.js.

One can then manually customize these outputs by editing the source html files.

For example:

-   [Schema.org](https://lambdamusic.github.io/ontospy-examples//schema_org_topbraidttl/index.html) documentation
-   [FOAF](https://lambdamusic.github.io/ontospy-examples//foafrdf/index.html) documentation

That's the kind of documentation Ontospy can generate out-of-the-box. For even more examples, [take a look at this page](https://lambdamusic.github.io/ontospy-examples//index.html).

> Note: this functionality relies on a module called _ontodocs_, which used to be a separate library. As of version 1.9.8 this module has been incorporated in Ontospy, but can be installed on-demand.

**Installation**

By default the libraries needed by this feature (Django and Pygments) are not installed, so you have to add them like this:

```bash
$ pip install ontospy[FULL] -U
```

This feature is normally used from the command line:

```bash
$ ontospy gendocs

Ontospy v1.9.8
Usage: ontospy gendocs [OPTIONS] [SOURCE]...

  Generate documentation for an ontology in html or markdown format

Options:
  -o, --outputpath TEXT  OUTPUT-PATH: where to save the visualization files
                         (default: home folder).
  --type TEXT            VIZ-TYPE: specify which viz type to use as an integer
                         (eg 1=single-page html, 2=multi-page etc..).
  --title TEXT           TITLE: custom title for the visualization
                         (default=graph uri).
  --theme TEXT           THEME: bootstrap css style for the html-multi-page
                         visualization (random=use a random theme).
  --lib                  LIBRARY: choose an ontology from the local library.
  --showtypes            SHOW-TYPES: show the available visualization types.
  --showthemes           SHOW-THEMES: show the available css theme choices.
  -h, --help             Show this message and exit.
```

This feature is not really meant to be used programmatically, but I'm sure there are a few constructs in there which can be reused.

In a nutshell, all visualizations inherit from a [VizFactory](https://github.com/lambdamusic/Ontospy/blob/master/ontospy/ontodocs/viz_factory.py) class that abstracts away the most common operations involved in rendering a dataviz.

This is how you would invoke a visualization from a script:

```python
import ontospy
from ontospy.ontodocs.viz.viz_html_single import *

g = ontospy.Ontospy("http://cohere.open.ac.uk/ontology/cohere.owl#")

v = HTMLVisualizer(g) # => instantiate the visualization object
v.build() # => render visualization. You can pass an 'output_path' parameter too
v.preview() # => open in browser

```

## Miscellaneous Tips

If you are using OSx El Capitan your installation line probably will look like this

    > sudo pip install ontospy -U --user python

This is due to the new [System Integrity Protection](https://support.apple.com/en-us/HT204899) (more info on this [stackoverflow post](http://stackoverflow.com/questions/33234665/upgrading-setuptools-on-osx-el-capitan))

## Quick Links

-   Github: [https://github.com/lambdamusic/ontospy](https://github.com/lambdamusic/ontospy)
-   CheeseShop: [https://pypi.python.org/pypi/ontospy](https://pypi.python.org/pypi/ontospy)
-   Docs: [http://lambdamusic.github.io/Ontospy/](http://lambdamusic.github.io/Ontospy/)

Also:

-   Video: [hhttps://youtu.be/MkKrtVHi_Ks](https://youtu.be/MkKrtVHi_Ks)

Issues or questions?

-   Then head over to the [issues](https://github.com/lambdamusic/Ontospy/issues) page.

What's changed recently?

-   Please have a look at the [Changelog](pages/changelog.html)
