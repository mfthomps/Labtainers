#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
echo "nameserver 203.0.113.1" | sudo tee /etc/resolv.conf
# remove the dns route so as to not confuse student
sudo route del -host 172.17.0.1

# no predicting docker network assignments, use ifconfig fu
#
# Set up NAT on gateway
#
lan1=$(ifconfig | grep -B1 "inet addr:192.168.0.1" | awk '$1!="inet" && $1!="--" {print $1}')
wan=$(ifconfig | grep -B1 "inet addr:203.0.113.1" | awk '$1!="inet" && $1!="--" {print $1}')
sudo iptables --table nat -I POSTROUTING 1 --out-interface $wan -j MASQUERADE
sudo iptables --append FORWARD --in-interface $lan1 -j ACCEPT
sudo iptables -t nat -A PREROUTING -i $wan -p udp --dport 53 -j DNAT --to-destination 192.168.0.10
sudo iptables -t nat -A POSTROUTING -o $lan1 -p udp --dport 53 -d 192.168.0.10 -j SNAT --to-source 192.168.0.1
sudo /etc/init.d/dnsmasq restart
