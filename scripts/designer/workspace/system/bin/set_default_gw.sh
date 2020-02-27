#!/bin/bash
#
# Define a default route for the container.
# Saves original default route, and hardcodes
# route to my_host.
#
labvar=/var/run/labtainers
mkdir -p $labvar
my_host_ip=$(grep my_host /etc/hosts | awk '{print $1}')
host_default_gw=$(route -n | grep "^0.0.0.0" | awk '{print $2}')
#echo myip is $my_host_ip
#echo mygw is $host_default_gw
if [ ! -f $labvar/host_gw ]; then
    echo $host_default_gw > $labvar/host_gw
fi
echo $1 > $labvar/container_gw
route add -host $my_host_ip gw $host_default_gw
route delete default
route add default gw $1

