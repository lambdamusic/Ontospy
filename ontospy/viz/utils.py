# !/usr/bin/env python
#  -*- coding: UTF-8 -*-

from . import *  # imports __init__
from .. import ontospy
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



