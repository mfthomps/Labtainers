#!/bin/bash

# Filename: stop.sh
# Description:
#     This is the stop script to be run by the student.
#     Note: It needs the same 'start.config' file used by start.sh.
#
#     It will perform the following tasks:
#     a. Run 'Student.py' (This will create zip file of the result)
#     b. Copy zip files from '/home/ubuntu' to 'Shared' folder
#     c. stop the student container
#        Note: student container name is defined in start.config
if [ "$#" -ne 1 ]; then
    echo "./stop.sh <labname>"
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

# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
if [ ! -d /home/$USER/$HOST_HOME_XFER ]
then
    echo "Directory /home/$USER/$HOST_HOME_XFER does not exist, creating it"
    mkdir -p /home/$USER/$HOST_HOME_XFER
fi

##### ***** start pre-stop commands ****
# This is where "pre-stop" commands should be run for each lab

# Run 'Student.py'
# This will create zip file of the result
docker exec -it $CONTAINER_NAME script -q -c "/bin/bash -c 'cd ; . .profile ; Student.py'" /dev/null

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

# Copy zip files from '/home/$USER/' to 'Shared' folder
zip_filelist=`docker exec -it $CONTAINER_NAME cat /home/$CONTAINER_USER/.local/zip.flist`
for fname in $zip_filelist;
do
    echo "cp $CONTAINER_NAME:$fname"
    docker cp $CONTAINER_NAME:$fname /home/$USER/$HOST_HOME_XFER/
done
# Change ownership to defined user $USER
sudo chown $USER:$USER /home/$USER/$HOST_HOME_XFER/*.zip

# Inform user where results are stored
echo "Results stored in directory: /home/$USER/$HOST_HOME_XFER "

#echo "Stopping container $CONTAINER_NAME"
docker stop $CONTAINER_NAME
#echo "Container $CONTAINER_NAME is now stopped!"

