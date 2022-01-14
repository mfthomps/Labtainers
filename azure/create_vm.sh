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
rm -f ~/.ssh/id_labtainers*
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_labtainers -q -N ""
key=$(cat ~/.ssh/id_labtainers.pub)
echo "key generated"
sed  "s|REPLACE_WITH_KEY|$key|" cloud_init.template > cloud_init.txt 
./resourcecheck.sh
echo "Creating Azure VM $vm_name for $user_id"
az vm create \
 --resource-group labtainerResources \
 --name $vm_name \
 --admin-username labtainer \
 --image UbuntuLTS \
 --ssh-key-value "~/.ssh/id_labtainers.pub" \
 --generate-ssh-keys \
 --custom-data cloud_init.txt > $user_id.json

./waitdone.sh $user_id
