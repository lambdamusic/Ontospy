#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary

An attempt to build a Turtle console using python-prompt-toolking

"""


from __future__ import unicode_literals
import sys

from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import style_from_dict

from pygments.lexers.rdf import TurtleLexer
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

from .. import ontospy
from .vocabsturtleprompt import rdfschema, rdfsschema, owlschema



def get_default_preds():
    """dynamically build autocomplete options based on an external file"""
    g = ontospy.Graph(rdfsschema, text=True, verbose=False, hide_base_schemas=False)
    classes = [(x.qname, x.bestDescription()) for x in g.classes]
    properties = [(x.qname, x.bestDescription()) for x in g.properties]
    
    return rdfschema + owlschema + classes + properties

turtle_completer = WordCompleter([x[0] for x in get_default_preds()], ignore_case=True)


# BOTTOM TOOLBAR

def get_bottom_toolbar_tokens(cli):
    # TIP: in order to analyze current text:
    # t = cli.current_buffer.document.current_line
    return [(Token.Toolbar, "Please enter some Turtle. [TIP: esc|meta + enter to submit / Control-D to exit]" )]

style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
})


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
        Token.Toolbar: '#ffffff bg:#333333',
    }
    styles.update(DefaultStyle.styles)


def main(database):
    history = InMemoryHistory()
    # connection = sqlite3.connect(database)
    
    while True:
        try:
            text = prompt('> ', lexer=TurtleLexer, completer=turtle_completer,
                          display_completions_in_columns=False,
                          complete_while_typing=False,
                          multiline=True,
                          get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                          style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break  # Control-D pressed.

        print("You said \n---\n" + text + "\n---")
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
    print("Initiating...")
    if len(sys.argv) < 2:
        # not relevant anymore.. but left here for ideas..
        db = ':memory:'
    else:
        db = sys.argv[1]

    main(db)
