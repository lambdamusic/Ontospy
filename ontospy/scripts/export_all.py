# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Script to generate docs for all models in the local library. Using the Complex-html template.

> python -m ontospy.scripts.export_all -o ~/Desktop/test/ --theme random


"""

import os
import click, sys
# http://click.pocoo.org/5/arguments/
# http://click.pocoo.org/5/options/
from .. import *
from ..core import actions
from ..core.manager import get_home_location, get_localontologies
from ..core.utils import *  

from ..gendocs.viz.viz_html_multi import KompleteViz, KompleteVizMultiModel
from ..gendocs.actions import random_theme
from ..gendocs.CONFIG import BOOTSWATCH_THEME_DEFAULT
import webbrowser

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--inputpath', '-i', help='Input path (default: ontospy home folder).')
@click.option('--outputpath', '-o', help='Output path (default: ~/ontospy-viz-multi).')
@click.option(
    '--theme',
    help=
    'CSS Theme for the html-complex visualization (random=use a random theme).'
)
@click.option('--verbose', is_flag=True, help='Verbose mode.')
@click.pass_context
def cli_run_viz(ctx, inputpath="", outputpath="", theme="", verbose=False):
    """
This application is a wrapper on the main ontospy-gendocs utility. It generates docs for all models in the local library. Using the Complex-html template..

> python -m ontospy.scripts.scripts.export_all -o ~/Desktop/ontodocs/ -o ~/Desktop/ontodocs/ --theme random

"""

    printDebug("Ontospy " + VERSION, "comment")
    if not inputpath and not outputpath and not theme:
        printDebug(ctx.get_help())
        return 

    if outputpath:
        if not (os.path.exists(outputpath)) or not (os.path.isdir(outputpath)):
            click.secho(
                "WARNING: the -o option must include a valid directory path.",
                fg="red")
            sys.exit(0)
    else:
        from os.path import expanduser
        home = expanduser("~")
        outputpath = os.path.join(home, "ontospy-viz-multi")
        printDebug(f"Using default output path: {outputpath}", dim=True)

    if inputpath:
        source_folder = inputpath
        if not os.path.isdir(source_folder):
            click.secho(
                "WARNING: '%s' is not a valid directory path." % source_folder,
                fg="red")
            sys.exit(0)

        files_list = [
            f for f in os.listdir(source_folder)
            if os.path.isfile(os.path.join(source_folder, f))
        ]
        click.secho(
            "Exporting the directory: '%s'" % source_folder, fg="green")
        click.secho("----------", fg="green")

    else:
        click.secho(
            "Exporting the local library: '%s'" % get_home_location(),
            fg="green")
        click.secho("----------", fg="green")
        files_list = get_localontologies()
        source_folder = get_home_location()

    report_pages = []

    for onto_name in sorted(files_list):

        full_uri = os.path.join(source_folder, onto_name)
        if theme:
            if theme == "random":
                _theme = random_theme()
            else:
                _theme = theme
        else:
            _theme = BOOTSWATCH_THEME_DEFAULT
        click.secho("Onto: <%s> Theme: '%s'" % (onto_name, _theme), fg="red")

        printDebug("Loading graph...", dim=True)
        g = Ontospy(os.path.join(source_folder, onto_name), verbose=verbose)
        if g.sources:
            # if Ontospy graph has no valid 'sources' = file passed was not valid RDF
            printDebug("Building visualization...", dim=True)
            onto_name_safe = slugify(unicode(onto_name))
            onto_outputpath = os.path.join(outputpath, onto_name_safe)
            # note: single static files output path
            static_outputpath = os.path.join(outputpath, "static")
            # v = KompleteViz(g, theme=_theme)
            v = KompleteVizMultiModel(
                g,
                theme=_theme,
                static_url="../static/",
                output_path_static=static_outputpath)
            try:
                # note: onto_outputpath is wiped out each time as part of the build
                url = v.build(onto_outputpath)
                report_pages.append(
                    "<li><a href='%s/index.html' target='_blank'>%s</a> ('%s' theme)</li>"
                    % (onto_name_safe, onto_name, _theme))
            except:
                e = sys.exc_info()[0]
                printDebug("Error: " + str(e), "red")
                continue

    # generate a report page
    report_path = os.path.join(outputpath, "index.html")
    html = """
<html>
<head>
  <style media="screen">
    body {margin: 40px 10px 100px 50px;}
    li a {font-size: 20px; font- text-transform: lowercase; text-decoration: none; font-family: monospace;}
    li a:hover {text-decoration: underline;}
  </style>
</head>
<body>
<h1>Examples of ontology documentation generated with <a href="https://github.com/lambdamusic/ontospy" target="_blank">Ontospy</a></h1>
<p>Source code on <a href="https://github.com/lambdamusic/ontospy-examples">GitHub</a></p>
<hr>
<ol>
%s
</ol>
</body>
</html>
    """
    with open(report_path, "w") as text_file:
        text_file.write(html % ("".join([x for x in report_pages])))
    # open report
    webbrowser.open("file:///" + report_path)

    raise SystemExit(1)


if __name__ == '__main__':
    try:
        # http://stackoverflow.com/questions/32553969/modify-usage-string-on-click-command-line-interface-on-windows
        cli_run_viz(prog_name='ontospy-viz')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
