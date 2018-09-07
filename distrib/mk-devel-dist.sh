#!/bin/bash
#
# Create a distribution for lab designers
# Expects a directory at /media/sf_SEED into which it
# will copy the distribution tar.
#
revision=`git describe --long`
myshare=/media/sf_SEED/
here=`pwd`
cd ../
rootdir=`pwd`
git status -s | grep -E "^ M|^ D|^ A" | less
ddir=/tmp/labtainer-distrib
ldir=$ddir/labtainer
ltrunk=$ldir/trunk
scripts=$ltrunk/scripts
labs=$ltrunk/labs
rm -fr /$ddir
mkdir $ddir
mkdir $ldir
mkdir $ltrunk
mkdir $labs
$here/fix-git-dates.py ./ $ltrunk
cd $ltrunk
sed -i "s/mm\/dd\/yyyy/$(date '+%m\/%d\/%Y %H:%M')/" README.md
sed -i "s/^Revision:/Revision: $revision/" README.md
cp setup_scripts/install-labtainer.sh .
cp setup_scripts/update-labtainer.sh .
cd $ldir/trunk/docs/labdesigner
make
cp labdesigner.pdf ../../../
cp labdesigner.pdf $myshare

cd $ldir/trunk/docs/student
make
cp labtainer-student.pdf ../../../
cp labtainer-student.pdf $myshare

cd $ldir/trunk/docs/instructor
make
cp labtainer-instructor.pdf ../../../
cp labtainer-instructor.pdf $myshare
$here/mkTars.sh $ldir/trunk/labs $here/skip-labs
cd $ldir/trunk/labs
mkdir -p /tmp/labtainer_pdf
cd $rootdir
distrib/mk-lab-pdf.sh $labs
cd $ddir
tar -cz -X $here/skip-labs -f $here/labtainer-developer.tar labtainer
cd /tmp/
zip -r $here/labtainer_pdf.zip labtainer_pdf
cd $here
cp labtainer-developer.tar $myshare
cp labtainer_pdf.zip $myshare
