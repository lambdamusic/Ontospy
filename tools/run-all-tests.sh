#!/bin/bash

# simple script to run all tests, see docs/pages/tests.md

# prerequisites: chmod u+x run-all-tests.sh
# requires: pip install pytest

pytest "$@"
