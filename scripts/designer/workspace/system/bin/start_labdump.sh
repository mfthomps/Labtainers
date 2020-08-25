#!/bin/bash
#
#  
#
exec 2>&1 > /var/log/start_labdump.log
SERVER=monitor_tap
PORT=1929
echo "check server"
while ! nc -z $SERVER $PORT </dev/null; do sleep 2; done
echo "back from netcat"

while [ ! -f /var/tmp/net_map.txt ]; do
    echo "no net_map yet, sleep"
    sleep 2
done

while read line; do
    echo "net_map line: $line"
    IFS=' ' read -a strarr <<< "$line"
    # ethernet interface
    br=br-${strarr[0]}
    # name of docker network
    net=${strarr[1]}
    # MAC of ethernet interface
    mac=${strarr[4]}
    ( /bin/labdump.sh $br $net $mac $SERVER $PORT & )
    echo "started for $br $net $mac $SERVER $PORT"
done </var/tmp/net_map.txt
mkdir -p /tmp/wait_tap_dir/lock
sleep infinity

