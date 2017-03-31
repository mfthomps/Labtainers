#!/usr/bin/env bash

# checklocal.sh
# Description:
#     This file should contain checks for local setting (such as sysctl)
#     specific for each lab
#
# Usage: checklocal.sh <outputfile>
# Arguments:
#     <outputfile> - where to store output

if [ $# -ne 1 ]
then
    echo "Usage: checklocal.sh <outputfile>"
    echo "       <outputfile> - where to store output"
    exit 1
fi

OUTPUTFILE=$1
echo "" > $OUTPUTFILE

# Get status of kernel.randomize_va_space
sudo sysctl -a | grep kernel.randomize_va_space >> $OUTPUTFILE

