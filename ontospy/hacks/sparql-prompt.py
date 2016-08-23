#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary

An attempt to build a sparql console using python-prompt toolking

NOTE: > problem with Sparql Lexer
https://bitbucket.org/birkenfeld/pygments-main/issues/1236/sparql-lexer-error
"fixed in 2.2 release soon"

TODO - revise in near future


"""


from __future__ import unicode_literals
import sys

from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from pygments.lexers.rdf import SparqlLexer
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

sparql_completer = WordCompleter(['select', 'insert',
                                  'delete', 'where',], ignore_case=True)

class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)

def main(database):
    history = InMemoryHistory()
    # connection = sqlite3.connect(database)

    while True:
        try:
            text = prompt('> ', lexer=SparqlLexer, completer=sparql_completer,
                          style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break  # Control-D pressed.

        print("You said " + text)
        # with connection:
        #     try:
        #         messages = connection.execute(text)
        #     except Exception as e:
        #         print(repr(e))
        #     else:
        #         for message in messages:
        #             print(message)
        
    print('GoodBye!')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        db = ':memory:'
    else:
        db = sys.argv[1]

    main(db)
