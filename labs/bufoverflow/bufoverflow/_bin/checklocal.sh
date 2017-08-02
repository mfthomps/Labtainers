#!/usr/bin/env bash

# checklocal.sh
# Description:
#     This file should contain checks for local settings (such as sysctl)
#     specific for each lab.  The resulting output will go into the
#     checklocal.stdout.timestamp file
#
# Get status of kernel.randomize_va_space
sudo sysctl -a | grep kernel.randomize_va_space
