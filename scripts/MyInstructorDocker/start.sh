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
if [ "$#" -ne 1 ]; then
    echo "./start.sh <labname>"
    exit 0
fi
lab=$1

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

echo "Name of container is $CONTAINER_NAME"
echo "Name of container image is $CONTAINER_IMAGE"

# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
if [ ! -d /home/$USER/$HOST_HOME_XFER ]
then
    echo "Directory /home/$USER/$HOST_HOME_XFER does not exist, creating it"
    mkdir -p /home/$USER/$HOST_HOME_XFER
fi

# Check to see if $CONTAINER_NAME container has been created or not
docker inspect -f {{.Created}} $CONTAINER_NAME &> /dev/null
result=$?
echo "initial inspect result is $result"

if [ $result -eq $FAILURE ]
then
    # get IP address of docker0
    IPADDR=`ifconfig docker0 | awk '/inet addr:/ {print $2}' | sed 's/addr://'`
    echo "Docker Host IP address is $IPADDR"
    #echo "Container $CONTAINER_NAME does not exist yet, call docker run"
    echo docker run -dt --privileged --add-host my_host:$IPADDR --name=$CONTAINER_NAME $CONTAINER_IMAGE bash
    docker run -dt --privileged --add-host my_host:$IPADDR --name=$CONTAINER_NAME $CONTAINER_IMAGE bash
    # Give the container some time -- just in case
    sleep 3
fi

echo $lab >/tmp/$lab.name
docker cp /tmp/$lab.name $CONTAINER_NAME:/home/$CONTAINER_USER/.local/.labname
##### ***** start pre-start commands ****
# This is where "pre-start" commands should be run for each lab
# Copy zip files from 'Shared' folder to 'home/$CONTAINER_USER'
ZIP_FILES=`ls /home/$USER/$HOST_HOME_XFER/*.zip`
#echo "filenames is ($ZIP_FILES)"
for fname in $ZIP_FILES; do
    #echo "name is $fname"
    base_fname=`basename $fname`
    docker cp $fname $CONTAINER_NAME:/home/$CONTAINER_USER/
    docker exec -it $CONTAINER_NAME sudo chown ubuntu:ubuntu /home/$CONTAINER_USER/$base_fname 
    # Somehow this will fail if not checked?
    success=$?
    if [ $success -ne 0 ]
    then
        echo "ERROR: Fail to change ownership for /home/$CONTAINER_USER/$base_fname"
    fi
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

