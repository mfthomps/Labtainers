#!/bin/bash
#
#  This example IPTABLES firewall will only allow SSH traffic
#  to be forwarded from 172.24.0.2.
#  NOTE: your IP addresses may vary
#
IPTABLES=/sbin/iptables

#start and flush
$IPTABLES -F
$IPTABLES -t nat -F
$IPTABLES -X
#
#  By default, do not allow any forwarding or accept any traffic
#  destined for the firewall.
#
$IPTABLES -P FORWARD DROP
$IPTABLES -P INPUT   DROP
$IPTABLES -P OUTPUT  DROP

# Allow forwarding of traffic associated with any established session 
$IPTABLES -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH traffic from 172.24.0.2
$IPTABLES -A FORWARD -p tcp -s 172.24.0.2 --dport 22 -j ACCEPT

# loopback device (internal traffic)
iptables -A INPUT -i lo -p all -j ACCEPT

# log IPTABLES filtering actions
iptables -A FORWARD -j NFLOG -m limit --limit 2/min --nflog-prefix "IPTABLES DROPPED"

