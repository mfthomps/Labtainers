#!/bin/bash
#
# Create a distribution for lab designers
# Expects a directory at /media/sf_SEED into which it
# will copy the distribution tar.
#
skip_pdf="NO"
if [[ "$1" == "-s" ]]; then
    echo "Skip PDF creation"
    skip_pdf="YES"
fi
revision=`git describe --always`
if [[ -z $myshare ]]; then
    myshare=/media/sf_SEED/
fi
here=`pwd`
cd ../
rootdir=`pwd`
ddir=$(mktemp -d -t labtainer-distrib-XXXXXXXX)
ldir=$ddir/labtainer
ltrunk=$ldir/trunk
scripts=$ltrunk/scripts
labs=$ltrunk/labs
docs=$ltrunk/docs
rm -fr /$ddir
mkdir $ddir
mkdir $ldir
mkdir $ltrunk
mkdir $labs
branch=$(git rev-parse --abbrev-ref HEAD)
$here/fix-git-dates.py ./ $ltrunk $branch
cd $ltrunk
sed -i "s/mm\/dd\/yyyy/$(date '+%m\/%d\/%Y %H:%M')/" README.md
sed -i "s/^Revision:/Revision: $revision/" README.md
sed -i "s/^Branch:/Branch: $branch/" README.md
cp setup_scripts/install-labtainer.sh .
cp setup_scripts/update-labtainer.sh .
if [[ $skip_pdf != "YES" ]]; then
    $here/mkTars.sh $ldir/trunk/labs $here/skip-labs
    cd $ldir/trunk/labs
    mkdir -p /tmp/labtainer_pdf
    cd $rootdir
    distrib/mk-lab-pdf.sh $labs
fi
cd $ldir/trunk/tool-src/capinout
pwd
./mkit.sh &> /tmp/mkit_$USER.out
# put student and instructor guide at top of distribution.
cp $docs/student/labtainer-student.pdf $ldir/
cp $docs/instructor/labtainer-instructor.pdf $ldir/
cp $docs/labdesigner/labdesigner.pdf $ldir/
cd $ddir
tar -cz -X $here/skip-labs -f $here/labtainer-developer.tar labtainer
cd $here
cp labtainer-developer.tar $myshare
if [[ $skip_pdf != "YES" ]]; then
    cd /tmp/
    zip -r $here/labtainer_pdf.zip labtainer_pdf
    cd $here
    cp labtainer_pdf.zip $myshare
fi
if [[ "$1" == "-r" ]]; then
    cp labtainer-developer.tar release/
fi
