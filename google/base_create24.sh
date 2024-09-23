#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
cp cloud_init.template cloud_init.txt
gcloud compute instances create $vm_name --image-family=ubuntu-2204-lts \
   --machine-type=e2-standard-2 \
   --image-project=ubuntu-os-cloud \
   --metadata-from-file=user-data=cloud_init.txt
echo "wait 40 seconds"
sleep 40
gcloud compute ssh labtainer@$vm_name --command='echo "VM created, wait for reboot"' || exit
cp ~/.ssh/google_compute_engine ~/.ssh/id_labtainers
cp ~/.ssh/google_compute_engine.pub ~/.ssh/id_labtainers.pub
echo "Now wait until up."
./waitdone.sh $user_id
