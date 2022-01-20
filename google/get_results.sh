#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "get_results.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
echo "Retrieving Labtainer results from $vm"
mkdir -p ~/labtainer_xfer
ip=$(./getip.sh $vm) 
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi
scp -i "~/.ssh/id_labtainers" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r labtainer@$ip:~/headless-labtainers/labtainer_xfer/* ~/labtainer_xfer/
echo "Results stored in $HOME/labtainer_xfer"

