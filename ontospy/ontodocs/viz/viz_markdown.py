# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# ==================
# VIZ MARKDOWN - multiple file, markdown format
# ==================

import os, sys
import json

from ..utils import *
from ..builder import *  # loads and sets up Django
from ..viz_factory import VizFactory


class MarkdownViz(VizFactory):
    """
    A simple markdown rendering, using multiple pages

    """

    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(MarkdownViz, self).__init__(ontospy_graph, title)

    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """

        # Ontology - MAIN PAGE
        contents = self._renderTemplate(
            "markdown/markdown_ontoinfo.md", extraContext=None)
        FILE_NAME = "index.md"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        browser_output_path = self.output_path

        if self.ontospy_graph.all_classes:

        # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.all_classes:
                extra_context = {
                    "main_entity": entity,
                    "main_entity_type": "class",
                    "ontograph": self.ontospy_graph
                }
                contents = self._renderTemplate(
                    "markdown/markdown_classinfo.md",
                    extraContext=extra_context)
                FILE_NAME = entity.slug + ".md"
                self._save2File(contents, FILE_NAME, browser_output_path)

        if self.ontospy_graph.all_properties:

        # BROWSER PAGES - PROPERTIES ======
            for entity in self.ontospy_graph.all_properties:
                extra_context = {
                    "main_entity": entity,
                    "main_entity_type": "property",
                    "ontograph": self.ontospy_graph
                }
                contents = self._renderTemplate(
                    "markdown/markdown_propinfo.md",
                    extraContext=extra_context)
                FILE_NAME = entity.slug + ".md"
                self._save2File(contents, FILE_NAME, browser_output_path)

        if self.ontospy_graph.all_skos_concepts:

        # BROWSER PAGES - CONCEPTS ======
            for entity in self.ontospy_graph.all_skos_concepts:
                extra_context = {
                    "main_entity": entity,
                    "main_entity_type": "concept",
                    "ontograph": self.ontospy_graph
                }
                contents = self._renderTemplate(
                    "markdown/markdown_conceptinfo.md",
                    extraContext=extra_context)
                FILE_NAME = entity.slug + ".ms"
                self._save2File(contents, FILE_NAME, browser_output_path)

        if self.ontospy_graph.all_individuals:

        # BROWSER PAGES - INDIVIDUALS ======
            for entity in self.ontospy_graph.all_individuals:
                extra_context = {
                    "main_entity": entity,
                    "main_entity_type": "individual",
                    "ontograph": self.ontospy_graph
                }
                contents = self._renderTemplate(
                    "markdown/markdown_individualinfo.md",
                    extraContext=extra_context)
                FILE_NAME = entity.slug + ".ms"
                self._save2File(contents, FILE_NAME, browser_output_path)

        return main_url


# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = MarkdownViz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
