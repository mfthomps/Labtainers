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
source ./set_reg.sh
if [[ "$1" != -f ]]; then
   echo "This will build the labtainer network image.  "
   echo "Confirm that the labtainer.base has been published."
   echo "registry is $LABTAINER_REGISTRY"
   read -p "Continue? (y/n)"
   if [[ ! $REPLY =~ ^[Yy]$ ]]
   then
       echo exiting
       exit
   fi
else
   echo "registry is $LABTAINER_REGISTRY"
fi
here=`pwd`
cd ../
docker build --build-arg registry=$LABTAINER_REGISTRY -f base_dockerfiles/Dockerfile.labtainer.network -t labtainer.network:latest .
cd $here
