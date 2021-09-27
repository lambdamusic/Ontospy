#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "CALLING [tests/quick] in 1 second..."
echo "=================="
sleep 1
python -m ontospy.tests.quick


echo ""
echo "=================="
echo "Completed."
echo "=================="
