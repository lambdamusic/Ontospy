# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


# ===========
# Utilities for Vizualisations
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
        # d['name'] = x.bestLabel(quotes=False).replace("_", " ")
        d['name'] = x.title
        d['objid'] = x.id
        if x.children() and level < MAX_DEPTH:
            d['size'] = len(x.children()) + 5  # fake size
            d['realsize'] = len(x.children())  # real size
            d['children'] = build_D3treeStandard(x.children(), MAX_DEPTH,
                                                 level + 1)
        else:
            d['size'] = 1  # default size
            d['realsize'] = 0  # default size
        out += [d]

    return out


# note: duplicate of templatetagg so to avoid circular imports
def truncchar_inverse(value, arg):
    if len(value) < arg:
        return value
    else:
        x = len(value) - arg
        return '...' + value[x:]


def build_D3bubbleChart(old, MAX_DEPTH, level=1, toplayer=None, _seen=None):
    """
	  Similar to standar d3, but nodes with children need to be duplicated otherwise they are
	   not depicted explicitly but just color coded

	"name": "all",
	"children": [
		{"name": "Biological Science", "size": 9000},
		 {"name": "Biological Science", "children": [
			 {"name": "Biological techniques", "size": 6939},
			{"name": "Cell biology", "size": 4166},
			{"name": "Drug discovery X", "size": 3620, "children": [
				{"name": "Biochemistry X", "size": 4585},
				{"name": "Biochemistry X", "size": 4585 },
			]},
			{"name": "Drug discovery Y", "size": 3620, "children": [
				{"name": "Biochemistry Y", "size": 4585},
				{"name": "Biochemistry Y", "size": 4585 },
			]},
			{"name": "Drug discovery A", "size": 3620, "children": [
				{"name": "Biochemistry A", "size": 4585},
			]},
			{"name": "Drug discovery B", "size": 3620, },
		 ]},
		etc...

	Each entity appears once, under the first parent the walk reaches it from: the chart
	shows density, so an entity with several parents (and its subtree) isn't repeated
	under each of them, which on FOVT made 288k bubbles for 12k classes (backlog #21).
	"""
    out = []
    if _seen is None:
        _seen = set()
    if not old:
        old = toplayer
    for x in old:
        if x.id in _seen:
            continue
        _seen.add(x.id)
        d = {}
        # print "*" * level, x.label
        d['qname'] = x.qname
        # d['name'] = x.bestLabel(quotes=False).replace("_", " ")
        d['name'] = x.title
        d['objid'] = x.id
        if x.children() and level < MAX_DEPTH:
            duplicate_row = {}
            duplicate_row['qname'] = x.qname
            # the same label as everywhere else, so that --preflabel/--preflang apply (#32)
            duplicate_row['name'] = x.title
            duplicate_row['objid'] = x.id
            duplicate_row['size'] = len(x.children()) + 5  # fake size
            duplicate_row['realsize'] = len(x.children())  # real size
            out += [duplicate_row]
            d['children'] = build_D3bubbleChart(x.children(), MAX_DEPTH,
                                                level + 1, _seen=_seen)
        else:
            d['size'] = 1  # default size
            d['realsize'] = 0  # default size
        out += [d]

    return out


def build_D3panelData(g):
    """
    The data the side panel of the D3 visualizations uses to build a class's Usage table
    (the properties its instances can have, its own and its superclasses'), in JavaScript
    when the panel opens (#26). Written once per page rather than as a table per class,
    which would repeat the properties of the top classes for every class: on schema.org
    that took a page from 3 to 14 MB.

    {"classes": {id: [title, [ancestor ids], [own property ids]]},
     "props": {id: [title, qname, [[range id or None, range title], ...]]},
     "thing": [ids of the properties with no domain, which apply to every class],
     "shapes": {id: [headers of the class's groups of SHACL constraints]},
     "shape_groups": {header: [[property id or None, property qname, min, max,
                                [[value type id or None, qname], ...]], ...]}}

    The SHACL constraints of a class include those of its superclasses, a group per class
    after a header naming it (shacl_helper.build_shacl_constraints), so each group is
    written once too.
    """
    thing = []
    for c in g.all_classes:
        for group in c.domain_of_inferred:
            for k, v in group.items():
                if k is g.OWLTHING:
                    thing = [p.id for p in v]
        if thing:
            break
    classes = {}
    for c in g.all_classes:
        if not c.domain_of_inferred:
            continue
        own = [p.id for p in c.domain_of + c.domain_of_via_superproperties]
        classes[c.id] = [c.title, [x.id for x in c.ancestors()], own]
    props = {}
    for p in g.all_properties:
        ranges = p.ranges or p.ranges_inferred
        props[p.id] = [p.title, p.qname,
                       [[getattr(r, "id", None), getattr(r, "title", str(r))] for r in ranges]]
    shapes, shape_groups = {}, {}
    for c in g.all_classes:
        headers, rows = [], None
        for x in getattr(c, "shacl_constraints", []):
            if x.header:
                headers.append(x.header)
                if x.header in shape_groups:
                    rows = None  # this group was already written
                else:
                    rows = shape_groups[x.header] = []
            elif rows is not None:
                prop = x.property_obj.onto_property
                rows.append([prop.id if prop else None,
                             prop.title if prop else x.property_obj.qname,
                             ", ".join(sorted(map(str, x.sh_minCount))) or "0",
                             ", ".join(sorted(map(str, x.sh_maxCount))) or "*",
                             [[t.entity.id if t.entity else None, t.qname] for t in x.value_types]])
        if headers:
            shapes[c.id] = headers
    return {"classes": classes, "props": props, "thing": thing,
            "shapes": shapes, "shape_groups": shape_groups}


##################
#
#  TREE DISPLAY FUNCTIONS [from ontospy web]
#
##################


def formatHTML_EntityTreeTable(treedict, element=0, _branch=()):
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

	Note: <_branch> holds <element> and the entities above it; an entity already on it is shown
	but not expanded again, so cycles (eg A > B > A) don't recurse forever (#142).

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
						  </tr>""" % (x.uri, x.slug, truncchar_inverse(x.title, 50))

        if treedict.get(x, None) and x not in _branch:
            stringa += """ <tr>
							<td class="space"></td>
							<td class="bar"></td>
							<td class="space"></td>
							<td>%s</td>
							</tr>""" % formatHTML_EntityTreeTable(treedict, x, _branch + (x,))

        # stringa += formatHTML_ClassTree(onto, treedict, x)
        # stringa += "</li>"
    stringa += "</table>"
    return stringa


def get_onto_for_testing(TEST_ONLINE=False):
    "Wrapper for util script used in viz main methods"
    if TEST_ONLINE:
        from ontospy import Ontospy
        g = Ontospy("http://cohere.open.ac.uk/ontology/cohere.owl#")
    else:
        from ontospy.core.manager import get_random_ontology
        uri, g = get_random_ontology(50)
    return g
