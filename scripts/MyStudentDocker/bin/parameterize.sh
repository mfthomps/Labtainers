#!/usr/bin/env bash

# parameterize.sh
#
# Usage: parameterize.sh <LAB_SEED>
# Arguments:
#     <LAB_SEED> -- laboratory seed
# 
# Description:
# 1. Call ParameterParser.py (passing $LAB_SEED)
# 2. If file .local/bin/fixlocal.sh exist, run it

#echo "Creating seed"

# Do not display instruction during parameterization
LOCKDIR=/tmp/.mylockdir
mkdir "$LOCKDIR" >/dev/null 2>&1

#echo "number of argument is $#"
#echo "argument is $@"

if [ $# -ne 1 ]
then
    echo "Usage: parameterize.sh <LAB_SEED>"
    echo "       <LAB_SEED> -- laboratory seed"
    exit 1
fi

LAB_SEED=$1

# call ParameterParser.py (passing $LAB_SEED)
sudo /home/ubuntu/.local/bin/ParameterParser.py $LAB_SEED

# If file /home/ubuntu/.local/bin/fixlocal.sh exist, run it
if [ -f /home/ubuntu/.local/bin/fixlocal.sh ]
then
    /home/ubuntu/.local/bin/fixlocal.sh
fi

rmdir $LOCKDIR

