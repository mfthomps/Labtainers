#!/bin/bash
here=`pwd`
cd $LABTAINER_DIR/distrib
./refresh_branch.py -r -q
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
./mkall.sh -q
result=$?
if [[ $result != 0 ]]; then
    echo "mkall failed"
    exit 1
fi
cd $LABTAINER_DIR/testsets/bin
./test-ubuntu16.sh
./test-ubuntu18.sh
