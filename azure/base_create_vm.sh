#!/bin/bash
#
# Create an Azure VM for a student, assuming the user has
# an Azure account and the CLI installed.
#
# This will create an ssh key pair and use it when creating the VM
#
if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
if [ ! -f ~/.ssh/id_labtainers ]; then
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_labtainers -q -N ""
    echo "new key generated"
fi
cp cloud_init.template cloud_init.txt
./resourcecheck.sh || exit 1
echo "Creating Azure VM $vm_name for $user_id"
az vm create \
 --resource-group labtainerResources \
 --name $vm_name \
 --image UbuntuLTS \
 --admin-username labtainer \
 --generate-ssh-keys \
 --ssh-key-values ~/.ssh/id_labtainers.pub \
 --custom-data cloud_init.txt > $user_id.json

./waitdone.sh $user_id
