#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
#
# no predicting docker network assignments, use ifconfig fu
#
# Set up NAT on gateway
#
lan1=$(ifconfig | grep -B1 "inet addr:192.168.1.10" | awk '$1!="inet" && $1!="--" {print $1}')
lan2=$(ifconfig | grep -B1 "inet addr:192.168.2.10" | awk '$1!="inet" && $1!="--" {print $1}')
wan=$(ifconfig | grep -B1 "inet addr:192.170.0.10" | awk '$1!="inet" && $1!="--" {print $1}')
#iptables --flush
#iptables -t nat --flush
#iptables --delete-chain
#iptables -t nat --delete-chain
sudo iptables --table nat -I POSTROUTING 1 --out-interface $wan -j MASQUERADE
sudo iptables --append FORWARD --in-interface $lan1 -j ACCEPT
sudo iptables --append FORWARD --in-interface $lan2 -j ACCEPT

