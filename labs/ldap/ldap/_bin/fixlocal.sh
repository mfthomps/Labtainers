#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
# Reconfigure the openldap package using dpkg-reconfigure and
# debconf-set-selections.
# Then, configure the ldap server for example.com with an initial group and
# an initial user
#
echo "BASE    dc=example,dc=com" | sudo tee -a /etc/ldap/ldap.conf
echo "URI     ldap://localhost" | sudo tee -a /etc/ldap/ldap.conf
sudo /var/tmp/configure.sh
sudo systemctl restart slapd
sudo /var/tmp/addusers.sh
