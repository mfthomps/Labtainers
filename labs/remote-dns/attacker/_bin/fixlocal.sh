#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo tee -a /etc/bind/named.conf.local << EOL
zone "example.com" {
type master;
file "/etc/bind/example.com.db";
};
EOL
echo "nameserver 203.0.113.10" | sudo tee /etc/resolv.conf

