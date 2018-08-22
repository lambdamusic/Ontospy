#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "CALLING [test_load_local] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_load_local

echo ""
echo "=================="
echo "CALLING [test_methods] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_methods

echo ""
echo "=================="
echo "CALLING [test_load_remote] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_load_remote

echo ""
echo "=================="
echo "CALLING [test_sparql] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_sparql

echo ""
echo "=================="
echo "CALLING [test_shapes] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_shapes

echo ""
echo "=================="
echo "CALLING [test_shaped_properties] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_shaped_properties

echo ""
echo "=================="
echo "Completed."
echo "=================="
