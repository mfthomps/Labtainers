#!/bin/bash
echo "in deallocate_vm"
if [ "$#" -ne 1 ]; then
    echo "deallocate_vm.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
az vm deallocate -g labtainerResources -n $vm
echo "VM $vm has been deallocated"
