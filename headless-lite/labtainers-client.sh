#!/bin/bash
if [[ -z $1 ]]; then
   echo "labtainers-client <IP>"
   exit
fi
echo "Creating tunnel to $1"
ssh -AfN -L 6901:127.0.0.1:6901 -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -o "ServerAliveInterval 60" labtainer@$1
echo "Now point your browser to http://localhost:6901/vnc.html?password= "
echo ""
echo "When done, use ./get-results.sh to retrieve your lab results into ~/labtainer_xfer."
