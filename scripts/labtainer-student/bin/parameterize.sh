#!/usr/bin/env bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
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
LAB_SEEDFILE="$HOME/.local/.seed"
USER_EMAILFILE="$HOME/.local/.email"
LAB_NAMEFILE="$HOME/.local/.labname"
WATERMARK_NAMEFILE="$HOME/.local/.watermark"
LAB_PARAMCONFIGFILE="$HOME/.local/config/parameter.config"

# Do not display instruction during parameterization
LOCKDIR=/tmp/.mylockdir
mkdir "$LOCKDIR" >/dev/null 2>&1

#echo "number of argument is $#"
#echo "argument is $@"

if [ $# -ne 5 ]
then
    echo "Usage: parameterize.sh <CONTAINER_USER> <LAB_INSTANCE_SEED> <USER_EMAIL> <LAB_NAME> <CONTAINER_NAME>"
    echo "       <CONTAINER_USER> -- username of the container"
    echo "       <LAB_INSTANCE_SEED> -- laboratory instance seed"
    echo "       <USER_EMAIL> -- user's e-mail"
    echo "       <LAB_NAME> -- name of the lab"
    echo "       <CONTAINER_NAME> -- name of the container"
    exit 1
fi

CONTAINER_USER=$1
LAB_INSTANCE_SEED=$2
USER_EMAIL=$3
LAB_NAME=$4
CONTAINER_NAME=$5

# Laboratory instance seed is always stored in $LAB_SEEDFILE
echo "$LAB_INSTANCE_SEED" > $LAB_SEEDFILE
# User's e-mail is always stored in $USER_EMAILFILE
echo "$USER_EMAIL" > $USER_EMAILFILE
echo "$LAB_NAME" > $LAB_NAMEFILE
echo "" > $WATERMARK_NAMEFILE

# call ParameterParser.py (passing $LAB_INSTANCE_SEED)
sudo $HOME/.local/bin/ParameterParser.py $CONTAINER_USER $LAB_INSTANCE_SEED $CONTAINER_NAME $LAB_PARAMCONFIGFILE

# If file $HOME/.local/bin/fixlocal.sh exist, run it
if [ -f $HOME/.local/bin/fixlocal.sh ]
then
    $HOME/.local/bin/fixlocal.sh 2>>/tmp/fixlocal.output
fi
$HOME/.local/bin/hookBash.sh 2>>/tmp/hookBash.output
rmdir $LOCKDIR

# Added a permanent 'did_param' lock directory
PERMLOCKDIR=/var/labtainer/did_param
sudo mkdir -p "$PERMLOCKDIR" >/dev/null 2>&1

