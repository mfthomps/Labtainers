#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
# Use gateway as the name server
#
echo "nameserver 198.18.1.3" | sudo tee /etc/resolv.conf
sudo /usr/bin/set_default_gw.sh 198.18.1.INNER_LAN1
# remove the dns route so as to not confuse student
sudo route del -host 172.17.0.1
