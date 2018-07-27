#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
sudo chown ubuntu:ubuntu /etc/proxy.config
sudo chown ubuntu:ubuntu /etc/proxy_whitelist.txt
sudo chown ubuntu:ubuntu /etc/proxy_filter.txt
sudo systemctl enable proxy
sudo systemctl start proxy
