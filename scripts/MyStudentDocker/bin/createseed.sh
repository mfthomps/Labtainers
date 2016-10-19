#!/usr/bin/env bash

# createseed.sh
#
# Usage: createseed.sh <ROOT_SEED> <USER_SEED>
# Arguments:
#     <ROOT_SEED> -- seed for /root/.seed
#     <USER_SEED> -- seed for /home/ubuntu/.seed
# 
# Description: Create /root/.seed and /home/ubuntu/.seed

#echo "Creating seed"

if [ $# -ne 2 ]
then
    echo "Usage: createseed.sh <ROOT_SEED> <USER_SEED>"
    echo "       <ROOT_SEED> -- seed for /root/.seed"
    echo "       <USER_SEED> -- seed for /home/ubuntu/.seed"
    exit 1
fi

ROOTSEED=$1
USERSEED=$1

# use sudo to ensure removal
sudo rm -f /tmp/seedfile.tmp

echo $ROOTSEED > /tmp/seedfile.tmp
# need sudo here
sudo cp /tmp/seedfile.tmp /root/.seed

echo $USERSEED > /tmp/seedfile.tmp
cp /tmp/seedfile.tmp /home/ubuntu/.seed

# use sudo to ensure removal
sudo rm -f /tmp/seedfile.tmp
