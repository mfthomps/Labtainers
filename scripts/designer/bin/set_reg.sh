if [ "$1" == -t ] || [ "$2" == -t ]; then
    registry=$($LABTAINER_DIR/scripts/labtainer-student/bin/registry.py)
    export LABTAINER_REGISTRY=$registry
else
    if [[ "${TEST_REGISTRY}" != YES ]]; then
        registry=$($LABTAINER_DIR/scripts/labtainer-student/bin/registry.py -d)
        export LABTAINER_REGISTRY=$registry
    else
        registry=$($LABTAINER_DIR/scripts/labtainer-student/bin/registry.py)
        export LABTAINER_REGISTRY=$registry
    fi
fi

