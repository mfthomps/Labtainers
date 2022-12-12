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
cp cloud_init.template cloud_init.txt
./resourcecheck.sh || exit 1
imgdef="/CommunityGalleries/LabtainersImages-fb345820-6f7a-4fbf-b106-7d50e3b601f2/Images/labtainersImageDefinition/Versions/latest"
echo "Creating Azure VM $vm_name for $user_id"
az vm create \
 --resource-group labtainerResources \
 --name $vm_name \
 --image $imgdef \
 --size Standard_B2s \
 --admin-username labtainer \
 --generate-ssh-keys \
 --verbose \
 --accept-term \
 --ssh-key-values ~/.ssh/id_labtainers.pub 

./waitdone.sh $user_id
