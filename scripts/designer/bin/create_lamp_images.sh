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
read -p "This buid will pull from the docker hub.  Have you published the centos base?"
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo exiting
    exit
fi
here=`pwd`
source ./set_reg.sh
cd ../
docker build --build-arg registry=$LABTAINER_REGISTRY -f base_dockerfiles/Dockerfile.labtainer.lamp -t labtainer.lamp:latest .
cd $here
