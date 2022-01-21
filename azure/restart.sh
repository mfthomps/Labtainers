#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "restart.sh <user ID>"
    exit
fi
user=$1
./checktunnel.sh $user || exit 1
echo "Point your browser to http://localhost:6901"
