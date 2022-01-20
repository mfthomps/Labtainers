#!/bin/bash
#
#  Create a Labtainers VM using the public Labtainers VM 
#
if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
gcloud compute instances create $vm_name --image=https://www.googleapis.com/compute/v1/projects/labtainers/global/images/labtainervm \
   --metadata-from-file=user-data=user_config.txt
# instances fail ssh until settled
./waitup.sh $user_id 2>/dev/null
echo "Do ssh to ensure keys"
gcloud compute ssh labtainer@$vm_name --command="echo VM booted"
cp ~/.ssh/google_compute_engine ~/.ssh/id_labtainers
cp ~/.ssh/google_compute_engine.pub ~/.ssh/id_labtainers.pub
./waitdone.sh $user_id
