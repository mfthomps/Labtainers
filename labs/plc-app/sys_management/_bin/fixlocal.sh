#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
cd $HOME
./build.sh
# unblock the waitparam.service, which is a predicate for svchost
PERMLOCKDIR=/var/labtainer/did_param
sudo mkdir -p "$PERMLOCKDIR"
sudo systemctl enable svchost
sudo systemctl start svchost
