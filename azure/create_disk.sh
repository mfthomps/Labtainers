#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "create_disk.sh <user ID>"
    exit
fi
user=$1
disk=$2
az disk create -g labtainerResources -n $disk --source https://labtainersblob.blob.core.windows.net/labtainersblobcontainer/labtainersbase.vhd
