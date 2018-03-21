#!/bin/bash

# simple script to automate the steps involved in running tests

# prerequisites: chmod u+x run-all-tests.sh

clear

echo "=================="
echo "CALLING [test_quick] in 2 seconds..."
echo "=================="
sleep 2
python -m ontospy.tests.test_quick


echo ""
echo "=================="
echo "Completed."
echo "=================="
