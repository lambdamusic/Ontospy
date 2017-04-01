# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

# https://github3py.readthedocs.org/en/master/examples/gist.html#creating-an-anonymous-gist

# >sudo pip install github3.py

from __future__ import print_function

from github3 import create_gist

files = {
    'spam.txt' : {
        'content': 'What... is the air-speed velocity of an unladen swallow?'
        }
    }
try:
    gist = create_gist('Answer this to cross the bridge', files)
    comments = [c for c in gist.iter_comments()]
    # []

    comment = gist.create_comment('Bogus. This will not work.')

# Which of course it didn't, because you're not logged in
# comment == None
    print(gist.html_url)


# works also in blocks eg from
# https://gist.github.com/anonymous/b839e3a4d596b215296f
# to
# http://bl.ocks.org/anonymous/b839e3a4d596b215296f

except Exception as e:
    print(e)
