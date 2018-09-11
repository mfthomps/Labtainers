#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
chmod 0700 $HOME/.ssh
chmod 0600 $HOME/.ssh/authorized_keys
sudo chmod 0700 root/.ssh
sudo chmod 0600 root/.ssh/authorized_keys
