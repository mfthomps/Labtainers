
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "generalize.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
ip=$(./getip.sh labtainerResources $vm) 
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi
ssh -i "~/.ssh/id_labtainers" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null labtainer@$ip "sudo waagent -deprovision"
./deallocate_vm.sh $user
az vm generalize --resource-group labtainerResources --name $vm
