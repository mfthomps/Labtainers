#!/bin/bash

# Filename: stop.sh
# Description:
#     This is the stop script to be run by the instructor.
#     Note: It needs the same 'start.config' file used by start.sh.
#
#     It will perform the following tasks:
#     a. Copy grades.txt file from '/home/ubuntu' to 'Shared' folder
#     b. stop the instructor container
#        Note: instructor container name is defined in start.config

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

# Check existence of HOST_HOME_SEED directory - create if necessary
if [ ! -d $HOST_HOME_SEED ]
then
    echo "Directory $HOST_HOME_SEED does not exist, creating it"
    mkdir -p $HOST_HOME_SEED
fi

##### ***** start pre-stop commands ****
# This is where "pre-stop" commands should be run for each lab

# Here are samples including performing 'sudo sysctl' type of command
#echo "arguments: $*" > /tmp/test.stop
#echo "environment:" >> /tmp/test.stop
#env | grep LXC >> /tmp/test.stop
#
#echo "Before systcl" >> /tmp/test.stop
#
#sudo sysctl -w kernel.randomize_va_space=0
#
#echo "After systcl" >> /tmp/test.stop
##### ***** end pre-stop commands ****

# Copy grades.txt from '/home/ubuntu' to 'Shared' folder
docker cp $CONTAINER_NAME:/home/$CONTAINER_USER/grades.txt $HOST_HOME_SEED/
# Change ownership to defined user $USER
sudo chown $USER:$USER $HOST_HOME_SEED/grades.txt

#echo "Stopping container $CONTAINER_NAME"
docker stop $CONTAINER_NAME
#echo "Container $CONTAINER_NAME is now stopped!"

