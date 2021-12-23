#
# update-add.sh Migrate most update function here so that changes to this this file are updated
# before the script is sourced from the update-labtainer.sh script.
#
if [ -z "$LABTAINER_DIR" ] || [ ! -d "$LABTAINER_DIR" ]; then
    export LABTAINER_DIR=/home/student/labtainer/trunk
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
$LABTAINER_DIR/setup_scripts/pull-all.py $test_flag 
here=`pwd`
rm -fr labtainer/trunk/setup-scripts
cd labtainer/trunk/scripts/labtainer-student/bin
if [ ! -L update-designer.sh ]; then
    ln -s ../../../setup_scripts/update-designer.sh
fi
if [[ "$TEST_REGISTRY" != TRUE ]]; then
    mkdir -p $LABTAINER_DIR/MakepackUI/bin
    wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/makepackui.jar -O $LABTAINER_DIR/MakepackUI/bin/makepackui.jar
fi
target=~/.bashrc
grep "lab-completion.bash" $target >>/dev/null
result=$?
if [[ result -ne 0 ]];then
   echo 'source $LABTAINER_DIR/setup_scripts/lab-completion.bash' >> $target
fi
source $LABTAINER_DIR/setup_scripts/lab-completion.bash
haspip3=$(dpkg -l python3-pip)
if [ -z "$haspipe3" ]; then
    echo "Need to install python3-pip package, will sudo apt-get"
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi
hasdocker=$(pip3 list --format=legacy | grep docker)
if [ -z "$hasdocker" ]; then
    echo "Need to install docker python module, will sudo pip3"
    sudo pip3 install docker
fi
cd $here
grep "^Distribution created:" labtainer/trunk/README.md | awk '{print "Updated to release of: ", $3, $4}'
grep "^Branch:" labtainer/trunk/README.md | awk '{print "branch: ", $2}'
grep "^Revision:" labtainer/trunk/README.md | awk '{print "Revision: ", $2}'
grep "^Commit:" labtainer/trunk/README.md | awk '{print "Commit: ", $2}'
