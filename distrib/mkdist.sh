#!/bin/bash
#
#  Create an end-user distribution of Labtainers.
#  This uses git archive, basing the distribution on committed content of the local repo.
#
#
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
revision=`git describe --always`
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
branch=$(git rev-parse --abbrev-ref HEAD)
registry=$(scripts/labtainer-student/bin/registry.py)
echo "Make distribution from branch: $branch  registry: $registry"
git archive $branch README.md | tar -x -C $ltrunk
git archive $branch | tar -x -C $ltrunk
sed -i "s/mm\/dd\/yyyy/$(date '+%m\/%d\/%Y %H:%M')/" $ltrunk/README.md
sed -i "s/^Revision:/Revision: $revision/" $ltrunk/README.md
sed -i "s/^Branch:/Branch: $branch/" $ltrunk/README.md
#git archive master config | tar -x -C $ltrunk
$here/fix-git-dates.py config $ltrunk $branch
$here/fix-git-dates.py setup_scripts $ltrunk $branch
$here/fix-git-dates.py docs $ltrunk $branch
$here/fix-git-dates.py tool-src $ltrunk $branch
$here/fix-git-dates.py distrib/skip-labs $ltrunk $branch
mkdir $scripts
$here/fix-git-dates.py scripts/labtainer-student $ltrunk $branch
$here/fix-git-dates.py scripts/labtainer-instructor $ltrunk $branch
mkdir $labs
llist=$(git ls-files labs | cut -d '/' -f 2 | uniq)
for lab in $llist; do
    if [ $(contains "${skiplist[@]}" $lab) != "y" ]; then
        $here/fix-git-dates.py labs/$lab/config $ltrunk $branch
        $here/fix-git-dates.py labs/$lab/instr_config $ltrunk $branch
        if [[ -d labs/$lab/docs ]]; then
            $here/fix-git-dates.py labs/$lab/docs $ltrunk $branch
        fi
        if [[ -d labs/$lab/bin ]]; then
            $here/fix-git-dates.py labs/$lab/bin $ltrunk $branch
        fi
    fi
done
distrib/mk-lab-pdf.sh $labs &> /tmp/mk-lab-pdf.log
result=$?
echo "result of mk-lab-pdf is $result"
if [ $result -ne 0 ]; then
    echo "Trouble making lab manuals"
    exit
fi
cd $ldir
#
#  NOTE the test_registry is changed if not on master branch
#
if [[ "$branch" != "master" ]]; then
    sed -i "s/TEST_REGISTRY.*$/TEST_REGISTRY $registry/" trunk/config/labtainer.config 
fi
mv trunk/setup_scripts/install-labtainer.sh .
ln -s trunk/setup_scripts/update-labtainer.sh .
ln -s trunk/setup_scripts/update-designer.sh .

cd $ldir/trunk/docs/student
make &> /tmp/mkstudent.out
cp labtainer-student.pdf ../../../
cp labtainer-student.pdf $myshare

cd $ldir/trunk/docs/instructor
make &> /tmp/mkins.out
cp labtainer-instructor.pdf ../../../
cp labtainer-instructor.pdf $myshare

cd $ldir/trunk/tool-src/capinout
pwd
./mkit.sh &> /tmp/mkit.out
cd $ddir
tar -cz -X $here/skip-labs -f $here/labtainer.tar labtainer
cd /tmp/
#tar -czf $here/labtainer_pdf.tar.gz labtainer_pdf
zip -qq -r $here/labtainer_pdf.zip labtainer_pdf
cd $here
cp labtainer.tar $myshare
cp labtainer_pdf.zip $myshare
echo "DONE"
