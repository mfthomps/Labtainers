#!/bin/bash
#
#  Copy a set of template files into a new lab directory
#
if [ -z $SEED_DIR ]; then
    echo SEED_DIR not defined
    echo "The SEED_DIR env variable should be through trunk in the svn repo path."
    exit
fi
echo "SEED_DIR is $SEED_DIR"
cp -r $SEED_DIR/scripts/designer/templates/* .
echo "Template files created."
