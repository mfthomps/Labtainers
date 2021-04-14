#!/bin/bash
#
# Create a distribution for lab designers
# Expects a directory at /media/sf_SEED into which it
# will copy the distribution tar.
if [[ -z $myshare ]]; then
    myshare=/media/sf_SEED/
fi
here=`pwd`
branch=$(git rev-parse --abbrev-ref HEAD)
cd ../
git archive $branch --prefix $branch -o distrib/labtainer-master.tar
cp distrib/labtainer-master.tar $myshare/
cd $here
