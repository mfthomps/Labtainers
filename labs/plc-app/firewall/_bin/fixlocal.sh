#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
sudo chown admin:admin /etc/firewall.config
sudo chown admin:admin /etc/firewall_whitelist.txt
sudo chown admin:admin /etc/firewall_filter.txt
sudo systemctl enable firewall
sudo systemctl start firewall
