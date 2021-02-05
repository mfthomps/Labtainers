hasnew=$(docker images | grep labtainers/labtainer.base)
if [[ -z $hasnew ]];then
    #echo "nope"
    $LABTAINER_DIR/setup_scripts/pull-all.py
fi
hascommit=$(grep "^Commit:" labtainer/trunk/README.md)
hasgit=$(grep "github.*releases" labtainer/update-labtainer.sh)
if [ -z "$hascommit" ] || [ -z "$hasgit" ]; then
    cd labtainer
    wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/labtainer.tar -O labtainer.tar
    sync
    cd ..
    tar xf labtainer/labtainer.tar --keep-newer-files --warning=none
fi
here=`pwd`
rm -fr labtainer/trunk/setup-scripts
cd labtainer/trunk/scripts/labtainer-student/bin
if [ ! -L update-designer.sh ]; then
    ln -s ../../../setup_scripts/update-designer.sh
fi
cd $here
grep "^Distribution created:" labtainer/trunk/README.md | awk '{print "Updated to release of: ", $3, $4}'
grep "^Branch:" labtainer/trunk/README.md | awk '{print "branch: ", $2}'
grep "^Revision:" labtainer/trunk/README.md | awk '{print "Revision: ", $2}'
grep "^Commit:" labtainer/trunk/README.md | awk '{print "Commit: ", $2}'
