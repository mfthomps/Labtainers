#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "waitdone.sh <user ID>"
    exit
fi
user=$1
# start the tunnel and wait for it to die, reflecting reboot.
echo "start the tunnelx"
./checktunnel.sh $user  || exit 1
echo "wait for dead tunnel"
./wait_tunnel.sh $user || exit 1
echo "Tunnel gone, wait 20 for reboot"
sleep 20
./checktunnel.sh $user || exit 1
rm -f index.html
while :
do
    result=$(wget localhost:6901)
    if [ -f index.html ]; then
        echo "Web server is up."
        break
    fi
    sleep 20
done
echo "Labtainers is up.  Point browser to localhost:6901"
