#!/bin/bash
#
# Invoked by a testvm .profile within a gnome terminal
#
export LABTAINER_DIR=$HOME/labtainer/trunk
# next line altered by sed
export LABTAINER_BRANCH=REPLACE_THIS
scriptpath=$(realpath $0)
vmtestdir=$(dirname "${scriptpath}")
echo "vmtestdir is $vmtestdir" >> /tmp/dothis.log
cd $HOME
tar -xf /media/sf_SEED/labtainer.tar labtainer/trunk/setup_scripts/full-smoke-test.sh
cd $LABTAINER_DIR/setup_scripts
./full-smoke-test.sh 
result=$?
echo "Back from full-smoke-test result $result for $vmtestdir" >> /tmp/dothis.log
if [[ $result == 0 ]]; then
    echo "PASS" > $vmtestdir/result.txt
else
    echo "FAIL" > $vmtestdir/result.txt
fi
