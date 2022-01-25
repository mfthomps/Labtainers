#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "get_headless.sh <user ID>"
    exit
fi
user=$1
vm=$user-labtainervm
ip=$(./getip.sh labtainerResources $vm) 
if [[ $ip == "FAIL" ]]; then
    echo "Failed to get ip of $vm"
    exit 1
fi

ssh -i "~/.ssh/id_labtainers" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null labtainer@$ip "mkdir headless_labtainers;cd headless_labtainers;wget -P /home/labtainer/headless-labtainers https://raw.githubusercontent.com/mfthomps/Labtainers/master/headless-lite/headless-labtainers.sh;chmod a+x /home/labtainer/headless-labtainers/headless-labtainers.sh;sudo usermod -aG docker labtainer;sudo systemctl restart headless-labtainers.service;"
