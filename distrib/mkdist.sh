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
revision=`git describe --long`
skip="skip-labs"
skiplist=""
lines=`cat $skip`
for line in $lines; do
    lab=$(basename $line)
    skiplist+=($lab)
done
mkdir -p /tmp/labtainer_pdf
#myshare=/home/mike/sf_SEED/
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
git archive master README.md | tar -x -C $ltrunk
sed -i "s/mm\/dd\/yyyy/$(date '+%m\/%d\/%Y %H:%M')/" $ltrunk/README.md
sed -i "s/^Revision:/Revision: $revision/" $ltrunk/README.md
git archive master config | tar -x -C $ltrunk
git archive master setup_scripts | tar -x -C $ltrunk
git archive master docs | tar -x -C $ltrunk
git archive master tool-src | tar -x -C $ltrunk
git archive master distrib/skip-labs | tar -x -C $ltrunk
mkdir $scripts
git archive master scripts/labtainer-student | tar -x -C $ltrunk
git archive master scripts/labtainer-instructor | tar -x -C $ltrunk
mkdir $labs
llist=$(git ls-files labs | cut -d '/' -f 2 | uniq)
for lab in $llist; do
    if [ $(contains "${skiplist[@]}" $lab) != "y" ]; then
        git archive master labs/$lab/config | tar -x -C $ltrunk
        git archive master labs/$lab/instr_config | tar -x -C $ltrunk
        if [[ -d labs/$lab/docs ]]; then
            git archive master labs/$lab/docs | tar -x -C $ltrunk
        fi
    fi
done
distrib/mk-lab-pdf.sh $labs
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
pwd
./mkit.sh
cd $ddir
tar -cz -X $here/skip-labs -f $here/labtainer.tar labtainer
cd /tmp/
#tar -czf $here/labtainer_pdf.tar.gz labtainer_pdf
zip -r $here/labtainer_pdf.zip labtainer_pdf
cd $here
cp labtainer.tar $myshare
cp labtainer_pdf.zip $myshare
