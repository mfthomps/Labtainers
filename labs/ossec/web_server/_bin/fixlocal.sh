#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo chown -R apache:apache /var/www/html
echo $1 | sudo -S sed -i 's%<server-ip>.*</server-ip>%<server-ip>172.0.0.2</server-ip>%' /var/ossec/etc/ossec.conf
# suppress kernel logging of apparmor noise from host
echo $1 | sudo -S sed -i '/^. Don.t log private.*/a :msg, !contains, "apparmor"' /etc/rsyslog.conf
echo $1 | sudo -S systemctl restart rsyslog


