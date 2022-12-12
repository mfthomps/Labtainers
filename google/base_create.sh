#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
cp cloud_init.template cloud_init.txt
gcloud compute instances create $vm_name --image-family=ubuntu-1804-lts \
   --image-project=ubuntu-os-cloud \
   --metadata-from-file=user-data=cloud_init.txt
sleep 2
gcloud compute ssh labtainer@$vm_name --command='echo "VM created, wait for reboot"' || exit
cp ~/.ssh/google_compute_engine ~/.ssh/id_labtainers
cp ~/.ssh/google_compute_engine.pub ~/.ssh/id_labtainers.pub
./waitdone.sh $user_id
