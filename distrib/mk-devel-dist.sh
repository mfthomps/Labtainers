#!/bin/bash
#myshare=/home/mike/sf_SEED/
myshare=/media/sf_SEED/
here=`pwd`
cd ../
svn status | grep -E "^M|^D|^A" | less
ddir=/tmp/labtainer-distrib
ldir=/tmp/labtainer-distrib/labtainer
rm -fr /$ddir
mkdir $ddir
mkdir $ldir
cd $ldir
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk
sed -i "s/mm\/dd\/yyyy/$(date '+%m\/%d\/%Y %H:%M')/" trunk/README
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
llist=$(ls)
for lab in $llist; do
        cd $lab
        if [[ -d docs ]]; then
            cd docs
            cp -p /tmp/labtainer_pdf/$lab/*.pdf .
            if [[ -f Makefile ]]; then
                make
            else
                doc=$lab.docx
                if [[ -f $doc ]]; then
                    soffice --convert-to pdf $doc --headless
                fi
            fi
            cp -p *pdf /tmp/labtainer_pdf/$lab/
            cd ../
        fi
        cd ../
done
cd $ddir
tar -cz -X $here/skip-labs -f $here/labtainer-developer.tar labtainer
cd $here
cp labtainer-developer.tar $myshare
