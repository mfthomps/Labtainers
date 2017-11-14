#!/bin/bash
IPTABLES=/sbin/iptables

#start and flush
$IPTABLES -F
$IPTABLES -t nat -F
$IPTABLES -X
$IPTABLES -P FORWARD DROP
$IPTABLES -P INPUT   DROP
$IPTABLES -P OUTPUT  ACCEPT

#Established
$IPTABLES -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$IPTABLES -A OUTPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT
#SSH traffic
$IPTABLES -A INPUT -p tcp --dport 22 -j ACCEPT
#HTTP traffic
$IPTABLES -A INPUT -p tcp --dport 80 -j ACCEPT

#loopback
iptables -A INPUT -i lo -p all -j ACCEPT

