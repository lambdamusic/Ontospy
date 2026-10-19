#!/usr/bin/python
# -*- coding: utf-8 -*-

VISUALIZATIONS_LIST = {
    "Visualizations": [{
        "ID": "html-simple",
        "Title": "Html: single page",
        "Description": "@todo",
    },
                       {
                           "ID": "html-complex",
                           "Title": "Html: multi page",
                           "Description": "@todo",
                       },
                       {
                           "ID": "markdown",
                           "Title": "Markdown: multi page",
                           "Description": "@todo",
                       },
                       {
                           "ID": "d3-dendogram",
                           "Title": "D3 Dendrogram",
                           "Description": "@todo",
                       },
                       {
                           "ID": "d3-bubble-chart",
                           "Title": "D3 Bubble chart",
                           "Description": "@todo",
                       },
                       {
                           "ID": "d3-pack-hierarchy",
                           "Title": "D3 Pack hierarchy",
                           "Description": "@todo",
                       }]
}

# A viz's --type number is its position in the list above, from 1, unless it has a
# "Number": new vizs take numbers above 10, so that the removed ones below aren't reused.

# Removed in 2.6 (backlog #25), by their former --type number: (ID, title). Their numbers
# aren't reused for a release or two, so that a script asking for one fails clearly
# rather than getting another visualization.
REMOVED_VISUALIZATIONS = {
    7: ("d3-bar-hierarchy", "D3 Bar hierarchy"),
    8: ("d3-partition-table", "D3 Partition table"),
    9: ("d3-rotating-cluster", "D3 Rotating cluster"),
    10: ("sigma-force-directed", "Sigma.js Force directed graph"),
}
REMOVED_IN = "2.6"

BOOTSWATCH_THEMES = [
    'cerulean', 'flatly', 'lumen', 'sandstone', 'spacelab', 'yeti', 'cosmo',
    'darkly', 'paper', 'simplex', 'superhero', 'readable', 'slate', 'united'
]

BOOTSWATCH_THEME_DEFAULT = "simplex"
# 'cyborg' , 'journal'
