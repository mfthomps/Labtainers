#!/bin/bash
#
#  This example IPTABLES firewall will only allow all traffic.
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
$IPTABLES -P FORWARD ACCEPT
$IPTABLES -P INPUT   ACCEPT
$IPTABLES -P OUTPUT  ACCEPT


