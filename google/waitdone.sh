#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "waitdone.sh <user ID>"
    exit
fi
user=$1
./checktunnel.sh $user || exit 1
rm -f index.html
echo "Waiting for remote Labtainers to become available.  Please be patient."
while :
do
    curl localhost:6901 --output index.html -s
    if [ -f index.html ]; then
        echo "Web server is up."
        break
    fi
    sleep 20
done
echo "Labtainers is up.  Point a browser to http://localhost:6901"
