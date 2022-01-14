#!/bin/bash
resource=$1
vm=$2
result=$(az vm show -d -g $resource -n $vm --query publicIps -o tsv) 
if [ -z "${result}" ]; then
    echo "FAIL"
else
    echo $result
    echo $result > myip.txt
fi
