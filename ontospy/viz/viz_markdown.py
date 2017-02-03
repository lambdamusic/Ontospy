# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# VIZ MARKDOWN
#
#



from .. import *
from ..core.utils import *
from ..core.manager import *

from .utils import *
from .viz_factory import VizFactory

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

# django loading requires different steps based on version
# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django

# http://stackoverflow.com/questions/1714027/version-number-comparison
from distutils.version import StrictVersion

if StrictVersion(django.get_version()) > StrictVersion('1.7'):
    from django.conf import settings
    from django.template import Context, Template

else:
    from django.conf import settings
    from django.template import Context, Template


import os, sys



class MarkdownViz(VizFactory):
    """
    A simple markdown rendering in multi pages

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
        contents = self._renderTemplate("markdown/markdown_ontoinfo.md", extraContext=None)
        FILE_NAME = "index.md"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        browser_output_path = self.output_path

        if self.ontospy_graph.classes:

            # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.classes:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "class",
                                "ontograph": self.ontospy_graph
                                }
                contents = self._renderTemplate("markdown/markdown_classinfo.md", extraContext=extra_context)
                FILE_NAME = entity.slug + ".md"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.properties:

            # BROWSER PAGES - PROPERTIES ======
            for entity in self.ontospy_graph.properties:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "property",
                                "ontograph": self.ontospy_graph
                                }
                contents = self._renderTemplate("markdown/markdown_propinfo.md", extraContext=extra_context)
                FILE_NAME = entity.slug + ".md"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.skosConcepts:

            # BROWSER PAGES - CONCEPTS ======
            for entity in self.ontospy_graph.skosConcepts:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "concept",
                                "ontograph": self.ontospy_graph
                                }
                contents = self._renderTemplate("markdown/markdown_conceptinfo.md", extraContext=extra_context)
                FILE_NAME = entity.slug + ".ms"
                self._save2File(contents, FILE_NAME, browser_output_path)

        return main_url




# if called directly, for testing purposes run the basic HTML rendering

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        if TEST_ONLINE:
            from ..core.ontospy import Ontospy
            g = Ontospy("http://cohere.open.ac.uk/ontology/cohere.owl#")
        else:
            uri, g = get_random_ontology(50)

        v = MarkdownViz(g, title="")
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
