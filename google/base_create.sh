#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "create_vm.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
#rm -f ~/.ssh/id_labtainers*
#ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_labtainers -q -N ""
#key=$(cat ~/.ssh/id_labtainers.pub)
#echo "key generated"
#sed 's|REPLACE_WITH_KEY|$key|' cloud_init.template > cloud_init.txt
cp cloud_init.template cloud_init.txt
gcloud compute instances create $vm_name --image-family=ubuntu-1804-lts \
   --image-project=ubuntu-os-cloud --zone=us-west1-a \
   --metadata-from-file=user-data=cloud_init.txt
gcloud compute ssh labtainer@$vm_name --command='echo "VM created, wait for reboot"'
cp ~/.ssh/google_compute_engine ~/.ssh/id_labtainers
cp ~/.ssh/google_compute_engine.pub ~/.ssh/id_labtainers.pub
./waitdone.sh $user_id
