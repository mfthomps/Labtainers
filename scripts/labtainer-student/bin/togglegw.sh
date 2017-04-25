#!/usr/bin/env bash

# togglegw.sh
# Arguments: container | host
#
# Usage: togglegw.sh container | host
# 
# Description: Toggle the default gateway

container_gw="$HOME"/.local/.container_gateway
host_gw="$HOME"/.local/.host_gateway

if [ "$#" -ne 1 ]; then
    echo "USAGE: togglegw.sh container | host"
    exit 1
fi
gateway=$1
if [ "$gateway" == "container" ]; then
    echo "Setting default gateway container's gateway"
    if [ -f $container_gw ]; then
        #echo "Container gateway file exists"
        #echo "Delete any default gateway first"
        route delete default
        default_gw=`cat $container_gw`
        #echo "About to run command: route add default gw $default_gw"
        route add default gw $default_gw
    else
        echo "ERROR: Container gateway file does not exists"
        exit 1
    fi
elif [ "$gateway" == "host" ]; then
    echo "Setting default gateway host's gateway"
    if [ -f $host_gw ]; then
        #echo "Host gateway file exists"
        #echo "Delete any default gateway first"
        route delete default
        default_gw=`cat $host_gw`
        #echo "About to run command: route add default gw $default_gw"
        route add default gw $default_gw
    else
        echo "ERROR: Host gateway file does not exists"
        exit 1
    fi
else
    echo "USAGE: togglegw.sh container | host"
    exit 1
fi

#echo "Container's default gateway is now set!"

