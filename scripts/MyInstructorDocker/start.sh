#!/bin/bash

# Filename: start.sh
# Description:
#     This is the start script to be run by the instructor.
#     Note: It needs 'start.config' file.
#
#     It will perform the following tasks:
#     a. check to see if instructor container has been created or not
#        Note: instructor container name is defined in start.config
#        a.1. If it has not been created, create using docker run
#        a.2. If it has been created, start it using docker start
#        a.3. Note: instructor does not need to generate seed files
#     b. Spawn a terminal with startup instruction and
#        another terminal for the instructor

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

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

# Check to see if $CONTAINER_NAME container has been created or not
docker inspect -f {{.Created}} $CONTAINER_NAME &> /dev/null
result=$?
#echo "initial inspect result is $result"

if [ $result -eq $FAILURE ]
then
    #echo "Container $CONTAINER_NAME does not exist yet, call docker run"
    docker run -dt --name=$CONTAINER_NAME $CONTAINER_IMAGE bash
    # Give the container some time -- just in case
    sleep 3
fi

##### ***** start pre-start commands ****
# This is where "pre-start" commands should be run for each lab
# Copy zip files from 'Shared' folder to 'home/$CONTAINER_USER'
ZIP_FILES=`ls $HOST_HOME_SEED/*.zip`
#echo "filenames is ($ZIP_FILES)"
for fname in $ZIP_FILES; do
    #echo "name is $fname"
    base_fname=`basename $fname`
    docker cp $fname $CONTAINER_NAME:/home/$CONTAINER_USER/
    docker exec -it $CONTAINER_NAME sudo chown ubuntu:ubuntu /home/$CONTAINER_USER/$base_fname 
done

# Here are samples including performing 'sudo sysctl' type of command
#echo "arguments: $*" > /tmp/test.start
#echo "environment:" >> /tmp/test.start
#env | grep LXC >> /tmp/test.start
#
#echo "Before systcl" >> /tmp/test.start
#
#sudo sysctl -w kernel.randomize_va_space=0
#
#echo "After systcl" >> /tmp/test.start
##### ***** end pre-start commands ****

docker inspect -f {{.Created}} $CONTAINER_NAME &> /dev/null
result=$?
#echo "inspect result is $result"
if [ $result -eq $FAILURE ]
then
    echo "ERROR: Container $CONTAINER_NAME still not starting up!"
    exit 1
else
    #echo "Container $CONTAINER_NAME already exist, call docker start"
    docker start $CONTAINER_NAME
    #echo "Container $CONTAINER_NAME is now running!"
fi

# Start a terminal and a shell in the container
gnome-terminal -x docker exec -it $CONTAINER_NAME script -q -c "/bin/bash -c 'cd ; . .profile ; exec ${SHELL:-sh}'" /dev/null &
gnome-terminal -x docker exec -it $CONTAINER_NAME script -q -c "/bin/bash -c 'cd ; . .profile ; startup.sh'" /dev/null &

