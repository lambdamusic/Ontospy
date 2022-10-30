# NOTICE
# This software was produced for the U.S. Government under contract FA8702-22-C-0001,
# and is subject to the Rights in Data-General Clause 52.227-14, Alt. IV (DEC 2007)
# ©2021 The MITRE Corporation. All Rights Reserved.

'''
This module implements a function that determines SHACL property constraints
from the triple provided by Ontospy.

In this file,
    OntoProperties is the ontospy class ontospy.core.entities.OntoProperties
    OntoClass is the ontospy class ontospy.core.entities.OntoClass
'''

from typing import Any, DefaultDict, Dict, List, Optional, Set, Tuple, Union

from collections import defaultdict
import rdflib
from rdflib import BNode, Graph, Literal, RDFS, SH, URIRef
from rdflib.term import Node
    # SH   = http://www.w3.org/ns/shacl#
    # OWL  = http://www.w3.org/2002/07/owl#
    # RDF  = http://www.w3.org/1999/02/22-rdf-syntax-ns#
    # RDFS = http://www.w3.org/2000/01/rdf-schema#


from .entities import OntoClass, OntoProperty, OntoShape, Ontology, RdfEntity

# TODO - This type is defined in what is currently a prerelease state of RDFLib.  Import rdflib.IdentifiedNode once RDFLib's version is >6.1.1.
IdentifiedNode = Union[BNode, URIRef]

# all_classes is a module-level tracking of all of the SHACL classes known to the caller of build_shacl_constraints.
# As a reminder, SHACL classes are explicitly noted as classes (e.g. RDF or OWL Class instances), or are inferred to be classes by appearing as a rdf:type Object.
# https://www.w3.org/TR/shacl/#dfn-shacl-class
# all_classes is indexed by the IRI of the class.  Note that this constrains OntoSpy to only representing classes that are not BNodes, which might or might not be an issue with anonymous classes defined as part of OWL Restrictions.
all_classes: Dict[URIRef, OntoClass] = dict()

# all_properties follows the same practice as all_classes.
all_properties: Dict[URIRef, OntoProperty] = dict()

namespace_manager = rdflib.namespace.NamespaceManager(Graph())


def set_namespace_manager(namespaces) -> None:
    for (prefix, uri) in namespaces:
        namespace_manager.bind(prefix, uri)


class NodeShape(object):
    '''
    Container for a class uri and its corresponding OntoClass object.
    A NodeShape MUST have a uri and may or may not have an OntoClass
    Two NodeShape objects are EQUAL if they have the same self.class_uri

    Attributes:
        self.class_uri       The URI of an ontology class
        self.onto_class      The OntoClass object with uri self.class_uri,
                                or None if this class is not in the ontology
        self.qname           The qname (onto_class.qname if onto_class is not None)
    '''
    # Class constant

    def __init__(self, class_uri: rdflib.URIRef) -> None:
        self.class_uri = class_uri
        self.onto_class = all_classes.get(class_uri)  # May be None
        self.qname = namespace_manager.qname(class_uri)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.class_uri == other.class_uri
        else:
            return False

    def __hash__(self):
        return hash(self.class_uri)

    def __str__(self):
        return '<{}, {}>'.format(self.qname, self.onto_class)
    def __repr__(self):
        return str(self)



class Property(object):
    '''
    Container for a property uri and its corresponding OntoProperty object.
    A Property MUST have a uri and may or may not have an OntoProperty
    Two Property objects are EQUAL if they have the same self.property_uri

    Attributes:
        self.property_uri       The URI of an ontology property
        self.onto_property      The OntoProperty object with uri self.property_uri,
                                or None if this property is not in the ontology
    '''

    def __init__(self, property_uri: rdflib.URIRef) -> None:
        self.property_uri = property_uri
        self.onto_property: Optional[OntoProperty] = all_properties.get(property_uri)
        self.qname: str
        try:
            self.qname = namespace_manager.qname(property_uri)
        except:
            self.qname = str(property_uri)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.property_uri == other.property_uri
        else:
            return False

    def __hash__(self):
        return hash(self.property_uri)

    def __str__(self):
        return '<{}, {}>'.format(self.property_uri, self.onto_property)
    def __repr__(self):
        return str(self)



class Constraint(object):
    '''
    Container for constraint attributes.

    Attributes are SETS of values.  Although there should normally be only zero
    or one value for each attribute, we need to be able to handle the
    possibility of there being multiple values.

    A Header Constraint is a Constraint object that contains only a header string
    If the header argument is specified, the property_obj is ignored and a Header Constraint is returned
    '''
    def __init__(self, property_obj=None, header=None) -> None:
        '''
        Create empty instance of this class.

        property_obj    The onto_prop object for this Constraint object to implement
        header          If present, this is a Header Constraint.  Ignore the property_obj.
        '''
        if header:
            self.header = header
            return

        self.property_obj = property_obj   # PROPERTY: Property object
        self.sh_path = property_obj.qname  # THIS PROPERTY, a Property object
        self.sh_minCount: Set[str] = set()
        self.sh_maxCount: Set[str] = set()
        self.sh_datatype: Set[NodeShape] = set()
        self.sh_class: Set[NodeShape] = set()
        self.sh_description: Set[str] = set()
        self.sh_minInclusive: Set[str] = set()
        self.sh_maxInclusive: Set[str] = set()
        self.sh_minExclusive: Set[str] = set()
        self.sh_maxExclusive: Set[str] = set()
        self.sh_minLength: Set[str] = set()
        self.sh_maxLength: Set[str] = set()
        self.sh_pattern: Set[str] = set()
        self.sh_disjoint: Set[RdfEntity] = set()            #  Property objects
        self.sh_equals: Set[OntoProperty] = set()              #  Property objects
        self.sh_lessThan: Set[OntoProperty] = set()            #  Property objects
        self.sh_lessThanOrEquals: Set[OntoProperty] = set()    #  Property objects
        self.sh_not: Set[NodeShape] = set()
        self.sh_hasValue: Set[Union[str, RdfEntity]] = set()
        self.sh_in: Set[RdfEntity] = set()
        self.rdftype_qname: Set[str] = set()       # "owl:ObjectProperty" exclusive-or "owl:DatatypeProperty"
        self.rdfs_range: Set[NodeShape] = set()
        self.rdfs_comment: Set[str] = set()


    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)



def build_shacl_constraints(ontology_object: Ontology) -> Dict[OntoClass, List[Constraint]]:
    '''
    Arguments:
        ontology_object   An Ontospy Ontology object

    Return:  All SHACL Constraint Dictionary
        all_shacl_constraints is {onto_class:[Constraint]}
        and the list of Constraint objects are sorted by property_uri.qname

    Ontodoc's job is to display the ontology, not to validate it.  If there are conflicting
    property ranges or cardinalities, all values are displayed.

    The display has eight columns:  PROPERTY, TYPE, DESCRIPTION, MIN, MAX, OTHER CONSTRAINTS, LOCAL TYPE, GLOBAL RANGE

    (1) Each sh:property entry describes a single property.
        The sh:property
        (a) MUST have a sh:path property, which is a property URI.  This is saved as property_uri and goes in the PROPERTY column.
        (b) MAY have sh:minCount, sh:maxCount.  This is saved as min_count and max_count, and goes into the MIN and MAX columns.
        (c) MAY have sh:class.  This is saved as a NodeShape object in range_obj and goes in the RANGE column, and TYPE is owl:ObjectProperty.
        (d) MAY have sh:datatype.  This is saved as a NodeShape object in range_obj, and goes in the RANGE column, and TYPE is owl:DatatypeProperty.

    (2) Each sh:path property MUST defined as an OWL property declaration in the ontology.
        The OWL property description
        (a) MUST have an rdftype_qname that is either "owl:ObjectProperty" or "owl:DatatypeProperty".  This is saved as property_type and goes in the TYPE column.
        (b) SHOULD have an rdfs:comment property.  This is saved as description and goes in the DESCRIPTION column.
        (c) SHOULD have an rdfs:range property.  This is saved as a NodeShape object in range_obj, and goes the RANGE column.

    Display notes (these defaults are implemented in the template, and may actually be implemented differently)
        If there is no property_uri, no property is displayed.
        If there is no property_type, the displayed value for TYPE is blank (this should never happen)
        If there is no description, the displayed value for DESCRIPTION is blank
        If there is no range_obj, the displayed value for RANGE is ("rdfs resource", None)
        If there is no min_count, the displayed value for MIN is '0'.
        If there is no max_count, the displayed value for MAX is '*'
    '''

    # Start with empty results
    all_shacl_constraints: Dict[OntoClass, List[Constraint]] = dict()

    # Compute {property_uri:OntoProperty}
    for onto_prop in ontology_object.all_properties:
        all_properties[onto_prop.uri] = onto_prop

    set_namespace_manager(ontology_object.namespaces)

    # Populate the dictionary mapping class IRIs to OntoClass objects.
    ontology_class: OntoClass
    for ontology_class in ontology_object.all_classes:
        all_classes[ontology_class.uri] = ontology_class

    # Do for each class in the ontology
    onto_class: OntoClass
    for onto_class in ontology_object.all_classes:

        # Start with an empty LIST of ordered Constraint objects for this onto_class
        constraints: List[Constraint] = []

        # Do for each class in the lineage (self, parents, grandparents, etc)
        lineage_classes: List[OntoClass] = get_lineage(onto_class)
        lineage_class: OntoClass
        for lineage_class in lineage_classes:

            # If class has no shapes, skip
            if not lineage_class.shapedProperties:
                continue

            # Start with empty dictionary of property constraints for this lineage class
            # The key of this dictionary is a property IRI (that is, a rdflib.URIRef).
            property_constraints: Dict[URIRef, Constraint] = dict()

            # Do for each shape in this class (multiple shapes may have constraints for the same property_uri)

            for shaped_property_dict in lineage_class.shapedProperties:
                assert isinstance(shaped_property_dict["shape"], OntoShape)
                shape: OntoShape = shaped_property_dict["shape"]
                # Parse triples to get property constraints for this shape and add to property_constraints
                add_property_constraints_from_shape_triples(lineage_class.uri, property_constraints, shape.triples)

            # Add property constraints from owl property descriptions to constraints
            add_owl_property_constraints(property_constraints)

            # If there's a header, add to LIST of constraints
            #if lineage_class != onto_class:
            #    constraints.append(Constraint(header = lineage_class.qname))

            # Always add header to LIST of constraints
            constraints.append(Constraint(header = lineage_class.qname))

            # Add constraints to LIST of constraints in alphabetical order
            constraints.extend(sorted(property_constraints.values(), key=lambda v:v.property_obj.qname))

        # Add cumulative constraints to all_shacl_constraints
        all_shacl_constraints[onto_class] = constraints

    # Return all the constraints
    return all_shacl_constraints


def add_property_constraints_from_shape_triples(
    class_uri: URIRef,
    property_constraints: Dict[URIRef, Constraint],
    shacl_triples: Optional[List[Tuple[IdentifiedNode, IdentifiedNode, Node]]]
) -> None:
    '''
    Arguments:
        class_uri                 URI of current class
        property_constraints      {property_uri:Constraint}
        shacl_triples             List of shacl triples [(s, p, o)] pertaining to sh:PropertyShapes attached to the current class.

    Action:
        Modify property_constraints by property_uris and their Constraint object derived from the shacl triples
    '''
    # If there are no triples, do nothing
    if not shacl_triples:
        return

    # Build temporary graph to get access to RDFLib iterators.
    tmp_graph = Graph()
    for shacl_triple in shacl_triples:
        tmp_graph.add(shacl_triple)

    # From sh:path, get property URI when object of sh:path triple is a named concept.
    # Once found, property_uri will be used to guarantee an entry for property_constraints.
    for n_property_shape, pred, obj in shacl_triples:
        if pred != SH["path"]:
            continue
        if not isinstance(obj, URIRef):
            # (sh:path can be an RDF List of predicates to follow in-sequence.  Designing documentation for that is left as future work.)
            continue
        property_uri: URIRef = obj
        
        # Find this property's Constraint object in property_constraints.
        # If it hasn't been defined yet, create one.
        if property_uri not in property_constraints:
            property_constraints[property_uri] = Constraint(property_obj=Property(property_uri))
        constraint: Constraint = property_constraints[property_uri]

        # Convert values in graph to sets of values to consolidate and/or compare after looping through lineage (outside scope of this subroutine).

        for triple in tmp_graph.triples((n_property_shape, SH["class"], None)):
            constraint.sh_class.update({NodeShape(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["datatype"], None)):
            constraint.sh_datatype.update({NodeShape(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["description"], None)):
            constraint.sh_description.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["disjoint"], None)):
            constraint.sh_disjoint.update({OntoProperty(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["equals"], None)):
            constraint.sh_equals.update({OntoProperty(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["hasValue"], None)):
            if isinstance(triple[2], Literal):
                constraint.sh_hasValue.update({str(triple[2])})
            else:
                constraint.sh_hasValue.update({RdfEntity(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["in"], None)):
            constraint.sh_in.update({RdfEntity(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["lessThan"], None)):
            constraint.sh_lessThan.update({OntoProperty(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["lessThanOrEquals"], None)):
            constraint.sh_lessThanOrEquals.update({OntoProperty(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["minCount"], None)):
            constraint.sh_minCount.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["maxCount"], None)):
            constraint.sh_maxCount.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["maxExclusive"], None)):
            constraint.sh_maxExclusive.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["maxInclusive"], None)):
            constraint.sh_maxInclusive.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["maxLength"], None)):
            constraint.sh_maxLength.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["minExclusive"], None)):
            constraint.sh_minExclusive.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["minInclusive"], None)):
            constraint.sh_minInclusive.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["minLength"], None)):
            constraint.sh_minLength.update({str(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["not"], None)):
            constraint.sh_not.update({NodeShape(triple[2])})

        for triple in tmp_graph.triples((n_property_shape, SH["pattern"], None)):
            constraint.sh_pattern.update({str(triple[2])})



def add_owl_property_constraints(property_constraints: Dict[URIRef, Constraint]) -> None:
    '''
    Arguments:
        property_constraints    {property_uri:Constraint}

    Action:
        Modify property_constraints by adding additional data
    '''
    # Do for each property_uri in cumulative constraints
    for property_uri, constraint in property_constraints.items():

        # Get OntoProperty object.  If no such object, do nothing
        property_obj = Property(property_uri)
        if property_obj.onto_property is None:
            return
        onto_property = property_obj.onto_property

        # From OntoProperty.rdftype_qname, add property_type
        constraint.rdftype_qname.add(onto_property.rdftype_qname)   # "owl:DatatypeProperty" or "owl:ObjectProperty"

        if onto_property.triples is None:
            return

        # Build temporary graph to get access to RDFLib iterators.
        tmp_graph = Graph()
        for rdfs_triple in onto_property.triples:
            tmp_graph.add(rdfs_triple)

        # From rdfs:comment, add comments from owl constraint to Constraints
        for triple in tmp_graph.triples((property_uri, RDFS["comment"], None)):
            constraint.rdfs_comment.update({str(triple[2])})

        # From rdfs:range, add NodeShape object to Constraints (skip BNodes)
        for triple in tmp_graph.triples((property_uri, RDFS["range"], None)):
            if not isinstance(triple[2], URIRef):
                continue
            constraint.rdfs_range.update({NodeShape(triple[2])})


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
    onto_classes: List[OntoClass] = [onto_class]

    # Add ancestors
    # Inner class -- recursively add ancestors, one generation at a time (breadth-first)
    def _add_ancestors(sibling_classes: List[OntoClass]) -> None:
        '''
        Arguments:
            sibling_classes  LIST of ontoClass objects whose parents to add

        Closure:
            onto_classes   Accumulating list of ancestor classes in breadth first order
        '''
        # Get next generation
        parent_classes: List[OntoClass] = []
        for sibling_class in sibling_classes:
            for parent_class in sibling_class.parents():
                assert isinstance(parent_class, OntoClass)
                parent_classes.append(parent_class)

        # If no parents, done
        if not parent_classes:
            return

        # Add parents in alphabetical order
        parent_classes.sort(key=lambda x:x.qname)
        onto_classes.extend(parent_classes)

        # Call self with parents
        _add_ancestors(parent_classes)


    _add_ancestors(onto_classes)

    # Remove duplicates while maintaining order
    unique_onto_classes: List[OntoClass] = []
    for onto_class in onto_classes:
        if onto_class not in unique_onto_classes:
            unique_onto_classes.append(onto_class)

    # Return results
    return unique_onto_classes
