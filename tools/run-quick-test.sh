#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "CALLING [test_quick] in 1 second..."
echo "=================="
sleep 1
python -m ontospy.tests.test_quick


echo ""
echo "=================="
echo "Completed."
echo "=================="
