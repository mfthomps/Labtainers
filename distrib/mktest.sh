#!/bin/bash
#
# Create a distribution of the SimLab data files for 
# Labtainers regression testing.
# NOTE: The files are in a separate, private repo, and
# are not generally distributed.
# Assumes the simlab files are in ../../Labtainers-simlab/simlab
#
mkdir -p /tmp/$USER
exec &> >(tee -a "/tmp/$USER/mktest.log") 2>&1
if [[ -z $myshare ]]; then
    myshare=/media/sf_SEED
fi
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
cd ../Labtainers-simlab/simlab
git pull
branch=$(git rev-parse --abbrev-ref HEAD)
echo "Make simlab distribution from branch: $branch"
cd ../
$here/fix-git-dates.py simlab $tmp_dir $branch
#git archive master simlab | tar -x -C $tmp_dir
cd $tmp_dir
tar --exclude *.zip -czf /tmp/$USER/labtainer-tests.tar trunk simlab
cp /tmp/$USER/labtainer-tests.tar $myshare
mv /tmp/$USER/labtainer-tests.tar $here/
tar --exclude expected -czf /tmp/$USER/simlab-dist.tar simlab
cp /tmp/$USER/simlab-dist.tar $myshare
mv /tmp/$USER/simlab-dist.tar $here/
