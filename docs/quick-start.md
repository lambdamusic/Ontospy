---
title: Quick start
nav_order: 3
---

# Quick start

If used as a Python package, the basic workflow is the following: load a graph by instantiating the `Ontospy` class with a file containing RDFS, OWL or SKOS definitions; you get back an object that lets you interrogate the ontology. That's all!

Let's take a look at the [Friend Of A Friend](http://xmlns.com/foaf/spec/) vocabulary.

```python
In [1]: import ontospy

In [2]: ontospy.__version__
Out[2]: '2.5'

In [3]: model = ontospy.Ontospy("http://xmlns.com/foaf/0.1/", verbose=True)
Reading: <https://xmlns.com/foaf/0.1/>
.. trying rdf serialization: <xml>
..... success!
----------
Loaded 631 triples.
----------
RDF sources loaded successfully: 1 of 1.
..... 'https://xmlns.com/foaf/0.1/'
----------
Scanning entities...
----------
Ontologies.........: 1
Classes............: 15
Properties.........: 68
..annotation.......: 7
..datatype.........: 27
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

In [5]: len(model.all_properties_object)
Out[5]: 34

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
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix vs: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .

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

For a longer walkthrough, see the [getting started notebook](https://github.com/lambdamusic/ontospy/blob/master/examples/getting-started.ipynb): it loads an ontology, prints its hierarchies, inspects classes, properties and individuals, and returns the data as [pandas](https://pandas.pydata.org/) data frames, including the results of SPARQL queries.

## Other ways to load RDF

Besides file paths and URLs, `Ontospy` can load RDF from strings, open files and existing [rdflib](https://rdflib.readthedocs.io/) graphs. Each parameter takes one item or a list, and they can be combined: everything ends up in one graph.

```python
import rdflib
import ontospy

g = ontospy.Ontospy(data="@prefix ex: <http://example.org/> . ex:Cat a <http://www.w3.org/2002/07/owl#Class> .",
                    rdf_format="turtle")           # a string of RDF

with open("foaf.rdf") as f:
    g = ontospy.Ontospy(file_obj=f)                 # an open file

my_graph = rdflib.Graph().parse("foaf.rdf")
g = ontospy.Ontospy(graph_obj=my_graph)             # an rdflib graph, eg built by your own code

g = ontospy.Ontospy("foaf.rdf", graph_obj=[my_graph, rdflib.Graph()])   # a mix of sources
```

Tip: Ontospy keeps the namespace prefixes declared in your RDF files. When you build an rdflib graph yourself, though, rdflib can rename them while parsing: since rdflib 7, a new `Graph()` comes with ~30 well-known prefixes, so eg a file declaring `schema:` for `http://schema.org/` ends up as `schema1:` (rdflib's own `schema` is `https://schema.org/`). To keep your files' prefixes, create the graph with only rdflib's core prefixes; Ontospy still adds the well-known ones for any namespace your data doesn't declare:

```python
my_graph = rdflib.Graph(bind_namespaces="core").parse("my-ontology.ttl")
g = ontospy.Ontospy(graph_obj=my_graph)
```

All the parameters are described in the `Ontospy` class docstring: `help(ontospy.Ontospy)`.
