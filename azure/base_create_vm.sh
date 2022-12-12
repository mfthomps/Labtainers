#!/bin/bash
#
# Create base Labtainers VM in Azure and provision it.
# Assumes you have an Azure account and the CLI installed.
# This base is intended to be generalized and used as an image for an Azure 
# community gallery.
#
# This will create an ssh key pair and use it when creating the VM
#
if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
rm -f ~/.ssh/id_labtainers*
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_labtainers -q -N ""
key=$(cat ~/.ssh/id_labtainers.pub)
echo "key generated"
cp cloud_init.template cloud_init.txt
./resourcecheck.sh || exit 1
echo "Creating Azure VM $vm_name for $user_id"
az vm create \
 --public-ip-sku Standard \
 --resource-group labtainerResources \
 --name $vm_name \
 --image UbuntuLTS \
 --admin-username labtainer \
 --nic-delete-option delete \
 --generate-ssh-keys \
 --ssh-key-values ~/.ssh/id_labtainers.pub \
 --custom-data cloud_init.txt > $user_id.json

./waitdone2.sh $user_id
