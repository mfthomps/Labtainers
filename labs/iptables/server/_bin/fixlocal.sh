#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
sudo systemctl enable httpserver.service
sudo systemctl start httpserver.service

