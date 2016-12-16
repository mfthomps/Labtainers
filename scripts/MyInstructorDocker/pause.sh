#!/bin/bash

# Filename: pause.sh
# Description:
#     This is the pause script to be run by the instructor.
#     Note: It needs the same 'start.config' file used by start.sh.
#
#     It will perform the following tasks:
#     a. Pause the running instructor container
#        Note: instructor container name is defined in start.config
if [ "$#" -ne 1 ]; then
    echo "./start.sh <labname>"
    exit 0
fi
lab=$1

CWD=`pwd`
#echo "Current directory is $CWD"
CONFIG=${CWD}/start.config

if [ -f $CONFIG ]
then
    #echo "Config file $CONFIG exists, proceeding"
    # Read start.config
    . $CONFIG
else
    echo "Config file $CONFIG does not exist, exiting."
    exit 1
fi

#echo "Name of container is $CONTAINER_NAME"
#echo "Name of container image is $CONTAINER_IMAGE"

#echo "Pausing container $CONTAINER_NAME"
docker pause $CONTAINER_NAME
#echo "Container $CONTAINER_NAME is now paused!"

