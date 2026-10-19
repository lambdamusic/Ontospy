# NOTICE
# This software was produced for the U.S. Government under contract FA8702-22-C-0001,
# and is subject to the Rights in Data-General Clause 52.227-14, Alt. IV (DEC 2007)
# ©2021 The MITRE Corporation. All Rights Reserved.

'''
This module works out, for documentation, the SHACL constraints that apply to each
class and each shape of an Ontospy graph.

A shape's constraints are read from the whole graph, so a property shape can be a blank
node (`sh:property [ sh:path ex:name ]`) or a named node (`sh:property ex:Person-name`, as
in DCAT-AP or QUDT). A shape applies to a class if it names it with sh:targetClass, or if
the class is itself a sh:NodeShape (an implicit class target, SHACL 2.1.3.3, as in SPDX,
QUDT or Brick).

The result is attached to the entities:
    OntoClass.shacl_constraints     the constraints of the shapes of the class and of its
                                    ancestors, each group after a header row
    OntoShape.shacl_constraints     the shape's own property constraints (for a property
                                    shape, the shape itself)
    OntoShape.targets               what the shape applies to, a list of (kind, Term)
    OntoShape.node_constraints      the shape's own node-level constraints, a list of
                                    (name, [values]), eg ("sh:closed", ["true"])
    OntoShape.used_by               for a named property shape, the shapes that use it
                                    (with sh:property), a list of Terms
'''

from typing import Any, Dict, List, Optional, Set, Tuple, Union

import rdflib
from rdflib import BNode, Graph, Literal, RDF, RDFS, SH, URIRef
from rdflib.collection import Collection
from rdflib.term import Node

from .entities import OntoClass, OntoProperty, OntoShape, Ontology, RdfEntity
from .utils import uri2niceString


class _EntityIndex(object):
    '''
    The entities of an Ontospy graph that have a page of their own, by URI. Built on first
    use, ie when the docs are rendered, so it includes the entities built after the shapes
    (eg individuals).
    '''

    def __init__(self, ontology_object: Ontology) -> None:
        self.ontology_object = ontology_object
        self._index: Optional[Dict[URIRef, RdfEntity]] = None

    def get(self, uri) -> Optional[RdfEntity]:
        if self._index is None:
            o = self.ontology_object
            self._index = {}
            # later buckets win: a URI that is both a class and a shape links to the class
            for bucket in [o.all_individuals, o.all_skos_concepts, o.all_shapes,
                           o.all_properties, o.all_classes]:
                for entity in bucket:
                    self._index[entity.uri] = entity
        return self._index.get(uri)


class Term(object):
    '''
    An RDF term mentioned by a constraint, eg a class, datatype or value.

    Attributes:
        self.node      the rdflib term
        self.qname     its prefixed name, or the literal's text
        self.entity    the entity of the graph with this URI (with a page of its own),
                       or None, eg for an XSD datatype or a class defined elsewhere
        self.href      the page of that entity, or None
    '''

    def __init__(self, node: Node, namespaces=None, index: Optional[_EntityIndex] = None) -> None:
        self.node = node
        self._index = index
        if isinstance(node, Literal):
            self.qname = str(node)
        else:
            self.qname = uri2niceString(node, namespaces) if isinstance(node, URIRef) else str(node)

    @property
    def entity(self) -> Optional[RdfEntity]:
        if self._index is None or not isinstance(self.node, URIRef):
            return None
        return self._index.get(self.node)

    @property
    def href(self) -> Optional[str]:
        entity = self.entity
        return entity.slug + ".html" if entity is not None else None

    # kept for templates written against the previous version of this module
    @property
    def onto_class(self) -> Optional[RdfEntity]:
        entity = self.entity
        return entity if isinstance(entity, OntoClass) else None

    def __eq__(self, other):
        return type(other) is type(self) and self.node == other.node

    def __hash__(self):
        return hash(self.node)

    def __str__(self):
        return self.qname

    def __repr__(self):
        return '<Term %s>' % self.qname


# the previous name of Term, which only held classes and datatypes
NodeShape = Term


class Property(object):
    '''
    The path of a property shape.

    Attributes:
        self.property_uri       the property URI, or None for a complex path (eg a sequence)
        self.onto_property      the OntoProperty with that URI, or None if the property is
                                not defined in the graph
        self.qname              the property's prefixed name, or the path written as in
                                SPARQL, eg "^ex:knows", "ex:a / ex:b", "(ex:a | ex:b)"
    '''

    def __init__(self, path: Node, graph: Optional[Graph] = None, namespaces=None,
                 properties: Optional[Dict[URIRef, OntoProperty]] = None) -> None:
        self.path = path
        self.property_uri = path if isinstance(path, URIRef) else None
        self.onto_property: Optional[OntoProperty] = (properties or {}).get(path) if self.property_uri else None
        self.qname = path_to_string(path, graph, namespaces)

    def __eq__(self, other):
        return type(other) is type(self) and self.path == other.path

    def __hash__(self):
        return hash(self.path)

    def __str__(self):
        return '<{}, {}>'.format(self.qname, self.onto_property)

    def __repr__(self):
        return str(self)


def path_to_string(path: Node, graph: Optional[Graph], namespaces=None) -> str:
    '''a SHACL property path (2.3.1) written as in SPARQL'''
    if isinstance(path, URIRef):
        return uri2niceString(path, namespaces)
    if graph is None or not isinstance(path, BNode):
        return str(path)
    if (path, RDF.first, None) in graph:  # a sequence
        return " / ".join(path_to_string(x, graph, namespaces) for x in _rdf_list(graph, path))
    for pred, fmt in [(SH.inversePath, "^%s"), (SH.zeroOrMorePath, "%s*"),
                      (SH.oneOrMorePath, "%s+"), (SH.zeroOrOnePath, "%s?")]:
        value = graph.value(path, pred)
        if value is not None:
            inner = path_to_string(value, graph, namespaces)
            if isinstance(value, BNode) and (value, RDF.first, None) in graph:
                inner = "(%s)" % inner
            return fmt % inner
    value = graph.value(path, SH.alternativePath)
    if value is not None:
        return "(%s)" % " | ".join(path_to_string(x, graph, namespaces) for x in _rdf_list(graph, value))
    return str(path)


def _rdf_list(graph: Graph, head: Node) -> List[Node]:
    try:
        return list(Collection(graph, head))
    except Exception:
        return []


class Constraint(object):
    '''
    The constraints of one property shape, or of several on the same path.

    Attributes are SETS of values: there should normally be only zero or one value for
    each, but there may be more, eg when two shapes constrain the same path. Ontospy's job
    is to display the ontology, not to validate it, so all the values are shown.

    A Header Constraint only has a header string: it names the class whose constraints
    follow, in a class's list of constraints.
    '''

    def __init__(self, property_obj: Optional[Property] = None, header=None) -> None:
        '''
        property_obj    the Property (path) this Constraint is about
        header          if present, this is a Header Constraint and property_obj is ignored
        '''
        if header:
            self.header = header
            return
        self.header = None
        self.property_obj = property_obj
        self.sh_path = property_obj.qname
        self.sh_order: Set[float] = set()
        self.sh_name: Set[str] = set()
        self.sh_description: Set[str] = set()
        self.sh_minCount: Set[str] = set()
        self.sh_maxCount: Set[str] = set()
        self.sh_datatype: Set[Term] = set()
        self.sh_class: Set[Term] = set()
        self.sh_node: Set[Term] = set()
        self.sh_nodeKind: Set[Term] = set()
        self.sh_minInclusive: Set[str] = set()
        self.sh_maxInclusive: Set[str] = set()
        self.sh_minExclusive: Set[str] = set()
        self.sh_maxExclusive: Set[str] = set()
        self.sh_minLength: Set[str] = set()
        self.sh_maxLength: Set[str] = set()
        self.sh_pattern: Set[str] = set()
        self.sh_languageIn: Set[str] = set()
        self.sh_uniqueLang: Set[str] = set()
        self.sh_disjoint: Set[Term] = set()
        self.sh_equals: Set[Term] = set()
        self.sh_lessThan: Set[Term] = set()
        self.sh_lessThanOrEquals: Set[Term] = set()
        self.sh_hasValue: Set[Term] = set()
        self.sh_in: List[Term] = []                 # an RDF list: keeps its order
        self.sh_or: List[List[str]] = []            # each a list of member shapes, as text
        self.sh_and: List[List[str]] = []
        self.sh_xone: List[List[str]] = []
        self.sh_not: List[str] = []
        self.sh_severity: Set[Term] = set()
        self.sh_message: Set[str] = set()
        self.sh_deactivated: Set[str] = set()
        self.rdftype_qname: Set[str] = set()    # of the property, eg "owl:ObjectProperty"
        self.rdfs_range: Set[Term] = set()      # of the property
        self.rdfs_comment: Set[str] = set()     # of the property

    @property
    def value_types(self) -> List[Term]:
        '''what the values must be: their datatype, class, node shape or node kind'''
        return sorted(self.sh_datatype | self.sh_class | self.sh_node, key=lambda t: t.qname) + \
            sorted(self.sh_nodeKind, key=lambda t: t.qname)

    @property
    def other_constraints(self) -> List[Tuple[str, List[Any]]]:
        '''the constraints that have no column of their own, as (name, [values]); the
        values are Terms or strings'''
        out: List[Tuple[str, List[Any]]] = []
        for name in ["hasValue", "in", "pattern", "minInclusive", "minExclusive",
                     "maxInclusive", "maxExclusive", "minLength", "maxLength", "languageIn",
                     "uniqueLang", "equals", "disjoint", "lessThan", "lessThanOrEquals",
                     "severity", "deactivated"]:
            values = getattr(self, "sh_" + name)
            if values:
                if isinstance(values, set):
                    values = sorted(values, key=str)
                out.append(("sh:" + name, list(values)))
        for name in ["or", "and", "xone"]:
            for members in getattr(self, "sh_" + name):
                out.append(("sh:" + name, members))
        for text in self.sh_not:
            out.append(("sh:not", [text]))
        return out

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class _Reader(object):
    '''reads the constraints of shapes from a graph'''

    LITERAL_PARAMS = ["name", "description", "minCount", "maxCount", "minInclusive",
                      "maxInclusive", "minExclusive", "maxExclusive", "minLength",
                      "maxLength", "pattern", "uniqueLang", "message", "deactivated"]
    TERM_PARAMS = ["datatype", "class", "node", "nodeKind", "disjoint", "equals",
                   "lessThan", "lessThanOrEquals", "severity"]

    def __init__(self, ontology_object: Ontology) -> None:
        self.graph: Graph = ontology_object.rdflib_graph
        self.namespaces = ontology_object.namespaces
        self.index = _EntityIndex(ontology_object)
        self.properties: Dict[URIRef, OntoProperty] = {p.uri: p for p in ontology_object.all_properties}

    def term(self, node: Node) -> Term:
        return Term(node, self.namespaces, self.index)

    def property_shapes(self, shape_uri: Node) -> List[Node]:
        '''the property shapes of a shape: its sh:property values or, if it is a property
        shape itself (it has a sh:path), the shape'''
        if self.graph.value(shape_uri, SH.path) is not None:
            return [shape_uri]
        return list(self.graph.objects(shape_uri, SH.property))

    def add_constraints(self, constraints: Dict[Node, Constraint], shape_uri: Node) -> None:
        '''add the constraints of a shape's property shapes to `constraints`, by path'''
        for property_shape in self.property_shapes(shape_uri):
            path = self.graph.value(property_shape, SH.path)
            if path is None:
                continue
            key = path if isinstance(path, URIRef) else path_to_string(path, self.graph, self.namespaces)
            if key not in constraints:
                constraints[key] = Constraint(Property(path, self.graph, self.namespaces, self.properties))
            self.read(constraints[key], property_shape)

    def read(self, constraint: Constraint, node: Node) -> None:
        g = self.graph
        for name in self.LITERAL_PARAMS:
            getattr(constraint, "sh_" + name).update(str(o) for o in g.objects(node, SH[name]))
        for name in self.TERM_PARAMS:
            getattr(constraint, "sh_" + name).update(self.term(o) for o in g.objects(node, SH[name])
                                                     if not isinstance(o, BNode))
        # a node shape given inline, eg sh:node [ sh:class ex:A ], is shown as text
        for name in ["node"]:
            for o in g.objects(node, SH[name]):
                if isinstance(o, BNode):
                    constraint.sh_node.add(Term(Literal(self.summary(o)), self.namespaces))
        for o in g.objects(node, SH.order):
            try:
                constraint.sh_order.add(float(o))
            except ValueError:
                pass
        for o in g.objects(node, SH.hasValue):
            constraint.sh_hasValue.add(self.term(o))
        for o in g.objects(node, SH["in"]):
            for member in _rdf_list(g, o):
                term = self.term(member)
                if term not in constraint.sh_in:
                    constraint.sh_in.append(term)
        for o in g.objects(node, SH.languageIn):
            constraint.sh_languageIn.update(str(x) for x in _rdf_list(g, o))
        for name in ["or", "and", "xone"]:
            for o in g.objects(node, SH[name]):
                alternatives = [self.summary(x) for x in _rdf_list(g, o)]
                if alternatives and alternatives not in getattr(constraint, "sh_" + name):
                    getattr(constraint, "sh_" + name).append(alternatives)
        for o in g.objects(node, SH["not"]):
            text = self.summary(o)
            if text not in constraint.sh_not:
                constraint.sh_not.append(text)

    def summary(self, shape: Node, depth: int = 0) -> str:
        '''a short text for a shape mentioned by another one, eg an alternative of sh:or:
        its name if it has one, else what it constrains, eg "sh:datatype xsd:string" or
        "sh:path ex:name, sh:minCount 1"'''
        if isinstance(shape, URIRef):
            return uri2niceString(shape, self.namespaces)
        if not isinstance(shape, BNode):
            return str(shape)
        pairs = [(p, o) for p, o in sorted(self.graph.predicate_objects(shape))
                 if p not in (RDF.type, SH.name, SH.description, SH.message)]
        if len(pairs) == 1 and pairs[0][0] in (SH.datatype, SH["class"], SH.node, SH.nodeKind) \
                and not isinstance(pairs[0][1], BNode):
            return self.term(pairs[0][1]).qname  # eg [ sh:datatype xsd:integer ]
        parts = []
        for p, o in pairs:
            pname = uri2niceString(p, self.namespaces)
            if p == SH.path:
                parts.append("%s %s" % (pname, path_to_string(o, self.graph, self.namespaces)))
            elif isinstance(o, BNode) and (o, RDF.first, None) in self.graph:
                parts.append("%s (%s)" % (pname, ", ".join(self.summary(x, depth + 1)
                                                           for x in _rdf_list(self.graph, o))))
            elif isinstance(o, BNode):
                parts.append("%s [%s]" % (pname, self.summary(o, depth + 1) if depth < 3 else "..."))
            else:
                parts.append("%s %s" % (pname, self.term(o).qname))
        return ", ".join(parts) if parts else str(shape)

    def targets(self, shape: OntoShape) -> List[Tuple[str, Term]]:
        out = []
        if (shape.uri, RDF.type, RDFS.Class) in self.graph or \
                (shape.uri, RDF.type, rdflib.OWL.Class) in self.graph:
            out.append(("implicit sh:targetClass", self.term(shape.uri)))
        for name in ["targetClass", "targetNode", "targetSubjectsOf", "targetObjectsOf"]:
            for o in sorted(self.graph.objects(shape.uri, SH[name])):
                out.append(("sh:" + name, self.term(o)))
        return out

    def node_constraints(self, shape: OntoShape) -> List[Tuple[str, List[Any]]]:
        '''the constraints of a node shape on the focus node itself, eg sh:closed'''
        if self.graph.value(shape.uri, SH.path) is not None:
            return []  # a property shape: these are in its table row
        c = Constraint(Property(shape.uri))
        self.read(c, shape.uri)
        out: List[Tuple[str, List[Any]]] = []
        for o in self.graph.objects(shape.uri, SH.closed):
            out.append(("sh:closed", [str(o)]))
        for o in self.graph.objects(shape.uri, SH.ignoredProperties):
            out.append(("sh:ignoredProperties", [self.term(x) for x in _rdf_list(self.graph, o)]))
        if c.value_types:
            out.append(("value type", c.value_types))
        out.extend(c.other_constraints)
        if c.sh_message:
            out.append(("sh:message", sorted(c.sh_message)))
        return out


def _sorted_constraints(constraints: Dict[Node, Constraint]) -> List[Constraint]:
    '''by sh:order, when given, then by path'''
    return sorted(constraints.values(), key=lambda c: (min(c.sh_order) if c.sh_order else float("inf"),
                                                      c.property_obj.qname))


def build_shacl_constraints(ontology_object: Ontology) -> Dict[OntoClass, List[Constraint]]:
    '''
    Arguments:
        ontology_object   An Ontospy Ontology object, once its classes, properties and
                          shapes have been built

    Return:
        {onto_class: [Constraint]}, for each class the constraints of its shapes and those
        of its ancestors, breadth-first, each group after a Header Constraint naming the
        class, and within a group sorted by sh:order then path.

    Also sets the shapes' shacl_constraints, targets, node_constraints and used_by (see the module
    docstring). The shapes must already be linked to their classes, explicit and implicit
    targets alike (OntoShape.targetClasses, OntoClass.all_shapes): Ontospy.build_shapes does it.

    For each property shape:
        (a) sh:path, a property or a property path, goes in the PROPERTY column
        (b) sh:minCount and sh:maxCount in the MIN and MAX columns
        (c) sh:datatype, sh:class, sh:node and sh:nodeKind in the value type column
        (d) the others, eg sh:in, sh:pattern or sh:or, are listed together
    and for the property itself, if defined in the ontology, its type (eg
    owl:ObjectProperty), rdfs:comment and rdfs:range.
    '''
    all_shacl_constraints: Dict[OntoClass, List[Constraint]] = dict()
    if ontology_object.rdflib_graph is None or not ontology_object.all_shapes:
        return all_shacl_constraints

    reader = _Reader(ontology_object)

    for shape in ontology_object.all_shapes:
        # the shape's own constraints
        constraints: Dict[Node, Constraint] = dict()
        reader.add_constraints(constraints, shape.uri)
        add_owl_property_constraints(constraints, reader)
        shape.shacl_constraints = _sorted_constraints(constraints)
        shape.targets = reader.targets(shape)
        shape.node_constraints = reader.node_constraints(shape)
        shape.used_by = sorted((reader.term(x) for x in reader.graph.subjects(SH.property, shape.uri)),
                               key=lambda t: t.qname)

    # A class's own group of constraints, read once and reused for each of its subclasses
    # rather than read again every time the class turns up in a lineage (backlog #13)
    groups: Dict[OntoClass, List[Constraint]] = dict()

    def group_of(lineage_class: OntoClass) -> List[Constraint]:
        if lineage_class not in groups:
            constraints: Dict[Node, Constraint] = dict()
            for shape in lineage_class.all_shapes:
                reader.add_constraints(constraints, shape.uri)
            group: List[Constraint] = []
            if constraints:
                add_owl_property_constraints(constraints, reader)
                group.append(Constraint(header=lineage_class.qname))
                group.extend(_sorted_constraints(constraints))
            groups[lineage_class] = group
        return groups[lineage_class]

    for onto_class in ontology_object.all_classes:
        constraints_list: List[Constraint] = []
        for lineage_class in get_lineage(onto_class):
            if lineage_class.all_shapes:
                constraints_list.extend(group_of(lineage_class))
        all_shacl_constraints[onto_class] = constraints_list

    return all_shacl_constraints


def add_owl_property_constraints(property_constraints: Dict[Node, Constraint], reader: _Reader) -> None:
    '''
    Add to each Constraint what the ontology says about its property, if it defines it:
    its type, description (eg its rdfs:comment) and rdfs:range.
    '''
    for constraint in property_constraints.values():
        onto_property = constraint.property_obj.onto_property
        if onto_property is None:
            continue
        if onto_property.rdftype_qname:
            constraint.rdftype_qname.add(onto_property.rdftype_qname)
        uri = onto_property.uri
        description = onto_property.bestDescription()
        if description:
            constraint.rdfs_comment.add(str(description))
        for o in reader.graph.objects(uri, RDFS.range):
            if isinstance(o, URIRef):
                constraint.rdfs_range.add(reader.term(o))


def get_lineage(onto_class: OntoClass) -> List[OntoClass]:
    '''
    Arguments:
        onto_class    An ontoClass object

    Return:
        LIST containing onto_class, its parents, grandparents, etc, in breadth-first order.
        The first item in the returned list is always the input, onto_class
        Remaining items are ancestor classes in breadth-first search order
    '''
    # Start with self
    unique_onto_classes: List[OntoClass] = [onto_class]
    seen: Set[OntoClass] = {onto_class}

    # Add ancestors one generation at a time (breadth-first), each generation in
    # alphabetical order. Iterative and skipping classes already seen, so cycles and
    # deep or multiply-inherited hierarchies don't recurse forever (#142).
    generation: List[OntoClass] = [onto_class]
    while generation:
        parent_classes: List[OntoClass] = []
        for sibling_class in generation:
            for parent_class in sibling_class.parents():
                assert isinstance(parent_class, OntoClass)
                if parent_class not in seen:
                    seen.add(parent_class)
                    parent_classes.append(parent_class)
        parent_classes.sort(key=lambda x: x.qname)
        unique_onto_classes.extend(parent_classes)
        generation = parent_classes

    # Return results
    return unique_onto_classes
