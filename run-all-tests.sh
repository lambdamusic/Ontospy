#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "CALLING [test_load_local] in 5 seconds..."
echo "=================="
sleep 5
python -m ontospy.tests.test_load_local


echo ""
echo "=================="
echo "CALLING [test_load_remote] in 5 seconds..."
echo "=================="
sleep 5
python -m ontospy.tests.test_load_remote

echo ""
echo "=================="
echo "CALLING [test_sparql] in 5 seconds..."
echo "=================="
sleep 5
python -m ontospy.tests.test_sparql

echo ""
echo "=================="
echo "CALLING [test_shapes] in 5 seconds..."
echo "=================="
sleep 5
python -m ontospy.tests.test_shapes

echo ""
echo "=================="
echo "Completed."
echo "=================="
