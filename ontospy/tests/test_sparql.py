# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit test stub for ontosPy

Run like this:

$ python -m ontospy.tests.test_sparql

"""

from __future__ import print_function
import time
import unittest
import os
import sys
from .. import *
from ..core import *
from ..core.utils import *


# sanity check
printDebug(f"-------------------\nOntospy {VERSION}\n-------------------")


class NHKInvalidSPARQLQueryError(Exception):
    pass


class TestSparqlStore(unittest.TestCase):

    ENDPOINT = "http://dbpedia.org/sparql"

    printDebug(f"""\n=================\n
    \nTEST SPARQL: Loading data from remote endpoint.
    \n\n=================""", bg="blue", fg="white")

    time.sleep(3)

    def test1_load_dbpedia(self):
        """
        Check if the dbpedia endpoint loads ok
        "http://dbpedia.org/sparql"
        """
        printDebug("\n=================\nTEST: Querying <%s> endpoint...\n=================" %
                   self.ENDPOINT, bg="green")

        o = Ontospy(sparql_endpoint=self.ENDPOINT, verbose=True)

        print(o), print("---------")

        q1 = o.query("select distinct ?b where {?x a ?b} limit 10")
        q2 = o.query(
            '''SELECT ?name ?birth ?death ?person WHERE {
               ?person dbo:birthPlace <http://dbpedia.org/resource/Berlin> .
               ?person dbo:birthDate ?birth .
               ?person foaf:name ?name .
               ?person dbo:deathDate ?death .
               FILTER (?birth < "1900-01-01"^^xsd:date) . } ORDER BY ?name
            '''
        )
        q3 = o.query(
            '''SELECT ?name ?birth ?description ?person WHERE {
               ?person a dbo:MusicalArtist .
               ?person dbo:birthPlace <http://dbpedia.org/resource/Berlin> .
               ?person dbo:birthDate ?birth .
               ?person foaf:name ?name .
               ?person rdfs:comment ?description .
               FILTER (LANG(?description) = 'en') .
               } ORDER BY ?name
            '''
        )
        q4 = o.query(
            '''
            SELECT distinct ?soccerplayer ?countryOfBirth ?team ?countryOfTeam ?stadiumcapacity
            { 
            ?soccerplayer a dbo:SoccerPlayer ;
            dbo:position|dbp:position <http://dbpedia.org/resource/Goalkeeper_(association_football)> ;
            dbo:birthPlace/dbo:country* ?countryOfBirth ;
            #dbo:number 13 ;
            dbo:team ?team .
            ?team dbo:capacity ?stadiumcapacity ; dbo:ground ?countryOfTeam . 
            ?countryOfBirth a dbo:Country ; dbo:populationTotal ?population .
            ?countryOfTeam a dbo:Country .
            FILTER (?countryOfTeam != ?countryOfBirth)
            FILTER (?stadiumcapacity > 30000)
            FILTER (?population > 10000000)
            } order by ?soccerplayer
        '''
        )
        error_message = "An error occurred while parsing the SPARQL query."
        if q1:
            for el in q1:
                print(el)
        else:
            raise NHKInvalidSPARQLQueryError(error_message)

        if q2:
            for e2 in q2:
                print(e2)
        else:
            raise NHKInvalidSPARQLQueryError(error_message)

        if q3:
            for e3 in q3:
                print(e3)
        else:
            raise NHKInvalidSPARQLQueryError(error_message)

        if q4:
            for e4 in q4:
                print(e4)
        else:
            raise NHKInvalidSPARQLQueryError(error_message)


if __name__ == "__main__":
    unittest.main()
