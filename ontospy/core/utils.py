# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Python and RDF Utils for Ontospy

Copyright (c) 2010-2015 __Michele Pasin__ <http://www.michelepasin.org>. All rights reserved.

"""

from __future__ import print_function

from colorama import Fore, Style

import rdflib
from rdflib import RDFS, RDF, BNode
from rdflib.namespace import OWL, DC
DEFAULT_LANGUAGE = "en"

import sys, os, subprocess, random, platform

import click

# Fix Python 2.x.
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)

# ===========
# generic python utils
# ===========


def is_http(stringa):
    if stringa:
        if stringa.startswith("http://") or stringa.startswith("https://"):
            return True
    return False


def safe_str(u, errors="replace"):
    """Safely print the given string.

    If you want to see the code points for unprintable characters then you
    can use `errors="xmlcharrefreplace"`.
    http://code.activestate.com/recipes/576602-safe-print/
    """
    s = u.encode(sys.stdout.encoding or "utf-8", errors)
    return s


def list_chunks(l, n):
    """Yield successive n-sized chunks from l.

    import pprint
    pprint.pprint(list(chunks(range(10, 75), 10)))
    [[10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
     [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
     [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
     [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
     [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
     [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
     [70, 71, 72, 73, 74]]

    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def split_list(alist, wanted_parts=1):
    """
    A = [0,1,2,3,4,5,6,7,8,9]

    print split_list(A, wanted_parts=1)
    print split_list(A, wanted_parts=2)
    print split_list(A, wanted_parts=8)
    """
    length = len(alist)
    return [
        alist[i * length // wanted_parts:(i + 1) * length // wanted_parts]
        for i in range(wanted_parts)
    ]


def remove_duplicates(seq, idfun=None):
    """ removes duplicates from a list, order preserving, as found in
    http://www.peterbe.com/plog/uniqifiers-benchmark
    """
    # order preserving
    if idfun is None:

        def idfun(x):
            return x

    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def printDebug(text, mystyle="", **kwargs):
    """
    util for printing in colors using click.secho()

    :kwargs = you can do printDebug("s", bold=True)

    2018-12-06: by default print to standard error (err=True)

    Styling output:
    <http://click.pocoo.org/5/api/#click.style>
    Styles a text with ANSI styles and returns the new string. By default the styling is self contained which means that at the end of the string a reset code is issued. This can be prevented by passing reset=False.

    Examples:

    click.echo(click.style('Hello World!', fg='green'))
    click.echo(click.style('ATTENTION!', blink=True))
    click.echo(click.style('Some things', reverse=True, fg='cyan'))
    Supported color names:

    black (might be a gray)
    red
    green
    yellow (might be an orange)
    blue
    magenta
    cyan
    white (might be light gray)
    reset (reset the color code only)
    New in version 2.0.

    Parameters:
    text – the string to style with ansi codes.
    fg – if provided this will become the foreground color.
    bg – if provided this will become the background color.
    bold – if provided this will enable or disable bold mode.
    dim – if provided this will enable or disable dim mode. This is badly supported.
    underline – if provided this will enable or disable underline.
    blink – if provided this will enable or disable blinking.
    reverse – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).
    reset – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

    """

    if mystyle == "comment":
        click.secho(text, dim=True, err=True)
    elif mystyle == "important":
        click.secho(text, bold=True, err=True)
    elif mystyle == "normal":
        click.secho(text, reset=True, err=True)
    elif mystyle == "red" or mystyle == "error":
        click.secho(text, fg='red', err=True)
    elif mystyle == "green":
        click.secho(text, fg='green', err=True)
    else:
        click.secho(text, **kwargs)


def printComment(text, mystyle="comment", **kwargs):
    """
    wrapper around click.secho()
    .. same as printDebug, but just one option
    [for backward compatibility]
    """

    click.secho(text, fg='green', **kwargs)


def OLD_printDebug(s, style=None):
    """
    util for printing in colors to sys.stderr stream
    """
    if style == "comment":
        s = Style.DIM + s + Style.RESET_ALL
    elif style == "important":
        s = Style.BRIGHT + s + Style.RESET_ALL
    elif style == "normal":
        s = Style.RESET_ALL + s + Style.RESET_ALL
    elif style == "red":
        s = Fore.RED + s + Style.RESET_ALL
    elif style == "green":
        s = Fore.GREEN + s + Style.RESET_ALL
    try:
        print(s, file=sys.stderr)
    except:
        pass


def pprint2columns(llist, max_length=60):
    """
    llist = a list of strings
    max_length = if a word is longer than that, for single col display

    > prints a list in two columns, taking care of alignment too
    """
    if len(llist) == 0:
        return None

    col_width = max(len(word) for word in llist) + 2  # padding

    # llist length must be even, otherwise splitting fails
    if not len(llist) % 2 == 0:
        llist += [' ']  # add a fake element

    if col_width > max_length:
        for el in llist:
            print(el)
    else:
        column1 = llist[:int(len(llist) / 2)]
        column2 = llist[int(len(llist) / 2):]
        for c1, c2 in zip(column1, column2):
            space = " " * (col_width - len(c1))
            print("%s%s%s" % (c1, space, c2))


def pprinttable(rows):
    """
    Pretty prints a table via python
    http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables

    Example

    >>> from collections import namedtuple
    >>> Row = namedtuple('Row',['first','second','third'])
    >>> data = Row(1,2,3)
    >>> data
    Row(first=1, second=2, third=3)
    >>> pprinttable([data])
     first = 1
    second = 2
     third = 3
    >>> pprinttable([data,data])
    first | second | third
    ------+--------+------
        1 |		 2 |	 3
        1 |		 2 |	 3

    """
    if len(rows) > 1:
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(
                len(
                    max([x[i] for x in rows] + [headers[i]],
                        key=lambda x: len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "-+-".join(['-' * n for n in lens])
        print(hpattern % tuple(headers))
        print(separator)
        for line in rows:
            print(pattern % tuple(line))
    elif len(rows) == 1:
        row = rows[0]
        hwidth = len(max(row._fields, key=lambda x: len(x)))
        for i in range(len(row)):
            print("%*s = %s" % (hwidth, row._fields[i], row[i]))


def save_anonymous_gist(title, files):
    """
    October 21, 2015
    title = the gist title
    files = {
        'spam.txt' : {
            'content': 'What... is the air-speed velocity of an unladen swallow?'
            }
            # ..etc...
        }

    works also in blocks eg from
    https://gist.github.com/anonymous/b839e3a4d596b215296f
    to
    http://bl.ocks.org/anonymous/b839e3a4d596b215296f

    So we return 3 different urls

    """

    try:
        from github3 import create_gist
    except:
        print("github3 library not found (pip install github3)")
        raise SystemExit(1)

    gist = create_gist(title, files)

    urls = {
        'gist':
        gist.html_url,
        'blocks':
        "http://bl.ocks.org/anonymous/" + gist.html_url.split("/")[-1],
        'blocks_fullwin':
        "http://bl.ocks.org/anonymous/raw/" + gist.html_url.split("/")[-1]
    }

    return urls


def _clear_screen():
    """ http://stackoverflow.com/questions/18937058/python-clear-screen-in-shell """
    if platform.system() == "Windows":
        tmp = os.system('cls')  #for window
    else:
        tmp = os.system('clear')  #for Linux
    return True


def addQuotes(s):
    """wrap a strings with quotes"""
    return "\"" + s + "\""


class bcolors:
    """
    http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    eg print bcolors.YELLOW + "Warning: No active frommets remain. Continue?"
    """
    PINK = '\033[95m'  # pink
    BLUE = '\033[94m'  # blue
    GREEN = '\033[92m'  # green
    YELLOW = '\033[93m'  # yellow
    RED = '\033[91m'  # red
    ENDC = '\033[0m'
    BOLD = '\033[1m'  # bold black
    UNDERLINE = '\033[4m'  # underline (note: must be ended)


def playSound(folder, name=""):
    """ as easy as that """
    try:
        if not name:
            onlyfiles = [
                f for f in os.listdir(folder)
                if os.path.isfile(os.path.join(folder, f))
            ]
            name = random.choice(onlyfiles)
        subprocess.call(["afplay", folder + name])
        # subprocess.call(["say", "%d started, batch %d" % (adate, batch)])
    except:
        pass


def truncate(data, l=20):
    "truncate a string"
    info = (data[:l] + '..') if len(data) > l else data
    return info


# ========
# rdf utils
# ===========

NAMESPACES_DEFAULT = [
    ("rdf", rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")),
    ("rdfs", rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#")),
    ("xml", rdflib.URIRef("http://www.w3.org/XML/1998/namespace")),
    ("xsd", rdflib.URIRef("http://www.w3.org/2001/XMLSchema#")),
    ('foaf', rdflib.URIRef("http://xmlns.com/foaf/0.1/")),
    ("skos", rdflib.URIRef("http://www.w3.org/2004/02/skos/core#")),
    ("owl", rdflib.URIRef("http://www.w3.org/2002/07/owl#")),
]


def isBlankNode(aClass):
    """ small utility that checks if a class is a blank node """
    if type(aClass) == BNode:
        return True
    else:
        return False


def printBasicInfo(onto):
    """
    Terminal printing of basic ontology information
    """
    rdfGraph = onto.rdflib_graph

    print("_" * 50, "\n")
    print("TRIPLES = %s" % len(rdfGraph))
    print("_" * 50)
    print("\nNAMESPACES:\n")
    for x in onto.ontologyNamespaces:
        print("%s : %s" % (x[0], x[1]))

    print("_" * 50, "\n")
    print("ONTOLOGY METADATA:\n")
    for x, y in onto.ontologyAnnotations():
        print("%s: \n	 %s" % (uri2niceString(x, onto.ontologyNamespaces),
                              uri2niceString(y, onto.ontologyNamespaces)))
    print("_" * 50, "\n")

    print("CLASS TAXONOMY:\n")
    onto.printClassTree()
    print("_" * 50, "\n")


def inferMainPropertyType(uriref):
    """
    Attempt to reduce the property types to 4 main types
    (without the OWL ontology - which would be the propert way)

    In [3]: for x in g.all_properties:
       ...:		print x.rdftype
       ...:
    http://www.w3.org/2002/07/owl#FunctionalProperty
    http://www.w3.org/2002/07/owl#FunctionalProperty
    http://www.w3.org/2002/07/owl#InverseFunctionalProperty
    http://www.w3.org/2002/07/owl#ObjectProperty
    http://www.w3.org/2002/07/owl#ObjectProperty
    http://www.w3.org/2002/07/owl#TransitiveProperty
    http://www.w3.org/2002/07/owl#TransitiveProperty
    etc.....
    """
    if uriref:
        if uriref == rdflib.OWL.DatatypeProperty:
            return uriref
        elif uriref == rdflib.OWL.AnnotationProperty:
            return uriref
        elif uriref == rdflib.RDF.Property:
            return uriref
        else:  # hack..
            return rdflib.OWL.ObjectProperty
    else:
        return None


def printGenericTree(element,
                     level=0,
                     showids=True,
                     labels=False,
                     showtype=True,
                     TYPE_MARGIN=18):
    """
    Print nicely into stdout the taxonomical tree of an ontology.

    Works irrespectively of whether it's a class or property.

    Note: indentation is made so that ids up to 3 digits fit in, plus a space.
    [123]1--
    [1]123--
    [12]12--

    <TYPE_MARGIN> is parametrized so that classes and properties can have different default spacing (eg owl:class vs owl:AnnotationProperty)
    """

    ID_MARGIN = 5

    SHORT_TYPES = {
        "rdf:Property": "rdf:Property",
        "owl:AnnotationProperty": "owl:Annot.Pr.",
        "owl:DatatypeProperty": "owl:DatatypePr.",
        "owl:ObjectProperty": "owl:ObjectPr.",
    }

    if showids:
        _id_ = Fore.BLUE +	\
        "[%d]%s" % (element.id, " " * (ID_MARGIN  - len(str(element.id)))) +  \
            Fore.RESET

    elif showtype:
        _prop = uri2niceString(element.rdftype)
        try:
            prop = SHORT_TYPES[_prop]
        except:
            prop = _prop
        _id_ = Fore.BLUE +	\
        "[%s]%s" % (prop, " " * (TYPE_MARGIN  - len(prop))) + Fore.RESET

    else:
        _id_ = ""

    if labels:
        bestLabel = element.bestLabel(qname_allowed=False)
        if bestLabel:
            bestLabel = Fore.MAGENTA + " (\"%s\")" % bestLabel + Fore.RESET
    else:
        bestLabel = ""

    printDebug("%s%s%s%s" % (_id_, "-" * 4 * level, element.qname, bestLabel))

    # recursion
    for sub in element.children():
        printGenericTree(sub, (level + 1), showids, labels, showtype,
                         TYPE_MARGIN)


def firstStringInList(literalEntities, prefLanguage="en"):
    """
    from a list of literals, returns the one in prefLanguage
    if no language specification is available, return first element
    """
    match = ""

    if len(literalEntities) == 1:
        match = literalEntities[0]
    elif len(literalEntities) > 1:
        for x in literalEntities:
            if getattr(x, 'language') and getattr(x,
                                                  'language') == prefLanguage:
                match = x
        if not match:  # don't bother about language
            match = literalEntities[0]
    return match


def firstEnglishStringInList(literalEntities, ):
    return firstStringInList(literalEntities, "en")


def joinStringsInList(literalEntities, prefLanguage="en"):
    """
    from a list of literals, returns the ones in prefLanguage joined up.
    if the desired language specification is not available, join all up
    """
    match = []

    if len(literalEntities) == 1:
        return literalEntities[0]
    elif len(literalEntities) > 1:
        for x in literalEntities:
            if getattr(x, 'language') and getattr(x,
                                                  'language') == prefLanguage:
                match.append(x)
        if not match:  # don't bother about language
            for x in literalEntities:
                match.append(x)

    return " - ".join([x for x in match])



def sortByNamespacePrefix(urisList, nsList):
    """
        Given an ordered list of namespaces prefixes, order a list of uris based on that.
        Eg

        In [7]: ll
        Out[7]:
        [rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
         rdflib.term.URIRef(u'printGenericTreeorg/2000/01/rdf-schema#comment'),
         rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
         rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')]

        In [8]: sortByNamespacePrefix(ll, [OWL.OWLNS, RDFS])
        Out[8]:
        [rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'),
         rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
         rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
         rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')]

    """
    exit = []
    urisList = sort_uri_list_by_name(urisList)
    for ns in nsList:
        innerexit = []
        for uri in urisList:
            if str(uri).startswith(str(ns)):
                innerexit += [uri]
        exit += innerexit

    # add remaining uris (if any)
    for uri in urisList:
        if uri not in exit:
            exit += [uri]

    return exit


def sort_uri_list_by_name(uri_list, bypassNamespace=False):
    """
     Sorts a list of uris

     bypassNamespace:
        based on the last bit (usually the name after the namespace) of a uri
        It checks whether the last bit is specified using a # or just a /, eg:
             rdflib.URIRef('http://purl.org/ontology/mo/Vinyl'),
             rdflib.URIRef('http://purl.org/vocab/frbr/core#Work')

     """

    def get_last_bit(uri_string):
        try:
            x = uri_string.split("#")[1]
        except:
            x = uri_string.split("/")[-1]
        return x

    try:
        if bypassNamespace:
            return sorted(uri_list, key=lambda x: get_last_bit(x.__str__()))
        else:
            return sorted(uri_list)
    except:
        # TODO: do more testing.. maybe use a unicode-safe method instead of __str__
        print(
            "Error in <sort_uri_list_by_name>: possibly a UnicodeEncodeError")
        return uri_list


def guess_fileformat(aUri):
    """
    Simple file format guessing (using rdflib format types) based on the suffix

    see rdflib.parse [https://rdflib.readthedocs.org/en/latest/using_graphs.html]

    """
    if aUri.endswith(".xml"):
        return "xml"
    elif aUri.endswith(".nt"):
        return "nt"
    elif aUri.endswith(".n3") or aUri.endswith(".ttl"):
        return "n3"
    elif aUri.endswith(".trix"):
        return "trix"
    elif aUri.endswith(".rdfa"):
        return "rdfa"
    else:  # to be handled outside this method
        return None


def inferNamespacePrefix(aUri):
    """
    From a URI returns the last bit and simulates a namespace prefix when rendering the ontology.

    eg from <'http://www.w3.org/2008/05/skos#'>
        it returns the 'skos' string
    """
    stringa = aUri.__str__()
    try:
        prefix = stringa.replace("#", "").split("/")[-1]
    except:
        prefix = ""
    return prefix


def inferURILocalSymbol(aUri):
    """
    From a URI returns a tuple (namespace, uri-last-bit)

    Eg
    from <'http://www.w3.org/2008/05/skos#something'>
        ==> ('something', 'http://www.w3.org/2008/05/skos')
    from <'http://www.w3.org/2003/01/geo/wgs84_pos'> we extract
        ==> ('wgs84_pos', 'http://www.w3.org/2003/01/geo/')

    """
    # stringa = aUri.__str__()
    stringa = aUri
    try:
        ns = stringa.split("#")[0]
        name = stringa.split("#")[1]
    except:
        if "/" in stringa:
            ns = stringa.rsplit("/", 1)[0]
            name = stringa.rsplit("/", 1)[1]
        else:
            ns = ""
            name = stringa
    return (name, ns)


def uri2niceString(aUri, namespaces=None):
    """
    From a URI, returns a nice string representation that uses also the namespace symbols
    Cuts the uri of the namespace, and replaces it with its shortcut (for base, attempts to infer it or leaves it blank)

    Namespaces are a list

    [('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
    ('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
    (u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
    ('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
    ('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
    (u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))]

    """
    if not namespaces:
        namespaces = NAMESPACES_DEFAULT

    if type(aUri) == rdflib.term.URIRef:
        # we have a URI: try to create a qName
        stringa = aUri.toPython()
        for aNamespaceTuple in namespaces:
            try:  # check if it matches the available NS
                if stringa.find(aNamespaceTuple[1].__str__()) == 0:
                    if aNamespaceTuple[0]:  # for base NS, it's empty
                        stringa = aNamespaceTuple[0] + ":" + stringa[len(
                            aNamespaceTuple[1].__str__()):]
                    else:
                        prefix = inferNamespacePrefix(aNamespaceTuple[1])
                        if prefix:
                            stringa = prefix + ":" + stringa[len(
                                aNamespaceTuple[1].__str__()):]
                        else:
                            stringa = ":" + stringa[len(aNamespaceTuple[1].
                                                        __str__()):]
            except:
                stringa = "error"

    elif type(aUri) == rdflib.term.Literal:
        stringa = "\"%s\"" % aUri  # no string casting so to prevent encoding errors
    else:
        # print(type(aUri))
        if type(aUri) == type(u''):
            stringa = aUri
        else:
            stringa = aUri.toPython()
    return stringa


def niceString2uri(aUriString, namespaces=None):
    """
    From a string representing a URI possibly with the namespace qname, returns a URI instance.

    gold:Citation  ==> rdflib.term.URIRef(u'http://purl.org/linguistics/gold/Citation')

    Namespaces are a list

    [('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
    ('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
    (u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
    ('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
    ('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
    (u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))]

    """

    if not namespaces:
        namespaces = []

    for aNamespaceTuple in namespaces:
        if aNamespaceTuple[0] and aUriString.find(
                aNamespaceTuple[0].__str__() + ":") == 0:
            aUriString_name = aUriString.split(":")[1]
            return rdflib.term.URIRef(aNamespaceTuple[1] + aUriString_name)

    # we dont handle the 'base' URI case
    return rdflib.term.URIRef(aUriString)


def entityLabel(rdfGraph, anEntity, language=DEFAULT_LANGUAGE, getall=True):
    """
    Returns the rdfs.label value of an entity (class or property), if existing.
    Defaults to DEFAULT_LANGUAGE. Returns the RDF.Literal resource

    Args:
    language: 'en', 'it' etc..
    getall: returns a list of all labels rather than a string

    """

    if getall:
        temp = []
        for o in rdfGraph.objects(anEntity, RDFS.label):
            temp += [o]
        return temp
    else:
        for o in rdfGraph.objects(anEntity, RDFS.label):
            if getattr(o, 'language') and getattr(o, 'language') == language:
                return o
        return ""


def entityComment(rdfGraph, anEntity, language=DEFAULT_LANGUAGE, getall=True):
    """
    Returns the rdfs.comment value of an entity (class or property), if existing.
    Defaults to DEFAULT_LANGUAGE. Returns the RDF.Literal resource

    Args:
    language: 'en', 'it' etc..
    getall: returns a list of all labels rather than a string

    """

    if getall:
        temp = []
        for o in rdfGraph.objects(anEntity, RDFS.comment):
            temp += [o]
        return temp
    else:
        for o in rdfGraph.objects(anEntity, RDFS.comment):
            if getattr(o, 'language') and getattr(o, 'language') == language:
                return o
        return ""


def shellPrintOverview(g, opts={'labels': False}):
    """
    overview of graph invoked from command line

    @todo
    add pagination via something like this
    # import pydoc
    # pydoc.pager("SOME_VERY_LONG_TEXT")

    """
    ontologies = g.all_ontologies

    # get opts
    try:
        labels = opts['labels']
    except:
        labels = False

    print(Style.BRIGHT + "\nOntologies\n-----------" + Style.RESET_ALL)
    if ontologies:
        for o in ontologies:
            o.printTriples()
    else:
        printDebug("None found", "comment")

    print(Style.BRIGHT + "\nClasses\n" + "-" * 10 + Style.RESET_ALL)
    if g.all_classes:
        g.printClassTree(showids=False, labels=labels)
    else:
        printDebug("None found", "comment")

    print(Style.BRIGHT + "\nProperties\n" + "-" * 10 + Style.RESET_ALL)
    if g.all_properties:
        g.printPropertyTree(showids=False, labels=labels)
    else:
        printDebug("None found", "comment")

    print(Style.BRIGHT + "\nSKOS Concepts\n" + "-" * 10 + Style.RESET_ALL)
    if g.all_skos_concepts:

        g.printSkosTree(showids=False, labels=labels)
    else:
        printDebug("None found", "comment")

    print(Style.BRIGHT + "\nSHACL Shapes\n" + "-" * 10 + Style.RESET_ALL)
    if g.all_shapes:

        for x in g.all_shapes:
            printDebug("%s" % (x.qname))
            # printDebug("%s" % (x.bestLabel()), "comment")
    else:
        printDebug("None found", "comment")


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    """
    import unicodedata, re
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value.decode()).strip().lower())
    value = re.sub('[-\s]+', '-', value)
    return value


def get_files_with_extensions(folder, extensions):
    """walk dir and return .* files as a list
    Note: directories are walked recursively"""
    out = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension.replace(".", "") in extensions:
                out += [os.path.join(root, file)]
                # break

    return out


def try_sort_fmt_opts(rdf_format_opts_list, uri):
    """reorder fmt options based on uri file type suffix - if available - so to test most likely serialization first when parsing some RDF 

    NOTE this is not very nice as it is hardcoded and assumes the origin serializations to be this: ['turtle', 'xml', 'n3', 'nt', 'json-ld', 'rdfa']
    
    """
    filename, file_extension = os.path.splitext(uri)
    # print(filename, file_extension)
    if file_extension == ".ttl" or file_extension == ".turtle":
        return ['turtle', 'n3', 'nt', 'json-ld', 'rdfa', 'xml']
    elif file_extension == ".xml" or file_extension == ".rdf":
        return ['xml', 'turtle', 'n3', 'nt', 'json-ld', 'rdfa']
    elif file_extension == ".nt" or file_extension == ".n3":
        return ['n3', 'nt', 'turtle', 'xml', 'json-ld', 'rdfa']
    elif file_extension == ".json" or file_extension == ".jsonld":
        return [
            'json-ld',
            'rdfa',
            'n3',
            'nt',
            'turtle',
            'xml',
        ]
    elif file_extension == ".rdfa":
        return [
            'rdfa',
            'json-ld',
            'n3',
            'nt',
            'turtle',
            'xml',
        ]
    else:
        return rdf_format_opts_list
