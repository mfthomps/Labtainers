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
echo "nameserver 198.18.1.3" | sudo tee /etc/resolv.conf
# remove the dns route so as to not confuse student
sudo route del -host 172.17.0.1

