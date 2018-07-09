#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
cd $HOME
./build.sh
sudo systemctl enable svchost
sudo systemctl start svchost
