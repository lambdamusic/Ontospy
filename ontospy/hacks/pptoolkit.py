#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary

test of https://github.com/jonathanslenders/python-prompt-toolkit

HowTo

>python -m ontospy.hacks.pptoolkit


"""

from __future__ import unicode_literals
from __future__ import print_function
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

from .. import main
from .. import VERSION
from ..core.ontospy import Ontospy
from ..core.utils import *


test_style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
})


def main():
    def get_bottom_toolbar_tokens(cli):
        print(cli.__class__)
        print(cli.current_buffer_name)
        return [(Token.Toolbar, ' OntoSpy ' + VERSION.VERSION)]

    text = prompt('Say something: ',
                  get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                  style=test_style)
    print('You said: %s' % text)


if __name__ == '__main__':
    main()
