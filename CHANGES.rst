OntosPy Changelog
=======================


November 1, 2014
---------------------------------
- added methods to extract OWL.AnnotationProperties

October 16, 2014
---------------------------------
- installed package on Pypi
- added executable: 'sketchonto' (generated via distutils)


October 11, 2014
---------------------------------
- sketch: added shortcuts 
	- (sub == rdfs:subClassOf) (class == owl:Class)
- sketch: added commands for a default_sketch


September 19, 2014
---------------------------------
- added Sketch utility
- added a dot file export mechanism 
	- so that we can open this stuff quickly in omniGraffle
	- http://paco.to/2004/omnigraffle-and-graphviz
	- http://en.wikipedia.org/wiki/DOT_(graph_description_language)

EG with labels

digraph graphname {
     a -> b [label=instanceOf];
     b -> d [label=isA];
 }


September 3, 2014
---------------------------------
- refactored ontology loading routine 


July 10, 2014
---------------------------------
- added webViz method that integrates d3 stuff
	- to be tested more!
	- added the tree view template too
		- but data format isn't finished yet (ps check also http://bl.ocks.org/mbostock/4063570)	 http://bl.ocks.org/mbostock/4339184		


2013-09-23
- added loadTriples method; separate loadURI from __setupOntology()

2013-06-02
- refactored, fixed a few bugs

2013-05-31
- added methods for proputils.pyerties

2013-05-27
- fixed ontoTree so to include OWL.Thing
- added alpha sorting to __buildClassTree
- split ontologyURI() and ontologyPrettyURI
- modified __ontologyURI so to include DC.identifier metadata
- updated ontologyAnnotations method: now multiple annotations are returned correctly
- added ontologyPhysicalLocation property

2013-05-24
- addded propertyRepresentation method
- fixed <classAllSupers> and <classAllSubs>: added wrapper so to preserve tree order
- added classRangeFor and classDomainFor; classProperties is now more generic;
- changed entityComment and entityLabel to pull out all results by default
- supers and subs methods: added parameter for sorting so to preserve tree order
- changed ontologyURI method to private; ignoring blank nodes now
- added the public -ontologyClassTree- property (previously called __classTree)
- added the FAMOUS ONTOLOGIES variables for loading stuff more easily
	eg: o = ontospy.Ontology(ontospy.FAMOUS_ONTOLOGIES.FRBR)


2013-05-09
- changed the default verbose option 


26 March 2013

- added inheritance to spy.classProperties
- improved compare script


25 March 2013 

- changed names of methods.. now all camelcased and more intuitive
- added module to compare two ontologies
