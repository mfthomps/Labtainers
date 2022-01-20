#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "waitup.sh <user ID>"
    exit
fi
user_id=$1
vm_name=$user_id-labtainervm
ip=$(./getip.sh $vm_name) || exit 1
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi
echo -n "Waiting for ssh port to open on $vm_name..."
while true; do
    result=$(echo > /dev/tcp/$ip/22 && echo "Open")
    if [[ "$result" == *"Open"* ]]; then
        echo "ssh port is now open"
        break
    fi
    echo -n "."
    sleep 2
done
