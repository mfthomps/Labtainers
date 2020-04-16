#!/bin/bash
#
# Create a distribution of the SimLab data files for 
# Labtainers regression testing.
# NOTE: The files are in a separate, private repo, and
# are not generally distributed.
# Assumes the simlab files are in ../../Labtainers-simlab/simlab
#
if [[ -z $myshare ]]; then
    myshare=/media/sf_SEED
fi
tmp_dir=/tmp/labtainer_tests
tmp_dir=$(mktemp -d -t labtainer_tests-XXXXXXXX)
rm -fr $tmp_dir
mkdir $tmp_dir
trunk=$tmp_dir/trunk
mkdir $trunk
here=`pwd`
cd ../
branch=$(git rev-parse --abbrev-ref HEAD)
echo "Make test set distribution from branch: $branch"
$here/fix-git-dates.py distrib $trunk $branch
$here/fix-git-dates.py testsets $trunk $branch
cd ../Labtainers-simlab
branch=$(git rev-parse --abbrev-ref HEAD)
echo "Make simlab distribution from branch: $branch"
$here/fix-git-dates.py simlab $tmp_dir $branch
#git archive master simlab | tar -x -C $tmp_dir
cd $tmp_dir
tar czf /tmp/labtainer-tests.tar trunk simlab
mv /tmp/labtainer-tests.tar $myshare
