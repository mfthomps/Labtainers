#!/usr/bin/env bash

# startup.sh
# Arguments: None
#
# Usage: startup.sh
# 
# Description: Concatenate instructions.txt file and pipe to less
instructions="$HOME"/instructions.txt
if [ -f $instructions ]; then
   LOCKDIR=/tmp/.mylockdir
   if mkdir "$LOCKDIR" >/dev/null 2>&1; then
       echo "Starting startup.sh"
       cat $instructions | less
   fi
fi
