# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# VIZ MODULE : util to visualize an ontology as html or similar
#
#



from .. import ontospy
from ..core.util import *


# django loading requires different steps based on version
# https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
import django
if django.get_version() > '1.7':
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()
	django.setup()
	settings.TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [
	            # insert your TEMPLATE_DIRS here
	            ontospy.ONTOSPY_VIZ_TEMPLATES + "shared",
	        ],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
	                # list if you haven't customized them:
	                'django.contrib.auth.context_processors.auth',
	                'django.template.context_processors.debug',
	                'django.template.context_processors.i18n',
	                'django.template.context_processors.media',
	                'django.template.context_processors.static',
	                'django.template.context_processors.tz',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]

else:
	from django.conf import settings
	from django.template import Context, Template
	settings.configure()







# @todo modify when new viz are created

RENDER_OPTIONS = [
	(1, "JavaDoc (static)"),
	(2, "Dendogram (interactive)"),
]



def run_viz(g, viztype, save_gist):
    """
    Main fun calling the visualizations

    :param g: graph instance
    :param viztype: a number passed from the user
    :param save_gist: a flag (just to extra info printed on template)
    :return: string contents of html file (the viz)
    """
    # @todo modify when new viz are created
    from . import viz_d3tree
    from . import viz_html

    if viztype == 1:
        contents = viz_html.main(g, save_gist)

    elif viztype == 2:
        contents = viz_d3tree.main(g, save_gist)

    return contents







def ask_visualization():
	"""
	ask user which viz output to use
	"""
	while True:
		text = "Please select an output format for the ontology visualization: (q=quit)\n"
		for viz in RENDER_OPTIONS:
			text += "%d) %s\n" % (viz[0], viz[1])
		var = raw_input(text + ">")
		if var == "q":
			return None
		else:
			try:
				n = int(var)
				test = RENDER_OPTIONS[n-1]  #throw exception if number wrong
				return n
			except:
				printDebug("Invalid selection. Please try again.", "important")
				continue



def saveVizLocally(contents, filename = "index.html"):
	filename = ontospy.ONTOSPY_LOCAL_VIZ + "/" + filename

	f = open(filename,'w')
	f.write(contents) # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call it

	url = "file://" + filename
	return url




def saveVizGithub(contents, ontouri):
	title = "OntoSpy: ontology export"
	readme = """This ontology documentation was automatically generated with OntoSpy (https://github.com/lambdamusic/OntoSpy).
	The graph URI is: %s""" % str(ontouri)
	files = {
	    'index.html' : {
	        'content': contents
	        },
	    'README.txt' : {
	        'content': readme
	        },
	    'LICENSE.txt' : {
	        'content': """The MIT License (MIT)

Copyright (c) 2016 OntoSpy project [http://ontospy.readthedocs.org/]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
	        }
	    }
	urls = save_anonymous_gist(title, files)
	return urls



