#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo sed -i 's/@include common-auth/#@include common-auth/' /etc/pam.d/sshd
sudo sed -i '/@include common-auth/a session    sufficient      /lib/security/pam_radius_auth.so debug conf=/etc/pam_radius_auth.conf' /etc/pam.d/sshd
sudo sed -i '/@include common-auth/a auth       sufficient      /lib/security/pam_radius_auth.so debug' /etc/pam.d/sshd
sudo /etc/init.d/xinetd restart

me=$(hostname)
cat >> $HOME/.profile << EOL
echo "Welcome to the $me shambang PDU controller."
echo "Type 'help' to terminate your session"
EOL
