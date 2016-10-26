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

if [ $# -ne 1 ]
then
    echo "Usage: parameterize.sh <LAB_SEED>"
    echo "       <LAB_SEED> -- laboratory seed"
    exit 1
fi

LAB_SEED=$1

# call ParameterParser.py (passing $LAB_SEED)
sudo .local/bin/ParameterParser.py $LAB_SEED

# If file .local/bin/fixlocal.sh exist, run it
if [ -f .local/bin/fixlocal.sh ]
then
    .local/bin/fixlocal.sh
fi

