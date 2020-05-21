hasnew=$(docker images | grep labtainers/labtainer.base)
if [[ -z $hasnew ]];then
    echo "nope"
    $LABTAINER_DIR/setup_scripts/pull-all.py
else
    echo "has it $hasnew"
fi
