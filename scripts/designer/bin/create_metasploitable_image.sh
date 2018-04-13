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
if [[ "$1" != -f ]]; then
   echo "This will build the labtainer base image.  It is suggested that all "
   echo "other images be purged, e.g., rm -fr /var/lib/docker. "
   read -p "Continue? (y/n)"
   if [[ ! $REPLY =~ ^[Yy]$ ]]
   then
       echo exiting
       exit
   fi
fi
here=`pwd`
cd ../
msf=../../../bigfiles/msf.tar.gz
if [[ ! -f system/msf.tar.gz ]]; then
    if [[ ! -f $msf ]]; then
        echo "Missing labtainers/bigfiles/msf.tar.gz"
        echo "Get the 05.GB file from http://my.nps.edu/cyberciege/downloads/msf.tar.gz"
        exit
    fi
    cp -a ../../../bigfiles/msf.tar.gz system/
fi
docker build -f base_dockerfiles/Dockerfile.labtainer.metasploitable -t labtainer.metasploitable:latest .
cd $here
