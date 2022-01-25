#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "get_disk_id.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
osDiskId=$(az vm show \
   -g labtainerResources \
   -n $vm \
   --query "storageProfile.osDisk.managedDisk.id" \
   -o tsv)

dbase=$(basename $osDiskId)
echo $dbase
