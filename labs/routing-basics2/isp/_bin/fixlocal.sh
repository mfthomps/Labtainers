#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
lan1=$(ifconfig | grep -B1 "inet addr:203.113.0.1" | awk '$1!="inet" && $1!="--" {print $1}')
wan=$(ifconfig | grep -B1 "inet addr:10.10.0.1" | awk '$1!="inet" && $1!="--" {print $1}')
sudo iptables --table nat -I POSTROUTING 1 --out-interface $wan -j MASQUERADE
sudo iptables --append FORWARD --in-interface $lan1 -j ACCEPT

