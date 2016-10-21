#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary

An attempt to build a sparql console using python-prompt toolking

Idea:
either pass a sparql endpoint / or a graph URI which is loaded in memory using RDFLib
= useful to test things out quickly!


NOTE: > problem with Sparql Lexer
https://bitbucket.org/birkenfeld/pygments-main/issues/1236/sparql-lexer-error
"fixed in 2.2 release soon"

TODO - revise in near future

2016-10-21
try install this commit?
https://bitbucket.org/birkenfeld/pygments-main/commits/60afc531aa2b
>> installed manually 'hg clone https://bitbucket.org/birkenfeld/pygments-main'
and it works


"""

from __future__ import unicode_literals
import sys
import pygments

import rdflib

import click

from ..core.loader import RDFLoader

#http://stackoverflow.com/questions/1714027/version-number-comparison
from distutils.version import StrictVersion

if StrictVersion(pygments.__version__) <= StrictVersion('2.1'):
    print "Pygments version 2.2 minimum required (you have %s)" % pygments.__version__
    sys.exit()


from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from pygments.lexers.rdf import SparqlLexer
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

sparql_completer = WordCompleter(['select', 'insert', 'distinct', 'count', 
                                  'delete', 'where', 
                                  'select distinct ?c where {?a a ?c}',
                                  'select * where {?a ?b ?c}',
                                  ], ignore_case=True)

class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)

def main(db):
    history = InMemoryHistory()
    # connection = sqlite3.connect(database)

    if db:
        _db = RDFLoader()
        db = _db.load(db)
    else:
        db = rdflib.Graph()

    while True:
        try:
            text = prompt('> ', lexer=SparqlLexer, completer=sparql_completer,
                          style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break  # Control-D pressed.

        if text:
            print("You said \"" + text + "\" (triples in DB: %d)" % len(db))

            res = run_query(text, db)

            try:
                print_results(res)
            except:
                e = sys.exc_info()[0]
                print "--error--->", e

        
    print('GoodBye!')



def run_query(q, db):
    
    try:
        qres = db.query(
            """%s""" % q)
        return list(qres)
    except:
        e = sys.exc_info()[0]
        print "--error--->", e
        return None


def add_ns(db):
    db.bind("rdf", rdflib.namespace.RDF)
    db.bind("rdfs", rdflib.namespace.RDFS)
    db.bind("owl", rdflib.namespace.OWL)
    db.bind("skos", rdflib.namespace.SKOS)



def print_results(res):

    if True:
        if res:
            counter = 0
            for row in res:
                counter += 1
                click.secho("%d. " % counter, fg='green')
                print " ,".join([unicode(x) for x in row])
        else:
            click.secho("No results", fg='red')

    if False:
        # pprinttable: works but the alignment is messed up!
        # probably better to output as HTML and open in browser..
        # @todo delete
        from collections import namedtuple  
        from ..core.utils import pprinttable
        howlong = len(res[0])
        Row = namedtuple('Row', ["Col%d" % (n+1) for n in range(howlong)])
        data = []
        counter = 0
        for row in res:
            counter += 1
            inner_data = []
            for x in row:
                inner_data += [unicode(x)]

            data.append(Row._make(inner_data))
            # print data
        pprinttable(data)




if __name__ == '__main__':
    if len(sys.argv) < 2:
        db = None
    else:
        db = sys.argv[1]

    main(db)
