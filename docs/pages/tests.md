---
title: Running the tests
nav_order: 8
---

# Running the tests

Ontospy's tests use [pytest](https://docs.pytest.org/). They live in `ontospy/tests`, together with the RDF files they load (`ontospy/tests/rdf`).

## Setup

From a clone of the repository, in a virtual environment:

```
$ pip install -e .
$ pip install pytest
```

Install with `-e` (editable): the RDF files in `ontospy/tests/rdf` aren't included in the package, so the tests and quick tests only find them in a source checkout.

## Running the tests

From the repository root:

```
$ pytest                       # all tests
$ pytest -m "not remote"       # skip the tests that need network access
$ pytest -m remote             # only the tests that need network access
```

Some useful variations:

```
$ pytest ontospy/tests/test_methods.py            # one file
$ pytest ontospy/tests/test_methods.py -k test2   # one test
$ pytest -s                                       # show the tests' printed output
$ pytest -W ignore::DeprecationWarning            # hide rdflib deprecation warnings
```

Each test file can also be run on its own with `unittest`, eg `python -m ontospy.tests.test_methods`.

The local tests take about a minute, mostly spent loading the ontologies in `ontospy/tests/rdf`.

## What the tests cover

| File | What it checks | Network |
|---|---|---|
| `test_load_local.py` | Every ontology in `ontospy/tests/rdf` loads | No |
| `test_methods.py` | Specific `Ontospy` methods, preferred titles and languages, custom entity classes | No |
| `test_shapes.py` | SHACL shapes are extracted (SciGraph ontology) | No |
| `test_gendocs.py` | Every documentation type builds for an ontology with individuals (`pizza.ttl`) | No |
| `test_load_remote.py` | A sample online ontology loads | Yes |
| `test_sparql.py` | Connecting to and querying the DBpedia SPARQL endpoint | Yes |

The network-dependent tests are tagged with the `remote` marker in `ontospy/tests/conftest.py`. They can fail for reasons outside Ontospy, eg when DBpedia is down or slow.

## Continuous integration

On every push and pull request to `master`, GitHub Actions runs `pytest -m "not remote"` on Python 3.10 to 3.14. See `.github/workflows/ci.yml`.

## Quick tests

`ontospy/tests/quick.py` is a scratchpad for trying things out before they become proper tests. It is not run by pytest. Run a numbered quick test with:

```
$ ontospy_quicktest 4
```

or `python -m ontospy.tests.quick 4`.

| Number | What it does |
|---|---|
| 1 | Loads `paper.jsonld` |
| 2 | Queries the DBpedia SPARQL endpoint |
| 3 | Navigates DBpedia triples using rdflib's `SPARQLStore` directly |
| 4 | Lists the individuals in `pizza.ttl` and the classes they are instances of |

## Local-only tests

Tests that shouldn't be committed, eg against a private SPARQL endpoint that needs credentials, can go in `ontospy/tests/local/`:

- the folder is gitignored
- it has no `__init__.py`, so it is never included in the package
- `pytest` still picks the tests up, and marks them as `remote`

Read credentials from environment variables rather than writing them in the test files, and skip the tests when they are missing, eg:

```python
import os
import pytest

@pytest.fixture(scope="module")
def credentials():
    user, pwd = os.environ.get("MY_SPARQL_USER"), os.environ.get("MY_SPARQL_PASSWORD")
    if not (user and pwd):
        pytest.skip("Set MY_SPARQL_USER and MY_SPARQL_PASSWORD to run these tests")
    return (user, pwd)
```
