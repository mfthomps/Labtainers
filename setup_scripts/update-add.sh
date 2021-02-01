hasnew=$(docker images | grep labtainers/labtainer.base)
if [[ -z $hasnew ]];then
    #echo "nope"
    $LABTAINER_DIR/setup_scripts/pull-all.py
fi
hascommit=$(grep "^Commit:" labtainer/trunk/README.md)
hasgit=$(grep "github" labtainer/update-labtainer.sh)
if [[ -z "$hascommit" ] || [ -z "$hasgit" ]]; then
    cd labtainer
    wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/labtainer.tar -O labtainer.tar
    sync
    cd ..
    tar xf labtainer/labtainer.tar --keep-newer-files --warning=none
fi
