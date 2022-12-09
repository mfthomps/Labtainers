#!/bin/bash
#
# Used to create base VM.  First waits for VM to die, reflecting that
# it has completed provisioning and has rebooted.  Then waits for
# it to come back up.
#
if [ "$#" -ne 1 ]; then
    echo "waitdone.sh <user ID>"
    exit
fi
user=$1
# start the tunnel and wait for it to die, reflecting reboot.
echo "start the tunnel"
./checktunnel.sh $user  || exit 1
./wait_tunnel.sh $user || exit 1
echo "Tunnel gone, wait 20 for reboot"
sleep 20
./checktunnel.sh $user || exit 1
./waitweb.sh $user
