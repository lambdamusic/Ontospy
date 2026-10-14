---
title: Generating documentation
nav_order: 5
---

# Generating documentation

Ontospy allows to generate documentation for an RDF vocabulary, using visualization algorithms that create simple HTML pages, Markdown files, or more complex javascript interactive charts based on D3.js.

One can then manually customize these outputs by editing the source html files.

For example:

-   [Pizza](https://lambdamusic.github.io/ontospy-examples/pizzattl/index.html) documentation
-   [FOAF](https://lambdamusic.github.io/ontospy-examples/foafrdf/index.html) documentation

That's the kind of documentation Ontospy can generate out-of-the-box. For even more examples, [take a look at this page](https://lambdamusic.github.io/ontospy-examples/index.html).


## How to

This feature is normally used from the command line:

```text
$ ontospy gendocs --help

Ontospy v2.5
Usage: ontospy gendocs [OPTIONS] [SOURCE]...

  GENDOCS: generate documentation in html or markdown format.

Options:
  -l, --lib              LIBRARY: choose an ontology from your local library.
  -o, --outputpath TEXT  OUTPUT-PATH: where to save the visualization files
                         (default: home folder).
  -x, --extra            EXTRA-DATA: extract implicit types and predicates
                         using basic inference rules. Note: by default ontospy
                         extracts only classes/properties which are explictly
                         declared.
  -i, --individuals      INDIVIDUALS: extract class instances as well. Note:
                         by default ontospy extracts only instances of
                         explicitly declared classes. Use with -x option to
                         get all possible instances.
  --type TEXT            VIZ-TYPE: specify which viz type to use as an integer
                         (eg 1=single-page html, 2=multi-page etc..).
  --title TEXT           TITLE: custom title for the visualization
                         (default=graph uri).
  --theme TEXT           THEME: select bootstrap style (only for the html-
                         multi-page visualization). Default: simplex
                         (random=use a random theme).
  --preflabel TEXT       PREF-LABEL: default value to use for entity titles
                         (qname|label - default=qname).
  --preflang TEXT        PREF-LANGUAGE: default language for multilingual
                         strings (default=en).
  --nobrowser            NO-BROWSER: prevents opening the html output in the
                         browser by default.
  --emptyfolder          EMPTY-FOLDER: delete everything in the output folder
                         before generating the documentation. By default,
                         files already there are kept (and overwritten when
                         needed).
  --nonredundant         NON-REDUNDANT: in the class, property, concept and
                         shape trees, don't repeat a child under a parent when
                         it's already a descendant of one of the parent's
                         other children, eg for reasoned ontologies. Only used
                         by the html-complex visualization.
  --showtypes            SHOW-TYPES: show the available visualization types.
  --showthemes           SHOW-THEMES: show the available css theme choices.
  -v, --verbose          VERBOSE: print out debug messages.
  -h, --help             Show this message and exit.
```

By default, files already in the output folder are kept and overwritten when needed; Ontospy warns about files it didn't write, eg left over from an earlier build. Use `--emptyfolder` to clear the folder first.

For reasoned ontologies, where inferred subclass relations are stated explicitly (eg `:RedBeardedGuy rdfs:subClassOf :Mammal` as well as `:Human`), the `--nonredundant` option shows each class only under its most specific parents in the html-complex tree pages. From Python, the same is available as `ontologyClassTree(non_redundant=True)` and the other tree methods.

## From Python

All visualizations inherit from a [VizFactory](https://github.com/lambdamusic/Ontospy/blob/master/ontospy/gendocs/viz_factory.py) class that abstracts away the most common operations involved in rendering a dataviz.

This is how you would invoke a visualization from a script:

```python
import ontospy
from ontospy.gendocs.viz.viz_html_single import *

g = ontospy.Ontospy("my-ontology.ttl")

v = HTMLVisualizer(g) # => instantiate the visualization object
v.build() # => render visualization. You can pass an 'output_path' parameter too
v.preview() # => open in browser

```

## Customising the templates

The documentation is rendered with [Jinja2](https://jinja.palletsprojects.com/) templates, which live in the package's [templates folder](https://github.com/lambdamusic/Ontospy/tree/master/ontospy/gendocs/media/templates). To change how the output looks, eg to add your own CSS, or to remove a section you don't need, you can override any of them with your own version:

1. Copy the template you want to change into a folder of your own, keeping its path relative to the templates folder, eg `my-templates/html-multi/base.html`.
2. Edit your copy.
3. Pass a Jinja2 environment that looks in your folder first, and falls back to Ontospy's own templates for everything else:

```python
import ontospy
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader, select_autoescape
from ontospy.gendocs.jinja_env import add_default_filters
from ontospy.gendocs.viz.viz_html_multi import KompleteViz

my_env = Environment(
    loader=ChoiceLoader([
        FileSystemLoader("my-templates"),                        # your versions first
        PackageLoader("ontospy.gendocs.media", "templates"),     # then Ontospy's
    ]),
    autoescape=select_autoescape(["html", "xml"]),
    extensions=["jinja2_time.TimeExtension"],
)
add_default_filters(my_env)   # the filters Ontospy's templates use

g = ontospy.Ontospy("my-ontology.ttl")
v = KompleteViz(g, title="My ontology", jinja2env=my_env)
v.build("my-docs")
```

Every visualization type accepts the `jinja2env` parameter. For example, with the multi-page HTML (`KompleteViz`):

-   to add your own stylesheet, override `html-multi/base.html` and add a `<link>` after the existing ones
-   to change what a class page shows, eg remove its "Usage" section, override `html-multi/browser/browser_classinfo.html`

Custom templates are only available from Python, not from the `ontospy gendocs` command.
