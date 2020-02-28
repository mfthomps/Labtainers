#!/bin/bash
exec 2>&1 > /var/log/labdump_$1.log
myfifo=/tmp/dump_$1
#    ( /bin/labdump.sh $br $net $mac $SERVER $PORT & )
br=$1
net=$2
mac=$3
server=$4
port=$5

/bin/labdump_client.py $br $net $mac $server $port &
echo "/bin/labdump_client.py $br $net $mac $server $port &"
echo "back from start labdump_client.py "
sleep infinity

