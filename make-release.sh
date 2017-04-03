#!/bin/bash

# simple script to automate the steps involved in releasing ontospy in PiPy

# prerequisites: chmod u+x release.sh

clear

echo "=================="
echo "Starting..."
echo "=================="

rm -r dist/;

echo "=================="
echo "..building"
echo "=================="

python setup.py sdist

python setup.py bdist_wheel --universal

echo "=================="
echo "Distribution built"
echo "=================="


echo "=================="
echo "..uploading"
echo "=================="

twine upload dist/*

echo "=================="
echo "Completed."
echo "=================="

