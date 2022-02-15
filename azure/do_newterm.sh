#!/bin/bash
con=$(echo labtainer | sudo -S docker ps | grep entry | awk '{print $1}')
echo "con is $con"
echo labtainer | sudo -S docker exec $con /bin/bash -c 'export LABTAINER_DIR=/home/labtainer/labtainer/trunk;/home/labtainer/.doterm.sh'
