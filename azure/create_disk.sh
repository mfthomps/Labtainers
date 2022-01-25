#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "create_disk.sh <disk name>"
    exit
fi
disk=$1
az disk create -g labtainerResources -n $disk --source https://labtainersblob.blob.core.windows.net/labtainersblobcontainer/labtainersbase.vhd --output none
