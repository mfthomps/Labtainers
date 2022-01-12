#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "wait_tunnel.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
echo "vm is $vm"
while : 
do
    result=$(ps aux | grep ssh | grep 6901)
    if [ -z "${result}" ]; then
        echo "gone"
        exit
    else
        echo "still here"
        sleep 20
    fi
done
