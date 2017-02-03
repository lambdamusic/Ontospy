# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import *
import json

from .utils import build_D3treeStandard


# TEMPLATE: SIGMA JS

#
# ===========
# Comments:
# ===========
#






def run(graph, save_on_github=False, main_entity=None):
    """
    2016-11-30
    """

    try:
        ontology = graph.ontologies[0]
        uri = ontology.uri
    except:
        ontology = None
        uri = ";".join([s for s in graph.sources])

    # ontotemplate = open("template.html", "r")
    ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "sigmajs.html", "r")

    t = Template(ontotemplate.read())

    dict_graph = build_class_json(graph.classes)
    JSON_DATA_CLASSES = json.dumps(dict_graph)

    if False:
        c_mylist = build_D3treeStandard(0, 99, 1, graph.toplayer)
        p_mylist = build_D3treeStandard(0, 99, 1, graph.toplayerProperties)
        s_mylist = build_D3treeStandard(0, 99, 1, graph.toplayerSkosConcepts)
    
        c_total = len(graph.classes)
        p_total = len(graph.properties)
        s_total = len(graph.skosConcepts)
    
        # hack to make sure that we have a default top level object
        JSON_DATA_CLASSES = json.dumps({'children' : c_mylist, 'name' : 'owl:Thing', 'id' : "None" })
        JSON_DATA_PROPERTIES = json.dumps({'children' : p_mylist, 'name' : 'Properties', 'id' : "None" })
        JSON_DATA_CONCEPTS = json.dumps({'children' : s_mylist, 'name' : 'Concepts', 'id' : "None" })
    

    c = Context({
                    "ontology": ontology,
                    "main_uri" : uri,
                    "STATIC_PATH": ONTOSPY_VIZ_STATIC,
                    "classes": graph.classes,
                    "classes_TOPLAYER": len(graph.toplayer),
                    "properties": graph.properties,
                    "properties_TOPLAYER": len(graph.toplayerProperties),
                    "skosConcepts": graph.skosConcepts,
                    "skosConcepts_TOPLAYER": len(graph.toplayerSkosConcepts),
                    # "TOTAL_CLASSES": c_total,
                    # "TOTAL_PROPERTIES": p_total,
                    # "TOTAL_CONCEPTS": s_total,
                    'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
                    # 'JSON_DATA_PROPERTIES' : JSON_DATA_PROPERTIES,
                    # 'JSON_DATA_CONCEPTS' : JSON_DATA_CONCEPTS,
                })

    rnd = t.render(c)

    return safe_str(rnd)



import random

def _classColor(x):
    if not x.parents():
        return "#FFD8DD"
    elif not x.children():
        return "#C4F5FF"
    else:
        return "#C8FFB3"
    
def build_class_json(classes):
    nodes = [{
                    "id": "owlthing",
                    "label": "owl:Thing",
                    "x": random.random(),
                    "y": random.random(),
                    "color" : "grey",
                    "size": 5
                }]
    edges = []
    for x in classes:
        temp = {
                    "id": x.id,
                    "label": x.bestLabel(quotes=False),
                    "x": random.random(),
                    "y": random.random(),
                    "color" : _classColor(x),
                    "size": len(x.descendants()) or 1
                }
        nodes.append(temp)
        
        if not x.parents():
            # add a relationship to OWL THING
            edges.append({
                "id": "%s-%s" % (x.id, "owlthing"),
                "source": "owlthing",
                "target": x.id,
                "color": '#ccc',
                "hover_color": '#000'
            })
        
        for el in x.children():
            temp2 = {
                "id": "%s-%s" % (x.id, el.id),
                "source": x.id,
                "target": el.id,
                 # "type": 'curve',
                "color": '#ccc',
                "hover_color": '#000'
            }
            edges.append(temp2)
    
    result = {
            "nodes": nodes ,
            "edges" : edges,
        }
    
    return result



if __name__ == '__main__':
    import sys
    try:

        # script for testing - must launch this module
        # >python -m viz.viz_d3tree
        
        TEST_PATH = "/Users/michele.pasin/Desktop/temp/"
        # if False:
        from .builder import _copyStaticFiles
        print("..copying")
        # note: this is just a hack.. all sigma files should be in subdir
        # hence _copyStaticFiles should dbe updated so to handle that
        _copyStaticFiles(["sigma.min.js", "sigma.layout.forceAtlas2.min.js"], TEST_PATH+"static", folder="")
        
        func = locals()["run"] # main func dynamically
        run_test_viz(func, filename="sigma.html", path=TEST_PATH)

        sys.exit(0)

    except KeyboardInterrupt as e: # Ctrl-C
        raise e



