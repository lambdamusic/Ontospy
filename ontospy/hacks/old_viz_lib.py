#!/usr/bin/env python
# encoding: utf-8



# TODO


def ontologyHtmlTree(self, element = 0, treedict = None):
	""" 
	Builds an html tree representation based on the internal tree-dictionary representation

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
	if not treedict:
		treedict = self.ontologyClassTree
	stringa = "<ul>"
	for x in treedict[element]:
		# print x
		stringa += "<li>%s" % uri2niceString(x, self.ontologyNamespaces)
		stringa += self.ontologyHtmlTree(x, treedict)
		stringa += "</li>"
	stringa += "</ul>"
	return stringa




def drawOntograph(self, fileposition):
	"""
	Visualize the graph using pyGraphViz (which needs to be preinstalled)

	More info on Layouts: http://rss.acs.unt.edu/Rdoc/library/Rgraphviz/html/GraphvizLayouts.html
	"""

	try:
		import pygraphviz as pgv
	except:
		return "You need to install pygraphviz for this operation."

	G = pgv.AGraph(rankdir="BT") # top bottom direction
	for s, v, o in self.rdfGraph.triples((None, RDFS.subClassOf , None)):
		G.add_edge(uri2niceString(s, self.ontologyNamespaces), uri2niceString(o, self.ontologyNamespaces))
	G.layout(prog='dot')	# eg dot, neato, twopi, circo, fdp
	G.draw(fileposition)
	print("\n\n", "_" * 50, "\n\n")
	print("Generated graph at %s" % fileposition)


def webViz(self):
	"""
		July 10, 2014
		Visualize the graph using d3  @todo
	"""

	try:
		import webbrowser
	except:
		return "You need the webbrowser module for this operation."

	filename = 'test.html'
	
	if False:		
		# the simeplest test ever
		f = open("test.html", "w")
		f.write("<html><body><h2>It WOrks</h2><p>%s</p></body></html>" % " ".join(["<li>"+str(x)+"</li>" for x in self.allclasses]))
		f.close()
		print("\n\n", "_" * 50, "\n\n")
		print("Generated graph at %s" % os.path.realpath(filename))
		webbrowser.open('file://'+os.path.realpath("test.html"))


		
		
	if False:
		# just opens a d3 file
		thisdir = os.path.dirname(os.path.realpath(__file__))		
		print thisdir
		webbrowser.open('file://'+thisdir+"/data/templates/forcedirected.html")
		
				
	if True:
		# uses a string template with d3
		from string import Template
		ss = ""		
		for x in self.allclasses:
			if self.classDirectSupers(x):
				for directSuper in self.classDirectSupers(x):
					ss += """{source: "%s", target: "%s", type: "test"},\n""" % (uri2niceString(x, self.ontologyNamespaces), uri2niceString(directSuper, self.ontologyNamespaces))
			else:
				ss += """{source: "%s", target: "ROOT", type: "test"},\n""" % (uri2niceString(x, self.ontologyNamespaces))		
		thisdir = os.path.dirname(os.path.realpath(__file__))
		
		#open the file
		filein = open(thisdir + '/data/templates/forceDirectedTemplate.html' )
		#read it
		src = Template( filein.read() )
		#do the substitution called $graphedges in html file

		from os.path import expanduser
		home = expanduser("~")
		location = home + "/ontospy-viz.html"
		
		
		fileout = open(location, "w")
		fileout.write(src.substitute({'graphedges' : ss}))
		fileout.close()
		# webbrowser.open('file://'+os.path.realpath("ontospy-viz.html"))
		webbrowser.open('file://'+location) # note: requires 2 forwards slashes + 1 for path



