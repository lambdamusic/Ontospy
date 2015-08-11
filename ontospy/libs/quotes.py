#!/usr/bin/env python
# encoding: utf-8

"""
Python and RDF Utils for OntoSPy

Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""


from colorama import Fore, Back, Style


QUOTES = [
	{
		"text" : "For, after all, how do we know that two and two make four? Or that the force of gravity works? Or that the past is unchangeable? If both the past and the external world exist only in the mind, and if the mind itself is controllable - what then?", 
		"source" : "George Orwell, 1984", 
	} ,
	{
		"text" : "I suppose therefore that all things I see are illusions; I believe that nothing has ever existed of everything my lying memory tells me. I think I have no senses. I believe that body, shape, extension, motion, location are functions. What is there then that can be taken as true? Perhaps only this one thing, that nothing at all is certain.", 
		"source" : "Rene Descartes", 
	} ,
	{
		"text" : "Beyond the fiction of reality, there is the reality of the fiction.", 
		"source" : "Slavoj Zizek, Less Than Nothing: Hegel and the Shadow of Dialectical Materialism", 
	} ,
	{
		"text" : "In ridiculing a pathetic human fallacy, which seeks explanation where none need be sought and which multiplies unnecessary assumptions, one should not mimic primitive ontology in order to challenge it. Better to dispose of the needless assumption altogether. This holds true for everything from Noah's flood to the Holocaust.", 
		"source" : "Christopher Hitchens", 
	} ,
	{
		"text" : "In the mind of all, fiction, in the logical sense, has been the coin of necessity; - in that of poets of amusement - in that of the priest and the lawyer of mischievous immorality in the shape of mischievous ambition, and too often both priest and lawyer have framed or made in part this instrument.", 
		"source" : "Jeremy Bentham, The Panopticon Writings", 
	} ,
	{
		"text" : "Bodies are real entities. Surfaces and lines are but fictitious entities. A surface without depth, a line without thickness, was never seen by any man; no; nor can any conception be seriously formed of its existence.", 
		"source" : "Jeremy Bentham, The Panopticon Writings", 
	} ,
	{
		"text" : "Nonbeing must in some sense be, otherwise what is it that there is not? This tangled doctrine might be nicknamed Plato's beard; historically it has proved tough, frequently dulling the edge of Occam's razor.", 
		"source" : "Willard Van Orman Quine, 'On What There Is', 1953", 
	} ,
	{
		"text" : "To be is to be perceived.", 
		"source" : "George Berkeley", 
	} ,
]
