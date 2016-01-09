#!/bin/bash

echo "##################"
echo "#Testing database#"
echo "##################"
echo ""
python2 -m unittest discover -s "./dbapi" -p "*_test.py"


