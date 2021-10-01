# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from __future__ import print_function

from ..VERSION import __version__, VERSION

import logging
logging.basicConfig()

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

import sys, os
try:
    import cPickle
except ImportError:
    import pickle as cPickle

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

from .ontospy import Ontospy
from .utils import printDebug

# ===========
# ***
# TESTING FLAG : DISABLE CACHING SO TO FORCE RECONSTRUCTION OF GRAPH EACH TIME
# ***
# ===========

GLOBAL_DISABLE_CACHE = False

# ===========
#
# STATIC VARIABLES AND PATHS
#
# ===========

# python package installation
_dirname, _filename = os.path.split(os.path.abspath(__file__))

# local repository constants
ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
ONTOSPY_LOCAL_CACHE = ONTOSPY_LOCAL + "/.cache/" + VERSION
ONTOSPY_LOCAL_CACHE_TOP = ONTOSPY_LOCAL + "/.cache/"

ONTOSPY_LIBRARY_DEFAULT = ONTOSPY_LOCAL + "/models/"

BOOTSTRAP_ONTOLOGIES = [
    "http://xmlns.com/foaf/spec/",
    "http://purl.org/dc/terms/",
    "http://rdfs.org/sioc/ns#",
    "http://www.w3.org/2008/05/skos#",
    "http://rdfs.org/ns/void#",
    "http://purl.org/goodrelations/v1",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl",
    "http://www.ifomis.org/bfo/1.1",
    #
    # "http://topbraid.org/schema/schema.ttl",
    # "http://www.cidoc-crm.org/rdfs/cidoc_crm_v6.0-draft-2015January.rdfs",
    # "http://purl.uniprot.org/core/",
    # "http://purl.org/spar/cito/",
    # "http://ns.nature.com/terms/",
]

# sample endpoints
BOOTSTRAP_ENDPOINTS = [
    "http://dbpedia.org/sparql", 
    "http://data.semanticweb.org/sparql",
    "http://linkedgeodata.org/sparql", 
    "http://sparql.data.southampton.ac.uk/"
]
