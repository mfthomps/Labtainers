#!/bin/bash
echo "in delete_vm"
if [ "$#" -ne 1 ]; then
    echo "checktunnel.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
az vm delete --yes -g labtainerResources -n $vm
