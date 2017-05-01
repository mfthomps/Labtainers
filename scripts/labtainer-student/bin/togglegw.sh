#!/usr/bin/env bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END

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

