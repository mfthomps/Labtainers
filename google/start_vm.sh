#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "start_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
gcloud -q compute instances start $vm_name 
./checktunnel.sh $user_id
