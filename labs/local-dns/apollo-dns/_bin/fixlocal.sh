#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo sed -i '/directory/a  dump-file "/var/cache/bind/dump.db";\nforwarders {\n127.0.0.11;\n};\nquery-source port 33333;' /etc/bind/named.conf.options
echo include \"/etc/bind/example.conf\"; | sudo tee -a /etc/bind/named.conf.local
sudo chown bind:bind /var/cache/bind/*
sudo /etc/init.d/bind9 restart

