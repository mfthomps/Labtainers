#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "wait_tunnel.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
echo -n "Waiting for vm $vm to provision and reboot..."
while : 
do
    result=$(ps aux | grep ssh | grep 6901)
    if [ -z "${result}" ]; then
        echo "gone"
        exit
    else
        echo -n "."
        sleep 20
    fi
done
