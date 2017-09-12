#!/usr/bin/env bash

# fixlocal.sh
#
# Usage: fixlocal.sh
# 
# Description:
#     This file should contain specific fixes that are needed
#     for each lab containers
#
# For buffer overflow containers for the student:

# 1. Remove /bin/sh (default is soft-linked to /bin/dash)
sudo rm -f /bin/sh

# 2. Re-create /bin/sh (soft-linked to /bin/zsh instead)
sudo ln -s /bin/zsh /bin/sh

cd $HOME
./compile.sh
