
import webbrowser
import rdflib	 # so we have it available as a namespace

from .. import ontospy 
from ..libs import util
from ..libs import vizutils


g = ontospy.Graph(ontospy.ONTOSPY_LOCAL_MODELS + "/foaf.rdf")


contents = vizutils.ontologyHtmlTree(g)

filename = ontospy.ONTOSPY_LOCAL_VIZ + "/test.html"

f = open(filename,'w')
f.write(contents) # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call it


webbrowser.open("file:///" + filename)