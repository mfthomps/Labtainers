#!/bin/bash
#
# Perform all build steps needed to run tests, then start smoketests.
# NOTE: this script assumes pulls from github.
#
here=`pwd`
branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$branch" == "master" ]]; then
    echo "Do not full_build as the master branch."
    exit 1
fi
git pull || exit 1
./mkall.sh -q
result=$?
if [[ $result != 0 ]]; then
    echo "mkall failed"
    exit 1
fi
#
# Clone local repo -- TBD do all building from same instance?
#
ddir=/tmp/labtainer-distrib
ldir=$ddir/labtainer
rm -fr $ldir
ltrunk=$ldir/trunk
mkdir -p $ltrunk
here=`pwd`
cd ../
git clone --single-branch --branch $branch $LABTAINER_DIR $ltrunk

#
# switch LABTAINER_DIR to new copy of repo
#
export LABTAINER_DIR=$ltrunk
#
#
cd $LABTAINER_DIR/distrib
# force current branch regsitry to match premaster
if [[ $branch != 'premaster' ]]; then
    echo "Refresh the branch registry"
    ./refresh_branch.py -q
    result=$?
    if [[ $result != 0 ]]; then
        echo "refresh_branch failed"
        exit 1
    fi
fi
#cd $LABTAINER_DIR/scripts/designer/bin
#echo "running mkbases from $LABTAINER_DIR"
#./mkbases.py 
#result=$?
#if [[ $result != 0 ]]; then
#    echo "mkbases failed"
#    exit 1
#fi
cd $LABTAINER_DIR/distrib
echo "Now rebuild lab images as needed and publish to branch registry"
./publish.py -q
result=$?
if [[ $result != 0 ]]; then
    echo "publish failed"
    exit 1
fi
cd $LABTAINER_DIR/testsets/bin
./testVMs.sh
#./test-ubuntu16.sh
#./test-ubuntu18.sh
