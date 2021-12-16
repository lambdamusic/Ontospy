#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "** [1/5] **"
echo "CALLING [test_load_local] ..."
echo "=================="
python -m ontospy.tests.test_load_local
sleep 2

echo ""
echo "=================="
echo "** [2/5] **"
echo "CALLING [test_methods] ..."
echo "=================="
python -m ontospy.tests.test_methods
sleep 2

echo ""
echo "=================="
echo "** [3/5] **"
echo "CALLING [test_load_remote] ..."
echo "=================="
python -m ontospy.tests.test_load_remote
sleep 2

echo ""
echo "=================="
echo "** [4/5] **"
echo "CALLING [test_sparql] ..."
echo "=================="
python -m ontospy.tests.test_sparql
sleep 2

echo ""
echo "=================="
echo "** [5/5] **"
echo "CALLING [test_shapes]..."
echo "=================="
python -m ontospy.tests.test_shapes
sleep 2

echo ""
echo "=================="
echo "Completed."
echo "=================="
