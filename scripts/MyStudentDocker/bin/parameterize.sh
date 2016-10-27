#!/usr/bin/env bash

# parameterize.sh
#
# Usage: parameterize.sh <LAB_INSTANCE_SEED>
# Arguments:
#     <LAB_INSTANCE_SEED> -- laboratory instance seed
# 
# Description:
# 1. Call ParameterParser.py (passing $LAB_INSTANCE_SEED)
# 2. If file .local/bin/fixlocal.sh exist, run it

#echo "Parameterizing laboratory"

# Configuration variables
LAB_SEEDFILE="/home/ubuntu/.seed"
LAB_PARAMCONFIGFILE="/home/ubuntu/.local/config/parameter.config"

# Do not display instruction during parameterization
LOCKDIR=/tmp/.mylockdir
mkdir "$LOCKDIR" >/dev/null 2>&1

#echo "number of argument is $#"
#echo "argument is $@"

if [ $# -ne 1 ]
then
    echo "Usage: parameterize.sh <LAB_INSTANCE_SEED>"
    echo "       <LAB_INSTANCE_SEED> -- laboratory instance seed"
    exit 1
fi

LAB_INSTANCE_SEED=$1

# Laboratory instance seed is always store in $LAB_SEEDFILE
echo "$LAB_INSTANCE_SEED" > $LAB_SEEDFILE

# call ParameterParser.py (passing $LAB_INSTANCE_SEED)
sudo /home/ubuntu/.local/bin/ParameterParser.py $LAB_INSTANCE_SEED $LAB_PARAMCONFIGFILE

# If file /home/ubuntu/.local/bin/fixlocal.sh exist, run it
if [ -f /home/ubuntu/.local/bin/fixlocal.sh ]
then
    /home/ubuntu/.local/bin/fixlocal.sh
fi

rmdir $LOCKDIR

