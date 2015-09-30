#!/usr/bin/env python
# encoding: utf-8

"""
Python and RDF Utils for OntoSPy

Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""


from colorama import Fore, Back, Style


QUOTES = [
	{
		"text" : "If all things in logic are to be rigorously demonstrated with genuine proofs, then logic must come after ontology and psychology. Logic derives its principles from ontology and psychology. Now the parts of philosophy should be ordered in such a way that those parts come first which provide principles for other parts. Therefore, ontology and psychology should precede logic if everything in logic is to be rigorously demonstrated and if its rules are to be genuinely proven.", 
		"source" : "Christian Wolff", 
	} ,
	{
		"text" : "I suppose therefore that all things I see are illusions; I believe that nothing has ever existed of everything my lying memory tells me. I think I have no senses. I believe that body, shape, extension, motion, location are functions. What is there then that can be taken as true? Perhaps only this one thing, that nothing at all is certain.", 
		"source" : "Rene Descartes", 
	} ,
	{
		"text" : "Beyond the fiction of reality, there is the reality of the fiction.", 
		"source" : "Slavoj Zizek", 
	} ,
	{
		"text" : "An ontology is an explicit specification of a conceptualization.", 
		"source" : "Tom Gruber Hitchens", 
	} ,
	{
		"text" : "I shall distinguish descriptive, formal and formalized ontology. Each of these ontologies comes in two guises: domain-dependent and domain-independent. Domain-dependent ontologies concern categorically closed regions of being; on the other hand, a domain independent ontology may be properly called general ontology. (...)Descriptive ontology concerns the collection of such prima facie information either in some specific domain of analysis or in general.", 
		"source" : "Roberto Poli", 
	} ,
	{
		"text" : "Bodies are real entities. Surfaces and lines are but fictitious entities. A surface without depth, a line without thickness, was never seen by any man; no; nor can any conception be seriously formed of its existence.", 
		"source" : "Jeremy Bentham", 
	} ,
	{
		"text" : "Nonbeing must in some sense be, otherwise what is it that there is not? This tangled doctrine might be nicknamed Plato's beard; historically it has proved tough, frequently dulling the edge of Occam's razor.", 
		"source" : "Willard Van Orman Quine, 'On What There Is', 1953", 
	} ,
	{
		"text" : "Ontology or the science of something and of nothing, of being and not-being, of the thing and the mode of the thing, of substance and accident.", 
		"source" : "Gottfried Wilhelm Leibniz", 
	} ,
	{
		"text" : "The predicates of a thing that are more general are the first principles of human cognition, thus ontology belongs, with reason, to metaphysics", 
		"source" : "Alexander Baumgarten", 
	} ,
	{
		"text" : "We now begin the science of the properties of all things in general, which is called ontology. (...) One easily comprehends that it will contain nothing but all basic concepts and basic propositions of our a priori cognition in general: for if it is to consider the properties of all things, then it has as an object nothing but a thing in general, i.e., every object of thought, thus no determinate object. Thus nothing remains for me other than the cognizing, which I consider.", 
		"source" : "Immanuel Kant", 
	} ,
	{
		"text" : "Ontology is that science (as part of metaphysics) which consists in a system of all concepts of the understanding, and principles, but only so far as they refer to objects that can be given to the senses, and thus confirmed by experience. It makes no allusion to the super-sensible, which is nevertheless the final aim of metaphysics, and thus belongs to the latter only as a propaedeutic, as the hallway or vestibule of metaphysics proper, and is called transcendental philosophy, because it contains the conditions and first elements of all our knowledge a priori.", 
		"source" : "Immanuel Kant", 
	} ,
	{
		"text" : "The first stage of metaphysics can be called that of ontology, since it does not teach us to investigate the essence of our concepts of things by a resolution into their elements, which is the business of logic; it tells us, rather, what concepts of things we frame to ourselves a priori, and how, in order to subsume thereunder whatever may be given to us in intuition generally.", 
		"source" : "Immanuel Kant", 
	} ,
	{
		"text" : "To be is to be perceived.", 
		"source" : "George Berkeley", 
	} ,
	{
		"text" : "The main thread of ontology in the philosophical sense is the study of entities and their relations. The question ontology asks is: What kinds of things exist or can exist in the world, and what manner of relations can those things have to each other? Ontology is less concerned with what is than with what is possible.", 
		"source" : "Clay Shirky", 
	},
]







# http://www.ontology.co/ontology-definitions-one.htm