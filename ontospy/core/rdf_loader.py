# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
ONTOSPY
Copyright (c)  __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""

from __future__ import print_function
import sys, os, time, optparse
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

import click
import rdflib

from .utils import *


class RDFLoader(object):
    """
    Utility to Load any RDF source into an RDFLIB graph instance.

    Accepts: [single item or list]
    :: uri_or_path = a uri or local path
    :: data = a string containing rdf
    :: file_obj = a python file objecy

    Returns: rdflib graph instance.

    Other options:
    :: rdf_format = one of ['xml', 'turtle', 'n3', 'nt', 'trix', 'rdfa']
    :: verbose = if True, prints out a summary of loading operations

    Note : you can pass lists, with the effect that the resulting graph
    will be a union of the rdf data contained in each of the arguments

    @TODO: refactor so that verbose is always taken from INIT method

    """

    SERIALIZATIONS = [
        'xml',
        'n3',
        'nt',
        'json-ld',
        'turtle',
        'rdfa',
    ]

    def __init__(self, rdfgraph=None, verbose=False):
        super(RDFLoader, self).__init__()

        self.rdflib_graph = rdfgraph or rdflib.Graph()
        self.sources_valid = []
        self.sources_invalid = []
        self.verbose = verbose

    def _debugGraph(self):
        """internal util to print out contents of graph"""
        print("Len of graph: ", len(self.rdflib_graph))
        for x, y, z in self.rdflib_graph:
            print(x, y, z)

    def load(self, uri_or_path=None, data=None, file_obj=None, rdf_format=""):

        if not rdf_format:
            self.rdf_format_opts = self.SERIALIZATIONS
        else:
            self.rdf_format_opts = [rdf_format]

        # URI OR PATH
        if uri_or_path:
            if not type(uri_or_path) in [list, tuple]:
                uri_or_path = [uri_or_path]
            for candidate in uri_or_path:
                if os.path.isdir(candidate):
                    # inner loop in case it's a folder
                    temp = get_files_with_extensions(candidate, [
                        "ttl", "rdf", "owl", "trix", "rdfa", "n3", "nq",
                        "jsonld", "nt"
                    ])
                else:
                    # fake a one-element list
                    temp = [candidate]
                # finally:
                for each in temp:
                    uri = self.resolve_redirects_if_needed(each)
                    self.load_uri(uri)

        # DATA STRING
        elif data:
            if not type(data) in [list, tuple]:
                data = [data]
            for each in data:
                self.load_data(each)

        # FILE OBJECT
        elif file_obj:
            if not type(file_obj) in [list, tuple]:
                file_obj = [file_obj]
            for each in file_obj:
                self.load_file(each)

        else:
            raise Exception("You must specify where to load RDF from.")

        if self.verbose: self.print_summary()

        return self.rdflib_graph

    def load_uri(self, uri):
        """
        Load a single resource into the graph for this object. 

        Approach: try loading into a temporary graph first, if that succeeds merge it into the main graph. This allows to deal with the JSONLD loading issues which can solved only by using a  ConjunctiveGraph (https://github.com/RDFLib/rdflib/issues/436). Also it deals with the RDFA error message which seems to stick into a graph even if the parse operation fails. 
        
        NOTE the final merge operation can be improved as graph-set operations involving blank nodes could case collisions (https://rdflib.readthedocs.io/en/stable/merging.html)  

        :param uri: single RDF source location
        :return: None (sets self.rdflib_graph and self.sources_valid)
        """

        # if self.verbose: printDebug("----------")
        if self.verbose: printDebug("Reading: <%s>" % uri, fg="green")
        success = False

        sorted_fmt_opts = try_sort_fmt_opts(self.rdf_format_opts, uri)

        for f in sorted_fmt_opts:
            if self.verbose:
                printDebug(".. trying rdf serialization: <%s>" % f)
            try:
                if f == 'json-ld':
                    if self.verbose:
                        printDebug(
                            "Detected JSONLD - loading data into rdflib.ConjunctiveGraph()",
                            fg='green')
                    temp_graph = rdflib.ConjunctiveGraph()
                else:
                    temp_graph = rdflib.Graph()
                temp_graph.parse(uri, format=f)
                if self.verbose: printDebug("..... success!", bold=True)
                success = True
                self.sources_valid += [uri]
                # ok, so merge
                self.rdflib_graph = self.rdflib_graph + temp_graph
                break
            except:
                temp = None
                if self.verbose: printDebug("..... failed")
                # self._debugGraph()

        if not success == True:
            self.loading_failed(sorted_fmt_opts, uri=uri)
            self.sources_invalid += [uri]

    def load_data(self, data):
        """

        :param data:
        :param rdf_format_opts:
        :return:
        """
        if self.verbose: printDebug("----------")
        if self.verbose: printDebug("Reading: '%s ...'" % data[:10])
        success = False
        for f in self.rdf_format_opts:
            if self.verbose:
                printDebug(".. trying rdf serialization: <%s>" % f)
            try:
                if f == 'json-ld':
                    self._fix_default_graph_for_jsonld()
                self.rdflib_graph.parse(data=data, format=f)
                if self.verbose: printDebug("..... success!")
                success = True
                self.sources_valid += ["Data: '%s ...'" % data[:10]]
                break
            except:
                if self.verbose: printDebug("..... failed", "error")

        if not success == True:
            self.loading_failed(self.rdf_format_opts)
            self.sources_invalid += ["Data: '%s ...'" % data[:10]]

    def load_file(file_obj):
        """
        The type of open file objects such as sys.stdout; alias of the built-in file.
        @TODO: when is this used?
        """
        if self.verbose: printDebug("----------")
        if self.verbose: printDebug("Reading: <%s> ...'" % file_obj.name)

        if type(file_obj) == file:
            self.rdflib_graph = self.rdflib_graph + file_obj
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

    def print_summary(self):
        """
        print out stats about loading operation
        """
        if self.sources_valid:
            printDebug(
                "----------\nLoaded %d triples.\n----------" % len(
                    self.rdflib_graph),
                fg='white')
            printDebug(
                "RDF sources loaded successfully: %d of %d." %
                (len(self.sources_valid),
                 len(self.sources_valid) + len(self.sources_invalid)),
                fg='green')
            for s in self.sources_valid:
                printDebug("..... '" + s + "'", fg='white')
            printDebug("----------", fg='white')
        else:
            printDebug("Sorry - no valid RDF was found", fg='red')

        if self.sources_invalid:
            printDebug(
                "----------\nRDF sources failed to load: %d.\n----------" %
                (len(self.sources_invalid)),
                fg='red')
            for s in self.sources_invalid:
                printDebug("-> " + s, fg="red")

    def loading_failed(self, rdf_format_opts, uri=""):
        """default message if we need to abort loading"""
        if uri:
            uri = " <%s>" % str(uri)
        printDebug(
            "----------\nFatal error parsing graph%s\n(using RDF serializations: %s)"
            % (uri, str(rdf_format_opts)), "red")
        printDebug(
            "----------\nTIP: You can try one of the following RDF validation services\n<http://mowl-power.cs.man.ac.uk:8080/validator/validate>\n<http://www.ivan-herman.net/Misc/2008/owlrl/>"
        )

        return


##
# testing
##


@click.command()
@click.argument('uri_or_path', nargs=-1, type=click.STRING)
@click.option('--noverbose', is_flag=True, help='Turn off verbose mode.')
@click.option(
    '--trylist', is_flag=True, help='Try loading a predefined list of files.')
def test(uri_or_path, noverbose, trylist):
    l = RDFLoader(verbose=not (noverbose))
    if trylist or not uri_or_path:
        l.load(["http://purl.org/dc/terms/", "http://xmlns.com/foaf/spec/"])
    else:
        l.load(uri_or_path)


if __name__ == '__main__':
    """
    simple test: python -m ontospy.core.rdf_loader [PATH] [OPTIONS]
    """
    test()
    printDebug("Finished")
