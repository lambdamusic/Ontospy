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

from pygments import highlight
from pygments.lexers.rdf import TurtleLexer
from pygments.formatters import Terminal256Formatter
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token

from ..core import ontospy
from .vocabsturtleprompt import rdfschema, rdfsschema, owlschema



def clear_screen():
    import os, platform
    """ http://stackoverflow.com/questions/18937058/python-clear-screen-in-shell """
    if platform.system() == "Windows":
        tmp = os.system('cls') #for window
    else:
        tmp = os.system('clear') #for Linux
    return True


def get_default_preds():
    """dynamically build autocomplete options based on an external file"""
    g = ontospy.Ontospy(rdfsschema, text=True, verbose=False, hide_base_schemas=False)
    classes = [(x.qname, x.bestDescription()) for x in g.all_classes]
    properties = [(x.qname, x.bestDescription()) for x in g.all_properties]
    commands = [('exit', 'exits the terminal'), ('show', 'show current buffer')]
    return rdfschema + owlschema + classes + properties + commands

turtle_completer = WordCompleter([x[0] for x in get_default_preds()], ignore_case=True, WORD=True)


# BOTTOM TOOLBAR

def get_bottom_toolbar_tokens(cli):
    # TIP: in order to analyze current text:
    # t = cli.current_buffer.document.current_line
    return [(Token.Toolbar, "Please enter some Turtle. [TIP: esc|meta + enter to submit / 'exit' = exit]" )]

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
    buffer = ""

    while True:
        try:
            text = prompt('> ', lexer=TurtleLexer, completer=turtle_completer,
                          display_completions_in_columns=False,
                          complete_while_typing=False,
                          # multiline=True,
                          get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                          style=DocumentStyle, history=history,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break  # Control-D pressed.

        if text == "exit":
            break
        elif text == "show":
            # print highlight(code, PythonLexer())
            print("You said \n---\n" + highlight(buffer, TurtleLexer(), Terminal256Formatter()) + "---")
        else:
            if text:
                buffer += text + "\n"


    print('GoodBye!')

if __name__ == '__main__':
    clear_screen()
    print("Initiating...")
    if len(sys.argv) < 2:
        # not relevant anymore.. but left here for ideas..
        db = ':memory:'
    else:
        db = sys.argv[1]

    main(db)
