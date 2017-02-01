# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


"""
ONTOSPY
Copyright (c) 2013-2017 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""

from __future__ import print_function
import sys, os, time, optparse
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

import click
import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLStore


from .utils import *



class RDFLoader(object):
    """
    Utility to Load any RDF source into an RDFLIB graph instance.
    
    Accepts: [single item or list]
    :: uri_or_path = a uri or local path 
    :: text = a string containing rdf 
    :: file_obj = a python file objecy 

    Returns: rdflib graph instance. 

    Other options:
    :: rdf_format = one of ['xml', 'turtle', 'n3', 'nt', 'trix', 'rdfa']
    :: verbose = if True, prints out a summary of loading operations

    Note : you can pass lists, with the effect that the resulting graph
    will be a union of the rdf data contained in each of the arguments 

    """

    def __init__(self, rdfgraph=None):
        super(RDFLoader, self).__init__()
        
        self.rdfgraph = rdfgraph or rdflib.Graph()
        self.sources_valid = []
        self.sources_invalid = []

    def load(self, uri_or_path=None, text=None, file_obj=None, rdf_format="", verbose=False):
        
        if not rdf_format:
            self.rdf_format_opts = ['xml', 'turtle', 'n3', 'nt', 'trix', 'rdfa']
        else:
            self.rdf_format_opts = [rdf_format]
       
        # URI OR PATH
        if uri_or_path:
            if not type(uri_or_path) in [list,tuple]:
                uri_or_path = [uri_or_path]
            for candidate in uri_or_path:
                if os.path.isdir(candidate):
                    # inner loop in case it's a folder
                    temp = get_files_with_extensions(candidate, ["ttl", "rdf", "owl", 
                        "trix", "rdfa", "n3", "nq", "jsonld"])
                else:
                    # fake a one-element list
                    temp = [candidate]
                # finally:
                for each in temp:
                    uri = self.resolve_redirects_if_needed(each)
                    self.load_uri(uri, verbose)


        # TEXT STRING
        elif text:
            if not type(text) in [list,tuple]:
                text = [text]
            for each in text:
                self.load_text(each, verbose)


        # FILE OBJECT
        elif file_obj:
            if not type(file_obj) in [list,tuple]:
                file_obj = [file_obj]
            for each in file_obj:
                self.load_file(each, verbose)


        else:
            raise Exception("You must specify where to load RDF from.")

    

        if verbose: self.print_summary()

        return self.rdfgraph
        



    def print_summary(self):
        """
        print out stats about loading operation
        """
        if self.sources_valid:
            printDebug("----------\nLoaded %d triples.\n----------" % 
                len(self.rdfgraph), fg='green')
            printDebug("RDF sources loaded successfully: %d of %d.\n----------" %
                (len(self.sources_valid), len(self.sources_valid) + len(self.sources_invalid)), fg='green')
            for s in self.sources_valid:
                printDebug("-> " + s, fg='green')
        else:
            printDebug("Sorry - no valid RDF was found", fg='red')

        if self.sources_invalid:
            printDebug("----------\nRDF sources failed to load: %d.\n----------" %
                (len(self.sources_invalid)), fg='red')
            for s in self.sources_invalid:
                printDebug("-> " + s, fg="red")        



    def load_uri(self, uri, verbose):
        """
        
        :param uri:
        :param rdf_format_opts:
        :param verbose:
        :return:
        """

        if verbose: printDebug("----------")
        if verbose: printDebug("Reading: <%s>" % uri)
        success = False
        for f in self.rdf_format_opts:
            if verbose: printDebug(".. trying rdf serialization: <%s>" % f)
            try:
                self.rdfgraph.parse(uri, format=f)
                if verbose: printDebug("..... success!", bold=True)
                success = True
                self.sources_valid += [uri]
                break
            except:
                if verbose: printDebug("..... failed")

        if not success == True:
            self.loading_failed(self.rdf_format_opts)
            self.sources_invalid += [uri]
      
                

    def load_text(self, text, verbose):
        """
        
        :param text:
        :param rdf_format_opts:
        :param verbose:
        :return:
        """
        if verbose: printDebug("----------")
        if verbose: printDebug("Reading: '%s ...'" % text[:10])
        success = False
        for f in self.rdf_format_opts:
            if verbose: printDebug(".. trying rdf serialization: <%s>" % f)
            try:
                self.rdfgraph.parse(data=text, format=f)
                if verbose: printDebug("..... success!")
                success = True
                self.sources_valid += ["Text: '%s ...'" % text[:10]]
                break
            except:
                if verbose: printDebug("..... failed", "error")

        if not success == True:
            self.loading_failed(self.rdf_format_opts)
            self.sources_invalid += ["Text: '%s ...'" % text[:10]]




    def load_file(file_obj, verbose):
        """
        The type of open file objects such as sys.stdout; alias of the built-in file.
        @TODO: when is this used? 
        """
        if verbose: printDebug("----------")
        if verbose: printDebug("Reading: <%s> ...'" % file_obj.name)

        if type(file_obj) == file:
            self.rdfgraph = self.rdfgraph + file_obj
            self.sources_valid += [file_obj.NAME]
        else:
            self.loading_failed(self.rdf_format_opts)
            self.sources_invalid += [file_obj.NAME]





    def resolve_redirects_if_needed(self, uri):
        """
        substitute with final uri after 303 redirects (if it's a www location!)
        :param uri:
        :return:
        """
        if type(uri) == type("string") or type(uri) == type(u"unicode"):
            
            if uri.startswith("www."):  # support for lazy people
                uri = "http://%s" % str(uri)
            if uri.startswith("http://"):
                # headers = "Accept: application/rdf+xml"  # old way
                headers = {'Accept': "application/rdf+xml"}
                req = urllib2.Request(uri, headers=headers)
                res = urllib2.urlopen(req)
                uri = res.geturl()
        
        else:
            raise Exception("A URI must be in string format.")
        
        return uri




    def loading_failed(self, rdf_format_opts):
        """default message if we need to abort loading"""
        printDebug(
            "----------\nFatal error parsing graph (tried using RDF serialization: %s)\n" % (str(rdf_format_opts)), "red")
        printDebug(
            "----------\nTIP: You can try one of the following RDF validation services\n<http://mowl-power.cs.man.ac.uk:8080/validator/validate>\n<http://www.ivan-herman.net/Misc/2008/owlrl/>")

        return





##
# testing
##


@click.command()
@click.argument('uri_or_path', nargs=-1, type=click.STRING)
@click.option('--noverbose', is_flag=True, help='Turn off verbose mode.')
@click.option('--trylist', is_flag=True, help='Try loading a predefined list of files.')
def test(uri_or_path, noverbose, trylist):
    l = RDFLoader()
    if trylist or not uri_or_path:
        l.load(["http://purl.org/dc/terms/", "http://xmlns.com/foaf/spec/"], verbose=not(noverbose))
    else:
        l.load(uri_or_path, verbose=not(noverbose))




if __name__ == '__main__':
    """
    simple test: python -m ontospy.core.loader [PATH] [OPTIONS]
    """
    test()
    printDebug("Finished")


