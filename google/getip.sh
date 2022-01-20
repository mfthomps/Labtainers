#!/bin/bash
vm=$1
result=$(gcloud compute instances describe $vm --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
if [ -z "${result}" ]; then
    echo "FAIL"
else
    echo $result
    echo $result > myip.txt
fi
