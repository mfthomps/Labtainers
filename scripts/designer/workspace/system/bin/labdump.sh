#!/bin/bash
exec 2>&1 > /var/log/labdump_$1.log
myfifo=/tmp/dump_$1
br=$1
net=$2
server=$4
port=$5

/bin/labdump_client.py $br $net $server $port &
echo "/bin/labdump_client.py $br $net $server $port &"
echo "back from start labdump_client.py "
sleep infinity

