
import time, optparse, os, sys, webbrowser
import rdflib	 # so we have it available as a namespace

from .. import ontospy 
from ..libs.util import *
from ..libs import render

MODULE_VERSION = 0.1
USAGE = "ontospy-doc <uri>"



def generateViz(location):
	
	# g = ontospy.Graph(ontospy.ONTOSPY_LOCAL_MODELS + "/foaf.rdf")
	g = ontospy.Graph(location)

	# contents = render.ontologyHtmlTree(g)
	contents = render.djangoTemplate(g)

	filename = ontospy.ONTOSPY_LOCAL_VIZ + "/test.html"

	f = open(filename,'w')
	f.write(contents) # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call it


	webbrowser.open("file:///" + filename)







def parse_options():
	"""
	parse_options() -> opts, args

	Parse any command-line options given returning both
	the parsed options and arguments.
	
	https://docs.python.org/2/library/optparse.html
	
	"""
	
	parser = optparse.OptionParser(usage=USAGE, version=ontospy.VERSION)

	# parser.add_option("-a", "--all",
	# 		action="store_true", default=False, dest="all",
	# 		help="Show all entries found by querying http://prefix.cc/popular/all.")
	#
	# parser.add_option("-q", "",
	# 		action="store", type="string", default="", dest="query",
	# 		help="A query string used to match the catalog entries.")
			
	opts, args = parser.parse_args()

	if not args:
		parser.print_help()
		sys.exit(0)

	return opts, args



	
def main():
	""" command line script """
	eTime = time.time()
	print "OntoSPy " + ontospy.VERSION
	
	ontospy.get_or_create_home_repo() 
	
	opts, args = parse_options()
					
					
	generateViz(args[0])
	
	sTime = time.time()
				
	# finally:	
	# print some stats.... 
	tTime = eTime - sTime
	printDebug("Time:	   %0.2fs" %  tTime, "comment")




				
	
if __name__ == '__main__':
	
	# from .. import ontospy
	try:
		main()
		sys.exit(0)
	except KeyboardInterrupt, e: # Ctrl-C
		raise e
