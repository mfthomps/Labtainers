#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "stop.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
az vm stop  -g labtainerResources -n $vm
echo "VM $vm has been stopoed."
