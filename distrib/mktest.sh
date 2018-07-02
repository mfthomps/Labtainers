#!/bin/bash
tmp_dir=/tmp/labtainer_tests
rm -fr $tmp_dir
mkdir $tmp_dir
cd ../
svn status testsets | less
cd $tmp_dir
mkdir trunk
cd trunk
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/testsets
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/distrib
cd ../
svn export https://tor.ern.nps.edu/svn/proj/labtainer/simlab
tar czf /tmp/labtainer-tests.tar trunk simlab
mv /tmp/labtainer-tests.tar /media/sf_SEED/
