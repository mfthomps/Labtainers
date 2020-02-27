#!/bin/bash
#
#  
#
SERVER=monitor_tap
PORT=1929
while ! nc -z $SERVER $PORT </dev/null; do sleep 2; done

while read line; do
    echo "$line"
    IFS=' ' read -a strarr <<< "$line"
    br=br-${strarr[0]}
    net=${strarr[1]}
    ( /bin/labdump.sh $br $net $SERVER $PORT & )
done </var/tmp/net_map.txt
sleep infinity

