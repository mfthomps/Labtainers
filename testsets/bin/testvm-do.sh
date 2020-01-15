#!/bin/bash
#
# Invoked by a testvm .profile within a gnome terminal
#
export LABTAINER_DIR=$HOME/labtainer/trunk
vmtestdir=$(realpath $0)
cd $HOME
tar -xf /media/sf_SEED/labtainer.tar labtainer/trunk/setup_scripts/full-smoke-test.sh
cd $LABTAINER_DIR/setup_scripts
./full-smoke-test.sh 
result=$?
if [[ $result == 0 ]]; then
    echo "PASS" > $vmtestdir/result.txt
else
    echo "FAIL" > $vmtestdir/result.txt
fi
