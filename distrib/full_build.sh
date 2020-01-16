#!/bin/bash
#
# Perform all build steps needed to run tests, then start smoketests.
# NOTE: this script assumes local repo is up to date and what you want tested
#
here=`pwd`

./mkall.sh -q
result=$?
if [[ $result != 0 ]]; then
    echo "mkall failed"
    exit 1
fi
#
# The temp dirs align with those created by mkall.sh
# Use those same files
#
ddir=/tmp/labtainer-distrib
ldir=$ddir/labtainer
ltrunk=$ldir/trunk

export LABTAINER_DIR=$ltrunk
branch=$(git rev-parse --abbrev-ref HEAD)
#
# Archive from git is not a repo, thus git commands will not work to get branch.  
# So set in the env
#
export LABTAINER_BRANCH=$branch
cd $LABTAINER_DIR/distrib
# force current branch regsitry to match premaster
./refresh_branch.py -q
result=$?
if [[ $result != 0 ]]; then
    echo "refresh_branch failed"
    exit 1
fi
cd $LABTAINER_DIR/scripts/designer/bin
./mkbases.py
result=$?
if [[ $result != 0 ]]; then
    echo "mkbases failed"
    exit 1
fi
cd $LABTAINER_DIR/distrib
./publish.py -q
result=$?
if [[ $result != 0 ]]; then
    echo "publish failed"
    exit 1
fi
cd $LABTAINER_DIR/testsets/bin
./test-ubuntu16.sh
./test-ubuntu18.sh
