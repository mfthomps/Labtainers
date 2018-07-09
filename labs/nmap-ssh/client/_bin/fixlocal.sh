#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
sudo systemctl enable telnetbot 
sudo systemctl start telnetbot 
sudo systemctl enable webbot 
sudo systemctl start webbot 
