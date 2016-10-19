#!/usr/bin/env bash

# createseedlocalfix.sh
#
# Usage: createseedlocalfix.sh <ROOT_SEED> <USER_SEED>
# Arguments:
#     <ROOT_SEED> -- seed for /root/.seed
#     <USER_SEED> -- seed for /home/ubuntu/.seed
# 
# Description:
# 1. Create /root/.seed and /home/ubuntu/.seed
# 2. If file .local/bin/fixlocal.sh exist, run it

#echo "Creating seed"

if [ $# -ne 2 ]
then
    echo "Usage: createseedlocalfix.sh <ROOT_SEED> <USER_SEED>"
    echo "       <ROOT_SEED> -- seed for /root/.seed"
    echo "       <USER_SEED> -- seed for /home/ubuntu/.seed"
    exit 1
fi

ROOTSEED=$1
USERSEED=$2

# use sudo to ensure removal
sudo rm -f /tmp/seedfile.tmp

echo $ROOTSEED > /tmp/seedfile.tmp
# need sudo here
sudo cp /tmp/seedfile.tmp /root/.seed
success=$?
if [ $success -ne 0 ]
then
    echo "ERROR: Fail to create root seed."
fi

echo $USERSEED > /tmp/seedfile.tmp
cp /tmp/seedfile.tmp /home/ubuntu/.seed
success=$?
if [ $success -ne 0 ]
then
    echo "ERROR: Fail to create user seed."
fi

# use sudo to ensure removal
sudo rm -f /tmp/seedfile.tmp

# If file .local/bin/fixlocal.sh exist, run it
if [ -f .local/bin/fixlocal.sh ]
then
    .local/bin/fixlocal.sh
fi

