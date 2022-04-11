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

import typing

from collections import defaultdict
import rdflib
from rdflib import SH, RDFS
    # SH   = http://www.w3.org/ns/shacl#
    # OWL  = http://www.w3.org/2002/07/owl#
    # RDF  = http://www.w3.org/1999/02/22-rdf-syntax-ns#
    # RDFS = http://www.w3.org/2000/01/rdf-schema#

import ontospy


class NodeShape:
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
    all_classes = {}
    namespace_manager = None

    def __init__(self, class_uri):
        self.class_uri = class_uri
        self.onto_class = self.all_classes.get(class_uri)  # May be None
        self.qname = self.namespace_manager.qname(class_uri)

    @classmethod
    def set_all_classes(cls, all_classes):
        cls.all_classes = all_classes

    @classmethod
    def set_namespace_manager(cls, namespaces):
        cls.namespace_manager = rdflib.Graph().namespace_manager
        for (prefix, uri) in namespaces:
            cls.namespace_manager.bind(prefix, uri)

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



class Property:
    '''
    Container for a property uri and its corresponding OntoProperty object.
    A Property MUST have a uri and may or may not have an OntoProperty
    Two Property objects are EQUAL if they have the same self.property_uri

    Attributes:
        self.property_uri       The URI of an ontology property
        self.onto_property      The OntoProperty object with uri self.property_uri,
                                or None if this property is not in the ontology
    '''
    # Class constant
    all_properties = {}
    namespace_manager = None
    namespace_lookup = {}

    def __init__(self, property_uri):
        if isinstance(property_uri, rdflib.term.Literal):
            tokens = property_uri.value.split(':')
            if len(tokens) == 2:
                prefix, propname = tokens
                namespace = self.namespace_lookup.get(prefix)
                if namespace:
                    property_uri = rdflib.term.URIRef(namespace + propname)
        self.property_uri = property_uri   # may be a Literal instead of a URI
        self.onto_property = self.all_properties.get(property_uri)  # May be None
        try:
            self.qname = self.namespace_manager.qname(property_uri)
        except:
            self.qname = str(property_uri)

    @classmethod
    def set_all_properties(cls, all_properties):
        cls.all_properties = all_properties

    @classmethod
    def set_namespace_manager(cls, namespaces):
        cls.namespace_manager = rdflib.Graph().namespace_manager
        for (prefix, uri) in namespaces:
            cls.namespace_manager.bind(prefix, uri)
            cls.namespace_lookup[prefix] = str(uri)

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



class Constraint:
    '''
    Container for constraint attributes.

    Attributes are SETS of values.  Although there should normally be only zero
    or one value for each attribute, we need to be able to handle the
    possibility of there being multiple values.

    A Header Constraint is a Constraint object that contains only a header string
    If the header argument is specified, the property_obj is ignored and a Header Constraint is returned
    '''
    def __init__(self, property_obj=None, header=None):
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
        self.sh_minCount = set()
        self.sh_maxCount = set()
        self.sh_datatype = set()
        self.sh_class = set()
        self.sh_description = set()
        self.sh_minInclusive = set()
        self.sh_maxInclusive = set()
        self.sh_minExclusive = set()
        self.sh_maxExclusive = set()
        self.sh_minLength = set()
        self.sh_maxLength = set()
        self.sh_pattern = set()
        self.sh_equals = set()              #  Property objects
        self.sh_disjoint = set()            #  Property objects
        self.sh_lessThan = set()            #  Property objects
        self.sh_lessThanOrEquals = set()    #  Property objects
        self.sh_not = set()
        self.sh_hasValue = set()
        self.sh_in = set()
        self.rdftype_qname = set()       # "owl:ObjectProperty" and/or "owl:DatatypeProperty"
        self.rdfs_range = set()
        self.rdfs_comment = set()


    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)



def build_shacl_constraints(ontology_object: ontospy.core.entities.Ontology) -> typing.Dict[ontospy.core.entities.OntoClass, Constraint]:
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
    all_shacl_constraints = {}   # {onto_class:[Constraint]}

    # Compute {property_uri:OntoProperty}
    all_properties = {onto_prop.uri:onto_prop for onto_prop in ontology_object.all_properties}   # {property_uri:OntoProperty}
    Property.set_all_properties(all_properties)
    Property.set_namespace_manager(ontology_object.namespaces)

    # Compute {class_uri:OntoClass}
    all_classes = {onto_class.uri:onto_class for onto_class in ontology_object.all_classes}      # {class_uri:OntoClass}
    NodeShape.set_all_classes(all_classes)
    NodeShape.set_namespace_manager(ontology_object.namespaces)

    # Do for each class in the ontology
    for onto_class in ontology_object.all_classes:

        # Start with an empty LIST of ordered Constraint objects for this onto_class
        constraints = []   # [Constraint]

        # Do for each class in the lineage (self, parents, grandparents, etc)
        lineage_classes = get_lineage(onto_class)
        for lineage_class in lineage_classes:

            # If class has no shapes, skip
            if not lineage_class.shapedProperties:
                continue

            # Start with empty dictionary of property constraints for this lineage class
            property_constraints = {}  # {property_uri:Constraint}

            # Do for each shape in this class (multiple shapes may have constraints for the same property_uri)
            for shape in {item['shape'] for item in lineage_class.shapedProperties}:

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

        # Add cumulative constraints to all_shacle_constraints
        all_shacl_constraints[onto_class] = constraints

    # Return all the constraints
    return all_shacl_constraints


def add_property_constraints_from_shape_triples(class_uri, property_constraints, shacl_triples):
    '''
    Arguments:
        class_uri                 URI of current class
        property_constraints      {property_uri:Constraint}
        shacl_triples             LIST of shacl triples [(s, p, o)]

    Action:
        Modify property_constraints by property_uris and their Constraint object derived from the shacl triples
    '''
    # If there are no triples, do nothing
    if not shacl_triples:
        return

    # Build spo_dict = {subj:{pred:{obj}}} from triples
    spo_dict = defaultdict(lambda: defaultdict(set))
    for subj, pred, obj in shacl_triples:
        spo_dict[subj][pred].add(obj)

    # If spo_dict does not contain the class_uri, something is very wrong
    if not class_uri in spo_dict:
        raise Exception('Something is very wrong.  Class URI not in triples.')

    # Get property bnodes
    # FIXME: The 'bnodes' variable makes an incorrect assumption on the graph node in the object position of 'sh:property'.  A SHACL PropertyShape can be identified as a blank node or an IRI.  This class is being incorrectly filtered to only BNodes.
    bnodes: typing.List[typing.Union[rdflib.URIRef, rdflib.BNode]] = spo_dict[class_uri].get(SH['property'], [])
    if not bnodes:
        return

    # If spo_dict is missing does not contain one of the bnodes, something is very wrong
    for bnode in bnodes:
        if bnode not in spo_dict:
            raise Exception('Something is very wrong.  Triples refer to BNode not in triples.')

    # Traverse bnodes and add to property_constraints
    # Do for each bnode
    for bnode in bnodes:
        po_dict = spo_dict[bnode]

        # From sh:path, get property URI
        property_uris = po_dict.get(SH['path'])
        if not property_uris:
            continue    # BNode has no shacl property
        if len(property_uris) > 1:
            raise Exception('Something is very wrong.  Multiple property_uris for a property bnode')
        property_uri = list(property_uris)[0]

        # Find this property's Constraint object in property_constraints.
        # If it hasn't been defined yet, create one.
        if property_uri not in property_constraints:
            property_constraints[property_uri] = Constraint(property_obj=Property(property_uri))
        constraint = property_constraints[property_uri]

        # Add shape attributes
        constraint.sh_minCount.update({str(literal.value) for literal in po_dict.get(SH['minCount'], [])})  # Strings
        constraint.sh_maxCount.update({str(literal.value) for literal in po_dict.get(SH['maxCount'], [])})  # Strings
        constraint.sh_datatype.update({NodeShape(uri) for uri in po_dict.get(SH['datatype'], [])})   # NodeShape objects
        constraint.sh_class.update({NodeShape(uri) for uri in po_dict.get(SH['class'], [])})         # NodeShape objects
        constraint.sh_minInclusive.update({str(literal.value) for literal in po_dict.get(SH['minInclusive'], [])})  # Strings
        constraint.sh_maxInclusive.update({str(literal.value) for literal in po_dict.get(SH['maxInclusive'], [])})  # Strings
        constraint.sh_minExclusive.update({str(literal.value) for literal in po_dict.get(SH['minExclusive'], [])})  # Strings
        constraint.sh_maxExclusive.update({str(literal.value) for literal in po_dict.get(SH['maxExclusive'], [])})  # Strings
        constraint.sh_minLength.update({str(literal.value) for literal in po_dict.get(SH['minLength'], [])})  # Strings
        constraint.sh_maxLength.update({str(literal.value) for literal in po_dict.get(SH['maxLength'], [])})  # Strings
        constraint.sh_pattern.update({str(literal.value) for literal in po_dict.get(SH['pattern'], [])})  # Strings
        constraint.sh_equals.update({Property(iri) for iri in po_dict.get(SH['equals'], [])})  # Property objects
        constraint.sh_disjoint.update({Property(iri) for iri in po_dict.get(SH['disjoint'], [])})  # Property objects
        constraint.sh_lessThan.update({Property(iri) for iri in po_dict.get(SH['lessThan'], [])})  # Property objects
        constraint.sh_lessThanOrEquals.update({Property(iri) for iri in po_dict.get(SH['lessThanOrEquals'], [])})  # Property objects
        constraint.sh_not.update({str(uri) for uri in po_dict.get(SH['not'], [])})  # String for Shape uris
        constraint.sh_hasValue.update({str(value) for value in po_dict.get(SH['hasValue'], [])})  # String for some value
        constraint.sh_in.update({str(value) for value in po_dict.get(SH['in'], [])})  # String for the head node of a Shacl list
        constraint.sh_description.update({str(literal.value) for literal in po_dict.get(SH['description'], [])})  # String




def add_owl_property_constraints(property_constraints):
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
        onto_property = property_obj.onto_property
        if not property_obj.onto_property:
            return

        # From OntoProperty.rdftype_qname, add property_type
        constraint.rdftype_qname.add(onto_property.rdftype_qname)   # "owl:DatatypeProperty" or "owl:ObjectProperty"

        # Build spo_dict = {subj:{pred:{obj}}} from triples
        spo_dict = defaultdict(lambda: defaultdict(set))
        for subj, pred, obj in onto_property.triples:
            spo_dict[subj][pred].add(obj)

        # Get po_dict for this property
        po_dict = spo_dict.get(property_uri)
        if not po_dict:
            return

        # From rdfs:comment, add comments from owl constraint to Constraints
        constraint.rdfs_comment.update({str(literal.value) for literal in po_dict.get(RDFS['comment'], [])})  # String

        # From rdfs:range, add NodeShape object to Constraints (skip BNodes)
        constraint.rdfs_range.update({NodeShape(class_uri) for class_uri in po_dict.get(RDFS['range'], []) if isinstance(class_uri, rdflib.term.URIRef)})



def get_lineage(onto_class):
    '''
    Arguments:
        onto_class    An ontoClass object

    Return:
        LIST containing onto_class, its parents, grandparents, etc, in breadth-first order.
        The first item in the returned list is always the input, onto_class
        Remaining items are ancestor classes in breadth-first search order
    '''
    # Inner class -- recursively add ancestors, one generation at a time (breadth-first)
    def _add_ancestors(sibling_classes):
        '''
        Arguments:
            sibling_classes  LIST of ontoClass objects whose parents to add

        Closure:
            onto_classes   Accumulating list of ancestor classes in breadth first order
        '''
        # Get next generation
        parent_classes = []
        for sibling_class in sibling_classes:
            parent_classes.extend(sibling_class.parents())

        # If no parents, done
        if not parent_classes:
            return

        # Add parents in alphabetical order
        parent_classes.sort(key=lambda x:x.qname)
        onto_classes.extend(parent_classes)

        # Call self with parents
        _add_ancestors(parent_classes)


    # Start with self
    onto_classes = [onto_class]

    # Add ancestors
    _add_ancestors([onto_class])

    # Remove duplicates while maintaining order
    unique_onto_classes = []
    for onto_class in onto_classes:
        if onto_class not in unique_onto_classes:
            unique_onto_classes.append(onto_class)

    # Return results
    return unique_onto_classes
