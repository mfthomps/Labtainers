if [ "$1" == -t ] || [ "$2" == -t ]; then
    export LABTAINER_REGISTRY="testregistry:5000"
else
    if [[ "${TEST_REGISTRY}" != YES ]]; then
        export LABTAINER_REGISTRY="mfthomps"
    else
        export LABTAINER_REGISTRY="testregistry:5000"
    fi
fi

