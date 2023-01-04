#!/bin/bash
vm=$1
zone=$(./findzone.sh)
result=$(gcloud compute instances describe $vm --zone=$zone --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
if [ -z "${result}" ]; then
    echo "FAIL"
else
    echo $result
    echo $result > myip.txt
fi
