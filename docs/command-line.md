---
title: Command line
nav_order: 4
---

# Command line

Installing Ontospy also installs the `ontospy` command. Each of its subcommands has its own `--help`.

```text
$ ontospy --help

Usage: ontospy [OPTIONS] [COMMAND] [ARGS]...

  Ontospy allows to extract and visualise ontology information included in RDF
  data. Use one of the commands listed below to find out more, or visit
  http://lambdamusic.github.io/ontospy

Options:
  -v, --verbose  VERBOSE: print out debug messages.
  -h, --help     Show this message and exit.

Commands:
  scan     SCAN: get ontology data from RDF source and print out a report.
  gendocs  GENDOCS: generate documentation in html or markdown format.
  lib      LIBRARY: work with a local library of RDF models.
  shell    SHELL: launch ontospy's interactive mode.
  ser      SERIALIZE: tranform an RDF graph to a format of choice.
  utils    UTILS: miscellaneous bits and pieces.
```

## Scanning an ontology

`ontospy scan` loads an RDF source (a file, a URL or, with `-e`, a SPARQL endpoint) and prints out a report of the ontologies, classes, properties, concepts and shapes it finds:

```bash
$ ontospy scan http://purl.org/spar/frbr
```

```text
$ ontospy scan --help

Usage: ontospy scan [OPTIONS] [SOURCES]...

  SCAN: get ontology data from RDF source and print out a report.

Options:
  -x, --extra        EXTRA-DATA: extract implicit types and predicates using
                     basic inference rules. Note: by default ontospy extracts
                     only classes/properties which are explictly declared.
  -i, --individuals  INDIVIDUALS: extract class instances as well. Note: by
                     default ontospy extracts direct instances of explicitly
                     declared classes. Use with -x option to get all possible
                     instances.
  -r, --raw          RAW-DATA: print out the raw RDF data received.
  -e, --endpoint     ENDPOINT: the url passed is a sparql endpoint (beta).
  -f, --format TEXT  RDF-FORMAT: the serialization format of the input file
                     (default=inferred)
  -v, --verbose      VERBOSE: print out debug messages.
  -h, --help         Show this message and exit.
```

## The other commands

-   `ontospy gendocs`: generate documentation for an ontology, see [Generating documentation](gendocs.html)
-   `ontospy lib`: work with a local library of ontologies, so they can be quickly reloaded later: list and open them (`--show`), or fill the library with some popular ones (`--bootstrap`)
-   `ontospy shell`: an interactive mode for exploring ontologies, optionally preloaded with an RDF source (requires the [shell extra](installation.html#standard-version-plus-shell))
-   `ontospy ser`: convert an RDF graph to another serialization, eg RDF/XML to Turtle (`-f`)
-   `ontospy utils`: test a JSON-LD file in the online playground (`-j`), or find ontologies in online repositories like LOV or prefix.cc (`-d`)
