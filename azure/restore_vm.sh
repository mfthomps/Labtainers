#!/bin/bash
echo "in restore_vm.sh"
if [ "$#" -ne 1 ]; then
    echo "restore_vm.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
az vm start  -g labtainerResources -n $vm
sleep 2
./waitweb.sh $user
