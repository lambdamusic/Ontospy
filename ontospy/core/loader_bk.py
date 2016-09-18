# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c) 2013-2016 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""

from __future__ import print_function
import sys, os, time, optparse
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLStore

import click

from ..shared.utils import *

from .graph import *
# from .queryHelper import QueryHelper



def load(uri=None, text="", file_obj=None, endpoint=None, rdf_format=None, verbose=False):
    """
    Load some RDF source into an RDFLIB graph instance.
    Return an ontospy Catalog object containing that graph.
    
    Note: arguments can be lists, with the effect that the resulting graph
    will be a union of the rdf data contained in each of the arguments 

    @todo: real_uri, graphuri - needed?

    @clarify: does this return an rdflib object or an ontospy one???? 
    in the first case it could go into 'shared' ..

    """

    rdfgraph = rdflib.Graph()
    
    if not rdf_format:
        rdf_format_opts = ['xml', 'turtle', 'n3', 'nt', 'trix', 'rdfa']
    else:
        rdf_format_opts = [rdf_format]
   
    # URI OR PATH
    if uri:
        if not type(uri) in [list,tuple]:
            uri = [uri]
        for candidate in uri:
            if os.path.isdir(candidate):
                # inner loop in case it's a folder
                temp = get_files_with_extensions(candidate, ["ttl", "rdf", "owl", 
                    "trix", "rdfa", "n3", "nq", "jsonld"])
            else:
                # fake a one-element list
                temp = [candidate]
            for each in temp:
                real_uri, graphuri = dereference_uri(each)
                rdfgraph = load_uri(real_uri, rdf_format_opts, verbose, rdfgraph)


    # TEXT STRING
    elif text:
        if not type(text) in [list,tuple]:
            text = [text]
        for each in text:
            rdfgraph = load_text(each, rdf_format_opts, verbose, rdfgraph)


    # FILE OBJECT
    elif file_obj:
        if not type(file_obj) in [list,tuple]:
            file_obj = [file_obj]
        for each in file_obj:
            rdfgraph = load_file(each, rdf_format_opts, verbose, rdfgraph)


    # ENDPOINT
    elif endpoint:
        rdfgraph = rdflib.ConjunctiveGraph(store=SPARQLStore(source))
        graphuri = source  # default uri is www location
        if verbose: printDebug("Accessing SPARQL Endpoint <%s>" % self.graphuri)
        if verbose: printDebug("(note: support for sparql endpoints is still experimental)")

    
    else:
        raise Exception("You must specify where to load rdf from.")

    
    if verbose: printDebug("----------\nLoaded %d triples from <%s>" %
                           (len(rdfgraph), uri))

    # set up the query helper too
    # self.queryHelper = QueryHelper(self.rdfgraph)
    return rdfgraph
    



def dereference_uri(uri):
    """

    :param uri:
    :return:
    """
    if type(uri) == type("string") or type(uri) == type(u"unicode"):
        
        if uri.startswith("www."):  # support for lazy people
            uri = "http://%s" % str(uri)
        if uri.startswith("http://"):
            # headers = "Accept: application/rdf+xml"
            headers = {'Accept': "application/rdf+xml"}
            req = urllib2.Request(uri, headers=headers)
            res = urllib2.urlopen(req)
            uri = res.geturl()  # after 303 redirects
            graphuri = uri  # default uri is www location
        else:
            graphuri = "file://" + uri  # default uri is www location
    
    else:
        raise Exception("A URI must be in string format.")
    
    return (uri, graphuri)





def loading_failed(rdf_format_opts):
    # abort loading
    printDebug(
        "----------\nFatal error parsing graph (tried using RDF serialization: %s)\n" % (str(rdf_format_opts)))
    printDebug(
        "----------\nTIP: You can try one of the following RDF validation services\n<http://mowl-power.cs.man.ac.uk:8080/validator/validate>\n<http://www.ivan-herman.net/Misc/2008/owlrl/>")
    # sys.exit(0)
    return


# ---------------------------------



def load_uri(uri, rdf_format_opts, verbose, rdfgraph):
    """
    
    :param uri:
    :param rdf_format_opts:
    :param verbose:
    :return:
    """

    if verbose: printDebug("----------")
    if verbose: printDebug("Loading URI <%s>" % uri)
    success = False
    for f in rdf_format_opts:
        if verbose: printDebug(".. trying rdf serialization: <%s>" % f)
        try:
            rdfgraph.parse(uri, format=f)
            if verbose: printDebug("..... success!")
            success = True
            break
        except:
            if verbose: printDebug("..... failed")

    if not success == True:
        loading_failed(rdf_format_opts)
        
    return rdfgraph
            
            
            

def load_text(text, rdf_format_opts, verbose, rdfgraph):
    """
    
    :param text:
    :param rdf_format_opts:
    :param verbose:
    :return:
    """
    if verbose: printDebug("----------")
    if verbose: printDebug("Loading Text '%s ...'" % text[:10])
    success = False
    for f in rdf_format_opts:
        if verbose: printDebug(".. trying rdf serialization: <%s>" % f)
        try:
            rdfgraph.parse(data=text, format=f)
            if verbose: printDebug("..... success!")
            success = True
            break
        except:
            if verbose: printDebug("..... failed", "error")

    if not success == True:
        loading_failed(rdf_format_opts)

    return rdfgraph







def load_file(file_obj, rdf_format_opts, verbose):
    if verbose: printDebug("----------")
    if verbose: printDebug("Loading File Object <%s> ...'" % file_obj.name)
    if type(file_obj) == file:
        # The type of open file objects such as sys.stdout; alias of the built-in file.
        graphuri = file_obj.name  # default uri is filename
    
    if not success == True:
        loading_failed(rdf_format_opts)
        
    return rdfgraph









if __name__ == '__main__':
    """
    simple test: python -m ontospy.core.loader
    """   
    # load(["http://purl.org/dc/terms/", "http://xmlns.com/foaf/spec/"], verbose=True)
    # load(["/Users/michele.pasin/Dropbox/code/scigraph/scigraph-core-ontology/data"], verbose=True)
    load(["/Users/michele.pasin/Dropbox/code/scigraph/scigraph-core-ontology/data/review/legacy/properties.ttl"], verbose=True)



