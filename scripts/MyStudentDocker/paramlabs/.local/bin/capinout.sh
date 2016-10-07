#!/bin/bash

# capinout.sh
# Description: * Re-direct stdin and stdout to files

# Usage: capinout.sh <execprog>
# Arguments:
#     <execprog> - program to execute

if [ $# -ne 1 ]
then
    echo "Usage: capinout.sh <execprog>"
    echo "       <execprog> - program to execute"
    exit 1
fi

EXECPROG=$1
PROGNAME=`basename $EXECPROG`
#echo "Program to execute is $EXECPROG"
#echo "basename of $EXECPROG is $PROGNAME"
timestamp=$(date +"%Y%m%d%H%M%S")
stdinfile=".local/result/$PROGNAME.stdin.$timestamp"
stdoutfile=".local/result/$PROGNAME.stdout.$timestamp"

echo "stdinfile is $stdinfile"
echo "stdoutfile is $stdoutfile"

# kill the tee when the pipe consumer dies
#
#set -o pipefail

# Setup trap to handle SIGINT and SIGTERM
trap "echo exiting due to signal; echo caught SIGINT >> $stdinfile " SIGINT
trap "echo exiting due to signal; echo caught SIGTERM >> $stdinfile " SIGTERM

pipe=$(mktemp -u)
if ! mkfifo $pipe; then
   echo "ERROR: pipe create failed" >%2
   exit 1
fi

exec 3<>$pipe
rm $pipe
(echo $BASHPID >&3; tee $stdinfile) | (stdbuf -oL -eL $EXECPROG; r=$?; kill $(head -n1 <&3); exit $r) | tee $stdoutfile

#exit ${PIPESTATUS[1]}

###### Call
#####tee $stdinfile | stdbuf -oL -eL $EXECPROG | tee $stdoutfile

