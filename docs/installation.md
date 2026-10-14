---
title: Installation
nav_order: 2
---

# Installation

Prerequisites:

-   Python 3.10 or later
-   A Python package manager, eg [pip](https://pip.pypa.io/en/stable/installation/)

Then install Ontospy from the Python Package Index.

## Standard version

If you want to use ontospy as a Python module, or to automatically create some [HTML documentation](gendocs.html) for an ontology, you can install the standard version of the library like this:

```bash
$ pip install ontospy
```

The python library, its dependencies and all of its command-line executables will be installed. The only thing which is left out is the bash autocomplete external dependencies.

NOTE:
As of Ontospy version 2.0, the documentation generation libraries are installed by default with Ontospy. Previously, third party dependencies (e.g. Django) had to be installed separately.

## Standard version plus shell

The 'shell' or interactive command line interface requires the [readline](https://pypi.org/project/readline/) module, a set of functions for use by applications that allow users to edit command lines as they are typed in.

This module is optionally installed with Ontospy like this:

```bash
$ pip install ontospy[SHELL]
```

## Upgrading

If you're upgrading from an older version, make sure you use the -U flag:

```bash
$ pip install ontospy -U
```

If you're upgrading from version 1.x, see [Upgrading to 2.0](upgrading.html).
