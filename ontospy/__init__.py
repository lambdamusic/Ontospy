#!/usr/bin/env python
# encoding: utf-8

from ._version import __version__

import logging
logging.basicConfig()

from .core.graph import Graph, SparqlEndpoint 
# this allows to load with 'import ontospy', and using 'ontospy.Graph' 