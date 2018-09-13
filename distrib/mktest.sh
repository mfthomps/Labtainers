#!/bin/bash
#
# Create a distribution of the SimLab data files for 
# Labtainers regression testing.
# NOTE: The files are in a separate, private repo, and
# are not generally distributed.
# Assumes the simlab files are in ../../Labtainers-simlab/simlab
#
tmp_dir=/tmp/labtainer_tests
rm -fr $tmp_dir
mkdir $tmp_dir
trunk=$tmp_dir/trunk
mkdir $trunk
here=`pwd`
cd ../
$here/fix-git-dates.py distrib $trunk
$here/fix-git-dates.py testsets $trunk
cd ../Labtainers-simlab
git status -s | grep -E "^ M|^ D|^ A" | less
$here/fix-git-dates.py simlab $tmp_dir
#git archive master simlab | tar -x -C $tmp_dir
cd $tmp_dir
tar czf /tmp/labtainer-tests.tar trunk simlab
mv /tmp/labtainer-tests.tar /media/sf_SEED/
