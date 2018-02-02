#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
if [[ "${TEST_REGISTRY}" != YES ]]; then
    export LABTAINER_REGISTRY="mfthomps"
    docker login
else
    export LABTAINER_REGISTRY="testregistry:5000"
fi
echo "Using registry $LABTAINER_REGISTRY"
image=$1
docker tag $image $LABTAINER_REGISTRY/$image
docker push $LABTAINER_REGISTRY/$image

