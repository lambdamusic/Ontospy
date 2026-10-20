# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# ==================
# VIZ HTML MULTI - html visualization with multiple files, one per entity
# ==================
#
# The sidebar's list of entities is written once, in sidebar.js, and built in the browser
# (templates/html-multi/sidebar.html), rather than repeated in every page, which made the
# output grow with the square of the number of entities: 1.6 GB for Brick, 27 GB for
# FOVT (backlog #21). The same for the Usage tables of the class pages, in usage.js.

import os, sys
import json

from ..utils import *
from ..actions import *
from ..viz_factory import VizFactory
from ...core.utils import uri2niceString



def is_class_defined_as_shacl_node_shape(entity) -> bool:
    """This function identifies all RDFS or OWL Classes that define themselves as SHACL Node Shapes."""
    is_NodeShape = False
    is_Class = False

    # check if the entity is a NodeShape
    for triple in entity.rdflib_graph.triples((entity.uri, RDF.type, SH.NodeShape)): is_NodeShape = True
    if is_NodeShape == False:
        return False

    # check if the entity is a SHACL Class (i.e. an OWL Class or RDFS Class)
    for triple in entity.rdflib_graph.triples((entity.uri, RDF.type, OWL.Class)): is_Class = True
    if is_Class == False:
        for triple in entity.rdflib_graph.triples((entity.uri, RDF.type, RDFS.Class)): is_Class = True

    return (is_NodeShape and is_Class)


def sidebar_js(g):
    """The entities of the sidebar, as a script defining SIDEBAR: for each section a list
    of [id, title, page (without .html), qname], the qname left out when it's the title"""
    def entries(entities):
        out = []
        for e in entities:
            entry = [e.id, e.title, e.slug]
            if e.qname != e.title:
                entry.append(e.qname)
            out.append(entry)
        return out
    data = {
        "classes": entries(g.all_classes),
        "properties": entries(g.all_properties),
        "concepts": entries(g.all_skos_concepts),
        "individuals": entries(g.all_individuals),
    }
    # "</" escaped, in case the file is ever inlined in a <script>
    return ("var SIDEBAR = %s;\n" % json.dumps(data, ensure_ascii=False)).replace("</", "<\\/")


def usage_groups(c):
    """The ids of the classes whose properties make up the Usage table of class c, in
    order: c, its ancestors, then owl:Thing (properties with no domain); only those
    with properties"""
    return [k.id for group in c.domain_of_inferred for k, v in group.items() if v]


def usage_js(g):
    """The rows of the Usage tables of the class pages, as a script defining USAGE:

    {"groups": {class id: [title, qname, page (without .html), [property ids]]},
     "props": {property id: [title, qname, page, rdf type, description,
                             [[range page or None, title, qname], ...]]}}

    Written once, rather than a table on every class page that repeated the properties
    of the top classes: on FOVT 377 KB of a 400 KB page (backlog #21). A page names its
    groups (usage_groups) and builds the table in the browser (custom/js/usage.js)."""
    groups, props = {}, {}
    for c in g.all_classes:
        for group in c.domain_of_inferred:
            for k, v in group.items():
                if v and k.id not in groups:
                    groups[k.id] = [k.title, k.qname, k.slug, [p.id for p in v]]
                    for p in v:
                        if p.id not in props:
                            ranges = p.ranges or p.ranges_inferred
                            props[p.id] = [p.title, p.qname, p.slug, p.rdftype_qname,
                                           p.bestDescription() or "",
                                           [[None if r.ext_model else r.slug, r.title, r.qname]
                                            for r in ranges]]
    data = {"groups": groups, "props": props}
    return ("var USAGE = %s;\n" % json.dumps(data, ensure_ascii=False)).replace("</", "<\\/")



def statistics_charts(g):
    """For the statistics page: (key, label, bubble chart tree, pack tree) for each kind of
    entity the graph has, built as for the D3 vizs"""
    out = []
    for key, label, toplayer, root in [
            ("classes", "Classes", g.toplayer_classes, "owl:Thing"),
            ("properties", "Properties", g.toplayer_properties, "Properties"),
            ("concepts", "Concepts", g.toplayer_skos, "Concepts")]:
        if toplayer:
            out.append((key, label,
                {'children': build_D3bubbleChart(0, 99, 1, toplayer), 'name': root, 'id': "None"},
                {'children': build_D3treeStandard(0, 99, 1, toplayer), 'name': root, 'id': "None"}))
    return out


def entity_info(g, max_description=300):
    """For the drawer of the statistics page, the basics of each entity, by kind and id:
    [title, qname, page (without .html), description (shortened), [parent ids], number of
    children], and for properties also [domains] and [ranges], each as [id or None, name]"""
    def short(text):
        text = " ".join((text or "").split())
        if len(text) > max_description:
            text = text[:max_description].rsplit(" ", 1)[0] + "…"
        return text

    def named(entities):
        # an entity of the graph, or a URI outside it (eg xsd:string)
        return [[e.id, e.title] if hasattr(e, "id") else [None, uri2niceString(e, g.namespaces)]
                for e in entities]

    def info(e):
        return [e.title, e.qname, e.slug, short(e.bestDescription()),
                [p.id for p in e.parents()], len(e.children())]

    return {
        "classes": {c.id: info(c) for c in g.all_classes},
        "properties": {p.id: info(p) + [named(p.domains), named(p.ranges)] for p in g.all_properties},
        "concepts": {c.id: info(c) for c in g.all_skos_concepts},
    }

class KompleteViz(VizFactory):
    """

    """


    def __init__(self, ontospy_graph, title="", theme="", *args, non_redundant=False, **kwargs):
        """
        Init

        non_redundant: in the tree pages, leave out children that are also descendants
        of another child, eg for reasoned graphs (PR #87)
        """
        super(KompleteViz, self).__init__(ontospy_graph, title, *args, **kwargs)
        self.non_redundant = non_redundant
        self.theme = validate_theme(theme)
        # only the chosen Bootswatch theme, not all of them
        self.static_files = [
                "custom",
                "libs/bootswatch3_2/" + self.theme,
                "libs/bootswatch3_2/fonts",
                "libs/bootstrap-3_3_7-dist",
                "libs/jquery/1_12_4/",
                "libs/chartjs-2_4_0",
                "libs/d3-v7"
                ]

    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """
        # SIDEBAR - the entities, for all pages
        self._save2File(sidebar_js(self.ontospy_graph).encode("utf-8"), "sidebar.js", self.output_path)
        # USAGE - the properties of each class, for the Usage tables of the class pages
        self._save2File(usage_js(self.ontospy_graph).encode("utf-8"), "usage.js", self.output_path)

        # INDEX - MAIN PAGE
        contents = self._renderTemplate("html-multi/index.html", extraContext={"theme": self.theme, "index_page_flag" : True})
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        # DASHBOARD - with the hierarchy and the density of the classes, properties and
        # concepts, drawn as in the D3 vizs (shared/js_d3_charts.html)
        extra_context = {"theme": self.theme}
        charts = statistics_charts(self.ontospy_graph)
        if charts:
            # "</" escaped, since it goes in a <script>
            extra_context["CHARTS"] = [(key, label) for key, label, _, _ in charts]
            extra_context["CHARTS_DATA"] = json.dumps(
                {key: {"bubble": bubble, "pack": pack} for key, _, bubble, pack in charts},
                ensure_ascii=False).replace("</", "<\\/")
            extra_context["ENTITY_INFO"] = json.dumps(
                entity_info(self.ontospy_graph), ensure_ascii=False).replace("</", "<\\/")
        contents = self._renderTemplate("html-multi/statistics.html", extraContext=extra_context)
        FILE_NAME = "statistics.html"
        self._save2File(contents, FILE_NAME, self.output_path)

        browser_output_path = self.output_path

        # ENTITIES A-Z
        extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme}
        contents = self._renderTemplate("html-multi/browser/browser_entities_az.html", extraContext=extra_context)
        FILE_NAME = "entities-az.html"
        self._save2File(contents, FILE_NAME, browser_output_path)



        if self.ontospy_graph.all_classes:

            # CLASSES = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "classes",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyClassTree(self.non_redundant))}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-classes.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - CLASSES ======

            for entity in self.ontospy_graph.all_classes:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "class",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph,
                                "usage_groups": usage_groups(entity)
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_classinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.all_properties:

            # PROPERTIES = ENTITIES TREE
            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "properties",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyPropTree(self.non_redundant))}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-properties.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - PROPERTIES ======

            for entity in self.ontospy_graph.all_properties:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "property",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_propinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.all_skos_concepts:

            # CONCEPTS = ENTITIES TREE

            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "concepts",
                'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyConceptTree(self.non_redundant))}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-concepts.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - CONCEPTS ======

            for entity in self.ontospy_graph.all_skos_concepts:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "concept",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_conceptinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.all_shapes:

            # SHAPES = ENTITIES TREE

            extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme,
                            "treetype" : "shapes", 'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyShapeTree(self.non_redundant)) }
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-shapes.html"
            self._save2File(contents, FILE_NAME, browser_output_path)

            # BROWSER PAGES - SHAPES ======

            for entity in self.ontospy_graph.all_shapes:

                # Check entities if they are SHACL NodeShapes and OWL Classes
                if is_class_defined_as_shacl_node_shape(entity):
                    # locate the class, and replace the parents/children for the tree-diagram
                    for c in self.ontospy_graph.all_classes:
                        if c.uri == entity.uri:
                            entity.parents = c.parents
                            entity.children = c.children

                extra_context = {"main_entity": entity,
                                "main_entity_type": "shape",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_shapeinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)



        if self.ontospy_graph.all_individuals:

            # INDIVIDUALS (FLAT) TREE

            extra_context = {
                    "ontograph": self.ontospy_graph, 
                    "theme": self.theme,
                    "treetype" : "individuals",
                    'treeTable' : formatHTML_EntityTreeTable(self.ontospy_graph.ontologyIndividualsTree())}
            contents = self._renderTemplate("html-multi/browser/browser_entities_tree.html", extraContext=extra_context)
            FILE_NAME = "entities-tree-individuals.html"
            self._save2File(contents, FILE_NAME, browser_output_path)
            
            # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.all_individuals:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "individual",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate(
                        "html-multi/browser/browser_individualinfo.html",
                        extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        return main_url




class KompleteVizMultiModel(KompleteViz):
    """
    Specialized version that supports customizing where the static url / folder are.

    The idea is to pass a location which can be shared by multiple html outputs. (eg multiple html-complex ontology folders)

    eg

    python -m ontospy.viz.scripts.export_all -o ~/Desktop/test2/ --theme random
    """


    def __init__(self, ontospy_graph, title="", theme="", static_url="", output_path_static="", **kwargs):
        """
        Init
        """
        super(KompleteVizMultiModel, self).__init__(ontospy_graph, title, theme, **kwargs)
        self.static_files = ["custom", "libs"]
        self.theme = validate_theme(theme)
        self.static_url = static_url  # eg "../static"
        self.output_path_static = output_path_static  # eg full path to a top level
        # note: the following serves to make sure self.static_url is passed correctly
        self.basic_context_data = self._build_basic_context()






# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = KompleteViz(g, title="", theme=random_theme())
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
