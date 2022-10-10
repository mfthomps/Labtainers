#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "newterm.sh <user ID>"
    echo "Create a new terminal on the VNC desktop."
    exit
fi
user=$1
vm=$user-labtainervm
echo "get the IP"
ip=$(./getip.sh $vm) 
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi
echo scp -i ~/.ssh/id_labtainers do_newterm.sh labtainer@$ip:/tmp/
scp -i ~/.ssh/id_labtainers -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null do_newterm.sh labtainer@$ip:/tmp/
ssh -i ~/.ssh/id_labtainers -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null labtainer@$ip /tmp/do_newterm.sh
