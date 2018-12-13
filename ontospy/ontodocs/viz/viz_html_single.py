# !/usr/bin/env python
#  -*- coding: UTF-8 -*-



# ==================
# VIZ HTML SINGLE - outputs documentation within a single HTML page
# ==================


import os, sys

from ..core import *
from ..core.utils import *
from ..core.builder import *  # loads and sets up Django
from ..core.viz_factory import VizFactory



class HTMLVisualizer(VizFactory):
    """
    A simple html rendering in one single page

    """


    def __init__(self, ontospy_graph, title=""):
        """
        Init
        """
        super(HTMLVisualizer, self).__init__(ontospy_graph, title)
        self.template_name = "html-single/html-single.html"
        self.main_file_name = "index.html"




# if called directly, for testing purposes run the basic HTML rendering

if __name__ == '__main__':

    TEST_ONLINE = False

    try:

        g = get_onto_for_testing(TEST_ONLINE) # from core.utils

        v = HTMLVisualizer(g)
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
