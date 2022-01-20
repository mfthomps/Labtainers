#!/bin/bash
echo "in checktunnel"
if [ "$#" -ne 1 ]; then
    echo "checktunnel.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
echo "get the IP"
ip=$(./getip.sh $vm) 
echo "ip is $ip"
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi
result=$(ps aux | grep ssh | grep 6901)
if [ -z "${result}" ]; then
    echo "No tunnel, create one."
    ssh -AfN -L 6901:127.0.0.1:6901 -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -o "ServerAliveInterval 60" -i "~/.ssh/id_labtainers" labtainer@$ip &
else
   if [[ "$result" == *"$ip"* ]]; then
       echo "Proper tunnel already exists."
       echo $result
   else
       echo "Tunnel exists but has has wrong IP"
       kill $(echo $result | awk '{print $2}')
       ssh -AfN -L 6901:127.0.0.1:6901 -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -o "ServerAliveInterval 60" -i "~/.ssh/id_labtainers" labtainer@$ip
   fi
fi

