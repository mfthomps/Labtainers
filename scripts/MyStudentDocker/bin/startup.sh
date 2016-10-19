#!/usr/bin/env bash

# startup.sh
# Arguments: None
#
# Usage: startup.sh
# 
# Description: Concatenate instruction.txt file and pipe to less

echo "Starting startup.sh"

cat /home/ubuntu/instruction.txt | less
