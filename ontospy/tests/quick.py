# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Test Quick: use this file to quickly run scripts/tests which will then be integrated into proper tests

"""

import click 

import unittest, os, sys
from .. import *
from ..core import *
from ..core.utils import *


from .context import TEST_RDF_FOLDER, TEST_SHAPES_FOLDER


# sanity check
print("-------------------\nOntospy ", VERSION, "\n-------------------")



@click.command()
@click.argument('test_number', nargs=1)
def main(test_number):

	test_number = int(test_number)


	if test_number == 1:

		print("=================\n*** QUICK TEST 1 ***\n=================\n")

		f = TEST_RDF_FOLDER + "paper.jsonld"

		o = Ontospy(f, verbose=True, rdf_format="json-ld", hide_implicit_types=False, hide_base_schemas=False, hide_implicit_preds=False)
		print(f)			



	if test_number == 2:

		print("=================\n*** QUICK TEST 2 ***\n=================\n")

		uri, title = "http://examples.com", "My ontology"
		printDebug(click.style("[%d]" % 1, fg='blue') +
				click.style(uri + " ==> ", fg='black') +
				click.style(title, fg='red'))


		from colorama import Fore, Style

		printDebug(Fore.BLUE + Style.BRIGHT + "[%d]" % 1 + 
              Style.RESET_ALL + uri + " ==> " + Fore.RED + title + 
              Style.RESET_ALL)


	if test_number == 3:

		print("=================\n*** QUICK TEST 1 ***\n=================\n")

		f = TEST_RDF_FOLDER + "pizza.ttl"

		o = Ontospy(f, verbose=True, rdf_format="ttl", hide_implicit_types=False, hide_base_schemas=True, hide_implicit_preds=False, hide_individuals=False)
		print(f)
		for x in o.all_individuals:
			print(x.qname, [z.uri for z in x.instance_of()])			





if __name__ == '__main__':
	main()

