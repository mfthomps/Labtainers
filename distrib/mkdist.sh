#!/bin/bash
function contains() {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
            echo "y"
            return 0
        fi
    }
    echo "n"
    return 1
}
revision=`svn info --show-item revision`
skip="skip-labs"
skiplist=""
lines=`cat $skip`
for line in $lines; do
    lab=$(basename $line)
    hack=$lab/
    skiplist+=($hack)
    #echo "added $hack"
done
mkdir -p /tmp/labtainer_pdf
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
mkdir trunk
cd trunk
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/README.md
sed -i "s/mm\/dd\/yyyy/$(date '+%m\/%d\/%Y %H:%M')/" README.md
sed -i "s/^Revision:/Revision: $revision/" README.md
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/config
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/setup_scripts
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/docs
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/tool-src
mkdir scripts
cd scripts
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/scripts/labtainer-student
svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/scripts/labtainer-instructor
cd ../
mkdir labs
cd labs
llist=$(svn ls https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs)
for lab in $llist; do
    if [ $(contains "${skiplist[@]}" $lab) != "y" ]; then
        mkdir $lab
        cd $lab
        mkdir -p /tmp/labtainer_pdf/$lab
        svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs/$lab/config
        svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs/$lab/instr_config
        svn export https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs/$lab/docs
        if [[ -d docs ]]; then
            echo "lab is $lab"
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
        else
            cp */instructions.txt /tmp/labtainer_pdf/$lab/
        fi
        cd ../
    fi
done
cd $ldir
mv trunk/setup_scripts/install-labtainer.sh .
ln -s trunk/setup_scripts/update-labtainer.sh .
ln -s trunk/setup_scripts/update-designer.sh .

cd $ldir/trunk/docs/student
make
cp labtainer-student.pdf ../../../
cp labtainer-student.pdf $myshare

cd $ldir/trunk/docs/instructor
make
cp labtainer-instructor.pdf ../../../
cp labtainer-instructor.pdf $myshare

cd $ldir/trunk/tool-src/capinout
./mkit.sh
cd $ddir
tar -cz -X $here/skip-labs -f $here/labtainer.tar labtainer
cd /tmp/
tar -czf $here/labtainer_pdf.tar labtainer_pdf
cd $here
cp labtainer.tar $myshare
cp labtainer_pdf.tar $myshare
