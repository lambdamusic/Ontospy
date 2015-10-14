#!/usr/bin/env python
# encoding: utf-8



from .util import *


def ontologyHtmlTree(graph, element = None):
	""" 
	Builds an html tree representation 

	NOTE: Copy and modify this function if you need some different type of html..

	EG:

	<ul id="example" class="filetree">
			<li><span class="folder">Folder 2</span>
					<ul>
							<li><span class="folder">Subfolder 2.1</span>
									<ul>
											<li><span class="file">File 2.1.1</span></li>
											<li><span class="file">File 2.1.2</span></li>
									</ul>
							</li>
							<li><span class="file">File 2.2</span></li>
					</ul>
			</li>
			<li class="closed"><span class="folder">Folder 3 (closed at start)</span></li>
			<li><span class="file">File 4</span></li>
	</ul>

	"""
	if not element:
		children = graph.toplayer
	else:
		children = element.children()
	stringa = "<ul>"
	for x in children:
		# print x
		stringa += "<li>%s" % uri2niceString(x.uri, graph.namespaces)
		stringa += ontologyHtmlTree(graph, x)
		stringa += "</li>"
	stringa += "</ul>"
	return stringa


