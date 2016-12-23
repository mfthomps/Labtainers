#!/bin/bash
#
# Stop, remove and recreate a container for the given lab.
# Intended for use during testing of labs to insure a fresh
# container derived from the latest image build is used.
#
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
echo "Name of container is $CONTAINER_NAME"
./stop.sh $1
docker rm $CONTAINER_NAME
./start.sh $1
