#!/bin/bash

# simple script to automate the steps involved in releasing ontospy in PiPy

# prerequisites: chmod u+x run-make-release.sh
# requires: pip install build twine

clear

# the build includes whatever is in the working folder, so refuse to build
# if there are uncommitted or untracked files in the package
if [ -n "$(git status --porcelain -- ontospy setup.py requirements.txt MANIFEST.in)" ]; then
    echo "ERROR: uncommitted or untracked files would end up in the release:"
    git status --porcelain -- ontospy setup.py requirements.txt MANIFEST.in
    exit 1
fi

echo "=================="
echo "Starting..."
echo "=================="

rm -rf dist/ build/ ontospy-*/

echo "=================="
echo "..building"
echo "=================="

python -m build || exit 1
twine check dist/* || exit 1

echo "=================="
echo "Distribution built"
echo "=================="
ls dist/

# setuptools deletes its sdist staging folder (eg ontospy-2.2/) after the build, but
# inside Dropbox parts of it can survive, so remove what's left
rm -rf ontospy-*/

echo "=================="
echo "..uploading"
echo "=================="

twine upload dist/*

echo "=================="
echo "Completed."
echo "=================="
