#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo chown -R bob:bob /shared_data/bob
sudo chown -R alice:alice /shared_data/alice
echo umask 007 | sudo tee -a /home/bob/.bashrc
echo umask 007 | sudo tee -a /home/alice/.bashrc
sudo setfacl -m "u:harry:rw" /shared_data/accounting.txt
sudo setfacl -m "u:alice:r" /shared_data/accounting.txt

