#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "delete_disk.sh <user ID>"
    exit
fi
user_id=$1
disk=$user_id-labtainervm-disk
az disk delete --yes -g labtainerResources -n $disk 
