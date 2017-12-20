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
sudo sed -i '/dnssec-validation/s/^/\/\//' /etc/bind/named.conf.options
sudo sed -i '/dnssec-validation/a   dnssec-enable no;' /etc/bind/named.conf.options
sudo tee -a /etc/bind/named.conf.default-zones << EOL
zone "ns.dnslabattacker.net" {
type master;
file "/etc/bind/db.attacker";
};
EOL
