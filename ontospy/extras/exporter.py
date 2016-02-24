
import time, optparse, sys, webbrowser

from .. import ontospy 
from ..core.util import *
import render

MODULE_VERSION = 0.2
USAGE = "exporter [graph-uri-or-location] [options]"

# 2016-02-04: launched with 'ontospy -e'



# manually edited
RENDER_OPTIONS = [
	(1, "Plain HTML (W3C docs style)"), 
	(2, "Interactive javascript tree (D3 powered)"), 
]





def _askVisualization():
	"""
	ask user which viz output to use
	"""
	while True:
		text = "Please select an output format: (q=quit)\n"
		for viz in RENDER_OPTIONS:
			text += "%d) %s\n" % (viz[0], viz[1])
		var = raw_input(text + "> ")
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
	
	url = "file:///" + filename
	return url 
	



def saveVizGithub(contents, ontouri):
	title = "Ontology documentation"
	readme = """This ontology documentation was automatically generated with OntoSPy (https://github.com/lambdamusic/OntoSPy).
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

Copyright (c) 2016 OntoSPy project [http://ontospy.readthedocs.org/]

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






def generateViz(graph, visualization):
	""" 
	<visualization>: an integer mapped to the elements of RENDER_OPTIONS
	"""
	
	if visualization == 1:
		contents = render.htmlBasicTemplate(graph)

	elif visualization == 2:
		contents = render.interactiveD3Tree(graph)	
				
	return contents
	



	
# def main():
# 	""" command line script """
# 	eTime = time.time()
# 	print "OntoSPy " + ontospy.VERSION
	
# 	ontospy.get_or_create_home_repo() 	
# 	opts, args = parse_options()
					
# 	# select from local ontologies:
# 	if opts.lib:
# 		ontouri = ontospy.actionSelectFromLocal()
# 		if ontouri:	
# 			islocal = True		
# 		else:	
# 			raise SystemExit, 1
# 	else:
# 		ontouri = args[0]
# 		islocal = False

	
# 	# select a visualization
# 	viztype = _askVisualization()
# 	if not viztype:
# 		raise SystemExit, 1
	
	
# 	# get ontospy graph
# 	if islocal:
# 		g = ontospy.get_pickled_ontology(ontouri)
# 		if not g:
# 			g = ontospy.do_pickle_ontology(ontouri)	
# 	else:
# 		g = ontospy.Graph(ontouri)
	
	
# 	# viz DISPATCHER
# 	if viztype == 1:
# 		contents = render.htmlBasicTemplate(g, opts.gist)

# 	elif viztype == 2:
# 		contents = render.interactiveD3Tree(g, opts.gist)	
				

	
# 	# once viz contents are generated, save file locally or on github
# 	if opts.gist:
# 		urls = saveVizGithub(contents, ontouri)
# 		printDebug("Documentation saved on github", "comment")
# 		printDebug("Gist: " + urls['gist'], "important")
# 		printDebug("Blocks Gist: " + urls['blocks'], "important")
# 		printDebug("Full Screen Blocks Gist: " + urls['blocks_fullwin'], "important")
# 		# url = saveVizGithub(contents)['blocks_fullwin'] # defaults to full win
# 		url = urls['blocks_fullwin'] # defaults to full win
# 	else:
# 		url = saveVizLocally(contents)
# 		printDebug("Documentation generated", "comment")

# 	# open browser	
# 	webbrowser.open(url)

# 	# finally: print some stats.... 
# 	sTime = time.time()					
# 	tTime = eTime - sTime
# 	printDebug("Time:	   %0.2fs" %  tTime, "comment")


