#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "waitweb.sh <user ID>"
    exit
fi
user=$1
echo "start the tunnel"
./checktunnel.sh $user  || exit 1
rm -f index.html
echo -n "Waiting for remote Labtainers to become available..."
while :
do
    curl localhost:6901 --output index.html -s
    if [ -f index.html ]; then
        echo ""
        echo "Web server is up."
        break
    fi
    echo -n "."
    sleep 5
done
echo "Labtainers is up.  Point a browser to http://localhost:6901"
