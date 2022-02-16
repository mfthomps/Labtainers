#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "newterm.sh <user ID>"
    echo "Create a new terminal on the VNC desktop."
    exit
fi
user=$1
vm=$user-labtainervm
echo "get the IP"
ip=$(./getip.sh labtainerResources $vm) 
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi
scp do_newterm.sh labtainer@$ip:/tmp/
ssh labtainer@$ip /tmp/do_newterm.sh
