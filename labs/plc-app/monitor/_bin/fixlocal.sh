#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo systemctl enable heartbeat
# unblock the waitparam.service, which is a predicate for heartbeat
PERMLOCKDIR=/var/labtainer/did_param
sudo mkdir -p "$PERMLOCKDIR"
sudo systemctl start heartbeat
