#!/bin/bash

# Filename: unpause.sh
# Description:
#     This is the unpause script to be run by the student.
#     Note: It needs the same 'start.config' file used by start.sh.
#
#     It will perform the following tasks:
#     a. Unpause a paused student container
#        Note: student container name is defined in start.config

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

#echo "Unpausing container $CONTAINER_NAME"
docker unpause $CONTAINER_NAME
#echo "Container $CONTAINER_NAME is now unpaused!"

