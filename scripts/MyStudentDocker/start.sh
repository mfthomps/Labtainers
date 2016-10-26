#!/bin/bash

# Filename: start.sh
# Description:
#     This is the start script to be run by the student.
#     Note: It needs 'start.config' file.
#
#     It will perform the following tasks:
#     a. check to see if student container has been created or not
#        Note: student container name is defined in start.config
#        a.1. If it has not been created, create using docker run
#        a.2. If it has been created, start it using docker start
#        a.3. If first run (i.e., container is created the first time)
#             prompt user for e-mail address and generate seed files
#             by calling createseedlocalfix.sh
#     b. Spawn a terminal with startup instruction and
#        another terminal for the student

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

# Check existence of /home/$USER/$HOST_HOME_SEED directory - create if necessary
if [ ! -d /home/$USER/$HOST_HOME_SEED ]
then
    echo "Directory /home/$USER/$HOST_HOME_SEED does not exist, creating it"
    mkdir -p /home/$USER/$HOST_HOME_SEED
fi

##### ***** start pre-start commands ****
# This is where "pre-start" commands should be run for each lab

# Currently there are no specific tasks to do (for format string lab)
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

# Check to see if $CONTAINER_NAME container has been created or not
docker inspect -f {{.Created}} $CONTAINER_NAME &> /dev/null
result=$?
#echo "initial inspect result is $result"

# Set need_seeds=0 first
need_seeds=0
if [ $result -eq $FAILURE ]
then
    #echo "Container $CONTAINER_NAME does not exist yet, call docker run"
    #docker run -dt --name=$CONTAINER_NAME $CONTAINER_IMAGE bash
    docker run -dt --privileged --name=$CONTAINER_NAME $CONTAINER_IMAGE bash
    # Give the container some time -- just in case
    sleep 3
    need_seeds=1
fi

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
    if [ $need_seeds -eq 1 ]
    then
        # Prompt user for e-mail address
        echo "Please enter your e-mail address: "
        read user_email
        # Create hash using LAB_SECRET concatenated with user's e-mail
        # LAB_SECRET is per laboratory - specified in start.config
        rm -f /tmp/hashfile.tmp
        #echo "$LAB_SECRET:$user_email"
        echo "$LAB_SECRET:$user_email" > /tmp/hashfile.tmp
        LAB_SEED=`md5sum /tmp/hashfile.tmp | awk '{ print $1 }'`
        #echo "About to call parameterize.sh with LAB_SEED = ($LAB_SEED)"
        rm -f /tmp/hashfile.tmp
        docker exec -it $CONTAINER_NAME script -q -c "/home/ubuntu/.local/bin/parameterize.sh $LAB_SEED" /dev/null
        result=$?
        if [ $result -eq $FAILURE ]
        then
            echo "ERROR: Failed to parameterize lab"
            exit 1
        fi
    fi
fi

# Start a terminal and a shell in the container
gnome-terminal -x docker exec -it $CONTAINER_NAME bash -l &
gnome-terminal -x docker exec -it $CONTAINER_NAME bash -l &

