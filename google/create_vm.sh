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
zone=$(./findzone.sh)
gcloud compute instances create $vm_name --image=https://www.googleapis.com/compute/v1/projects/labtainers/global/images/labtainervm5 \
   --metadata-from-file=user-data=user_config.txt
gcloud compute disks resize $vm_name --size 30G --zone=$zone -q
# instances fail ssh until settled
./waitup.sh $user_id 2>/dev/null
echo "Check keys"
gcloud compute ssh labtainer@$vm_name --command="echo VM booted"
cp ~/.ssh/google_compute_engine ~/.ssh/id_labtainers
cp ~/.ssh/google_compute_engine.pub ~/.ssh/id_labtainers.pub
./waitdone.sh $user_id
