# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# TEST TEST TEST TEST TES
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

        if TEST_ONLINE:
            from ..core.ontospy import Ontospy
            g = Ontospy("http://cohere.open.ac.uk/ontology/cohere.owl#")
        else:
            uri, g = get_random_ontology(50)

        v = HTMLVisualizer(g)
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
