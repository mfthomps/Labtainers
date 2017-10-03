#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
echo "172.17.0.2    verydodgy.com" | sudo tee --append /etc/hosts
