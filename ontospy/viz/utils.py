# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import main
import json




# ===========
# Utilities
# ===========



def build_D3treeStandard(old, MAX_DEPTH, level=1, toplayer=None):
	"""
	  For d3s examples all we need is a json with name, children and size .. eg

	  {
	 "name": "flare",
	 "children": [
	  {
	   "name": "analytics",
	   "children": [
		{
		 "name": "cluster",
		 "children": [
		  {"name": "AgglomerativeCluster", "size": 3938},
		  {"name": "CommunityStructure", "size": 3812},
		  {"name": "HierarchicalCluster", "size": 6714},
		  {"name": "MergeEdge", "size": 743}
		 ]
		},
		etc...
	"""
	out = []
	if not old:
		old = toplayer
	for x in old:
		d = {}
		# print "*" * level, x.label
		d['qname'] = x.qname
		d['name'] = x.bestLabel(quotes=False).replace("_", " ")
		d['objid'] = x.id
		if x.children() and level < MAX_DEPTH:
			d['size'] = len(x.children()) + 5	 # fake size
			d['realsize'] = len(x.children())        # real size
			d['children'] = build_D3treeStandard(x.children(), MAX_DEPTH, level+1)
		else:
			d['size'] = 1	 # default size
			d['realsize'] = 0	 # default size
		out += [d]


	return out




# note: duplicate of templatetagg so to avoid circular imports
def truncchar_inverse(value, arg):
	if len(value) < arg:
		return value
	else:
		x = len(value) - arg
		return '...' + value[x:]



##################
#
#  TREE DISPLAY FUNCTIONS [from ontospy web]
#
##################


def formatHTML_EntityTreeTable(treedict, element=0):
	""" outputs an html tree representation based on the dictionary we get from the Inspector
	object....

	EG:
	<table class=h>

		<tr>
		  <td class="tc" colspan=4><a href="../DataType">DataType</a>
		  </td>
		</tr>
		<tr>
		  <td class="tc" colspan=4><a href="../DataType">DataType</a>
		  </td>
		</tr>

		<tr>
		  <td class="space"></td>
		  <td class="bar"></td>
		  <td class="space"></td>

		  <td>
			<table class=h>
			   <tr><td class="tc" colspan=4><a href="../Boolean">Boolean</a>
					</td>
			   </tr>
			   <tr><td class="tc" colspan=4><a href="../Boolean">Boolean</a>
					</td>
			   </tr>
		   </table>
		  </td>


		 </tr>
	 </table>


	Note: The top level owl:Thing never appears as a link.

	"""
	# ontoFile = onto.ontologyMaskedLocation or onto.ontologyPhysicalLocation
	# if not treedict:
	# 	treedict = onto.ontologyClassTree()
	stringa = """<table class="h">"""
	for x in treedict[element]:
		if x.qname == "owl:Thing":
			stringa += """<tr>
							<td class="tc" colspan=4><a>%s</a></td>
						  </tr>""" % (truncchar_inverse(x.qname, 50))
		else:
			stringa += """<tr>
							<td class="tc" colspan=4><a title=\"%s\" class=\"treelinks\" href=\"%s.html\">%s</a></td>
						  </tr>""" % (x.uri, x.slug,
									  truncchar_inverse(x.qname, 50))

		if treedict.get(x, None):
			stringa += """ <tr>
							<td class="space"></td>
							<td class="bar"></td>
							<td class="space"></td>
							<td>%s</td>
							</tr>""" % formatHTML_EntityTreeTable(treedict, x)

		# stringa += formatHTML_ClassTree(onto, treedict, x)
		# stringa += "</li>"
	stringa += "</table>"
	return stringa
