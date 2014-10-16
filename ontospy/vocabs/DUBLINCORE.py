#!/usr/bin/env python
# encoding: utf-8

##################
#  Thu May 12 15:32:26 BST 2011
#  DUBLINCORE ELEMENTS vocabulary 
#  http://dublincore.org/documents/dces/
# 
#  michelepasin.org
##################


from rdflib import Namespace

DCNS = Namespace("http://purl.org/dc/elements/1.1/")
contributor = 	DCNS["contributor"]
coverage = DCNS["coverage"]
creator	= DCNS["creator"]
date = DCNS["date"]
description = DCNS["description"]
format = DCNS["format"]
identifier = DCNS["identifier"]
language = DCNS["language"]
publisher = DCNS["publisher"]
relation = DCNS["relation"]
rights = DCNS["rights"]
source = DCNS["source"]
subject = DCNS["subject"]
title = DCNS["title"]
type = DCNS["type"]
