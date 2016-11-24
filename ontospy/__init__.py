# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from __future__ import print_function

from .VERSION import __version__, VERSION

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

from colorama import Fore, Style


from .core.ontospy import Ontospy
# this allows to load with 'import ontospy', and using 'ontospy.Ontospy'

from .core.utils import printDebug




# ===========
# ***
# TESTING FLAG : DISABLE CACHING SO TO FORCE RECONSTRUCTION OF GRAPH EACH TIME
# ***
# ===========

import socket
hostname = socket.gethostname()
if hostname in ("L7898", "Tartaruga"):
    GLOBAL_DISABLE_CACHE = False  # set to True for testing
else:
    GLOBAL_DISABLE_CACHE = False

# ===========
# ===========





# ===========
#
# STATIC VARIABLES AND PATHS
#
# ===========



# python package installation
_dirname, _filename = os.path.split(os.path.abspath(__file__))

ONTOSPY_VIZ_TEMPLATES = _dirname + "/viz/templates/"
ONTOSPY_VIZ_STATIC = _dirname + "/viz/static/"
ONTOSPY_SOUNDS = _dirname + "/data/sounds/"


# local repository constants
ONTOSPY_LOCAL = os.path.join(os.path.expanduser('~'), '.ontospy')
ONTOSPY_LOCAL_VIZ = ONTOSPY_LOCAL + "/viz"
ONTOSPY_LOCAL_CACHE = ONTOSPY_LOCAL + "/.cache/" + VERSION

ONTOSPY_LIBRARY_DEFAULT = ONTOSPY_LOCAL + "/models/"



BOOTSTRAP_ONTOLOGIES = [
	"http://xmlns.com/foaf/spec/" ,
	"http://purl.org/dc/terms/" ,
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
