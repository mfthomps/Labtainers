#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
# 1. Remove /bin/sh (default is soft-linked to /bin/dash)
sudo rm -f /bin/sh

# 2. Re-create /bin/sh (soft-linked to /bin/zsh instead)
sudo ln -s /bin/zsh /bin/sh
cd $HOME
gcc -g -m32 -o retlib -fno-stack-protector -z noexecstack retlib.c
sudo chown root:root retlib
sudo chmod 4755 retlib

