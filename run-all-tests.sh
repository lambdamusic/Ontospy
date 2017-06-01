#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "test_load_local..."
echo "=================="

python -m ontospy.tests.test_load_local

echo "=================="
echo "test_load_remote...."
echo "=================="

python -m ontospy.tests.test_load_remote

echo "=================="
echo "test_sparql..."
echo "=================="

python -m ontospy.tests.test_sparql

echo "=================="
echo "test_shapes..."
echo "=================="

python -m ontospy.tests.test_shapes

echo "=================="
echo "Completed."
echo "=================="
