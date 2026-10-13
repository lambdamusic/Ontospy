# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Script to generate docs for all models in the local library. Using the Complex-html template.

> python -m ontospy.scripts.export_all -o ~/Desktop/test/ --theme random


"""

import os
import html
import datetime
import traceback
import click, sys
# http://click.pocoo.org/5/arguments/
# http://click.pocoo.org/5/options/
from .. import *
from ..core import actions
from ..core.manager import get_home_location, get_localontologies
from ..core.utils import *  

from ..gendocs.viz.viz_html_multi import KompleteViz, KompleteVizMultiModel
from ..gendocs.actions import random_theme, stable_theme
from ..gendocs.CONFIG import BOOTSWATCH_THEME_DEFAULT
import webbrowser

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--inputpath', '-i', help='Input path (default: ontospy home folder).')
@click.option('--outputpath', '-o', help='Output path (default: ~/ontospy-viz-multi).')
@click.option(
    '--theme',
    help=
    'CSS Theme for the html-complex visualization (random=use a random theme, stable=a theme picked from the file name, the same at every run).'
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
            if os.path.isfile(os.path.join(source_folder, f)) and not f.startswith(".")
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

    report_rows = []
    failed = []

    for onto_name in sorted(files_list, key=str.lower):

        full_uri = os.path.join(source_folder, onto_name)
        if theme:
            if theme == "random":
                _theme = random_theme()
            elif theme == "stable":
                _theme = stable_theme(onto_name)
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
                # the per-ontology folders belong to this script, so they're rebuilt from scratch
                url = v.build(onto_outputpath, empty_folder=True)
                report_rows.append(_index_row(g, onto_name, onto_name_safe, _theme))
            except Exception:
                printDebug("Error building <%s>:\n%s" % (onto_name, traceback.format_exc()), "red")
                failed.append(onto_name)
                continue
        else:
            failed.append(onto_name)

    # generate the index page
    report_path = os.path.join(outputpath, "index.html")
    with open(report_path, "w", encoding="utf-8") as text_file:
        text_file.write(_index_page(report_rows))
    if failed:
        printDebug("Failed: %s" % ", ".join(failed), "red")
    # open report
    webbrowser.open("file:///" + report_path)


# columns of the index table: (heading, Ontospy.stats() label)
INDEX_COUNTS = [("Classes", "Classes"), ("Properties", "Properties"),
                ("Concepts", "Skos Concepts"), ("Shapes", "Data Shapes")]


def _ontology_title_and_description(g):
    """title and description of the first ontology declared in the graph, if any"""
    for onto in g.all_ontologies:
        title = ""
        for pred in [rdflib.RDFS.label, rdflib.namespace.DCTERMS.title, rdflib.namespace.DC.title]:
            values = onto.getValuesForProperty(pred)
            if values:
                title = str(firstStringInList(values, "en"))
                break
        return title, str(onto.bestDescription(prefLanguage="en") or "")
    return "", ""


def _truncate(text, length=220):
    text = " ".join(text.split())
    if len(text) <= length:
        return text
    return text[:length].rsplit(" ", 1)[0] + "…"


def _index_row(g, onto_name, folder, theme):
    """a row of the index table (#8): the ontology's title, description and counts"""
    title, description = _ontology_title_and_description(g)
    stats = dict(g.stats())
    cells = "".join('<td class="count">%d</td>' % stats.get(label, 0) for _, label in INDEX_COUNTS)
    return """<tr>
  <td><a href="%s/index.html"><code>%s</code></a></td>
  <td>%s<div class="theme">theme: %s</div></td>
  %s
</tr>""" % (folder, html.escape(onto_name),
         "<br>".join(x for x in [
             "<b>%s</b>" % html.escape(_truncate(title, 100)) if title else "",
             html.escape(_truncate(description)) if description else ""] if x),
         html.escape(theme), cells)


def _index_page(rows):
    headings = "".join('<th class="count">%s</th>' % h for h, _ in INDEX_COUNTS)
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ontospy examples</title>
  <link href="static/libs/bootstrap-3_3_7-dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { margin: 40px 0 80px; }
    td.count, th.count { text-align: right; white-space: nowrap; }
    td .theme { color: #999; font-size: 85%%; margin-top: 4px; }
    td code { font-size: 100%%; white-space: nowrap; }
  </style>
</head>
<body>
<div class="container">
  <h1>Examples of ontology documentation generated with <a href="https://github.com/lambdamusic/ontospy">Ontospy</a></h1>
  <p>%d ontologies, documented with the <i>html-complex</i> visualization. Source files and code on <a href="https://github.com/lambdamusic/ontospy-examples">GitHub</a>.</p>
  <div class="table-responsive">
  <table class="table table-hover">
    <thead><tr><th>Ontology</th><th>Title and description</th>%s</tr></thead>
    <tbody>
%s
    </tbody>
  </table>
  </div>
  <hr>
  <p class="text-muted">Generated on %s with Ontospy %s.</p>
</div>
</body>
</html>
""" % (len(rows), headings, "\n".join(rows), datetime.date.today().isoformat(), VERSION)


if __name__ == '__main__':
    try:
        # http://stackoverflow.com/questions/32553969/modify-usage-string-on-click-command-line-interface-on-windows
        cli_run_viz(prog_name='ontospy-viz')
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
