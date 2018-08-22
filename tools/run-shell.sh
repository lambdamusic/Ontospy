#!/bin/bash

# simple script to run iPython preloaded with this library
# prerequisites: chmod u+x run-shell.sh

clear

echo "=================="
echo "Opening iPython with Ontospy pre-loaded..."
echo "=================="
ipython shell_profile.py --no-simple-prompt --no-confirm-exit -i