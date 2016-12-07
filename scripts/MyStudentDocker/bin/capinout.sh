#!/bin/bash

# capinout.sh
# Description: * Re-direct stdin and stdout to files

# Usage: capinout.sh <execprog>
# Arguments:
#     <execprog> - program to execute
pipe_sym="|"
full=$*
#echo $full
if [[ "$full" == *"$pipe_sym"* ]]; then
    #echo is pipe has $pipe_sym
    IFS='|' read -ra COMMAND_ARRAY <<< "$full"
    precommand=${COMMAND_ARRAY[0]}
    targetcommand=${COMMAND_ARRAY[1]}
    IFS=' '
    #echo "precommand is $precommand"
    #echo "target command is $targetcommand"
    TARGET_ARGS=($targetcommand)
    EXECPROG=${TARGET_ARGS[0]}
    PROGNAME=`basename ${EXECPROG}`
    len=${#TARGET_ARGS[@]}
    if [ $len -gt 1 ]; then
       PROGRAM_ARGUMENTS=${TARGET_ARGS[@]:1:$len}
    else
       PROGRAM_ARGUMENTS=""
    fi
else
    targetcommand=${full}
    TARGET_ARGS=($targetcommand)
    EXECPROG=${TARGET_ARGS[0]}
    PROGNAME=`basename $EXECPROG`
    len=${#TARGET_ARGS[@]}
    if [ $len -gt 1 ]; then
       PROGRAM_ARGUMENTS=${TARGET_ARGS[@]:1:$len}
    else
       PROGRAM_ARGUMENTS=""
    fi
fi

#echo "EXECPROG is ($EXECPROG)"
#echo "PROGNAME is ($PROGNAME)"
#echo "PROGRAM_ARGUMENTS is ($PROGRAM_ARGUMENTS)"
#echo "Program to execute is $EXECPROG"
#echo "basename of $EXECPROG is $PROGNAME"
timestamp=$(date +"%Y%m%d%H%M%S")
stdinfile="$HOME/.local/result/$PROGNAME.stdin.$timestamp"
stdoutfile="$HOME/.local/result/$PROGNAME.stdout.$timestamp"

# Store programs arguments into stdinfile
echo "PROGRAM_ARGUMENTS is ($PROGRAM_ARGUMENTS)" >> $stdinfile

#echo "stdinfile is $stdinfile"
#echo "stdoutfile is $stdoutfile"

# If file $HOME/.local/bin/checklocal.sh exist, run it
if [ -f $HOME/.local/bin/checklocal.sh ]
then
    checklocaloutfile="$HOME/.local/result/checklocal.stdout.$timestamp"
    $HOME/.local/bin/checklocal.sh $checklocaloutfile
fi

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
if [ -z "$precommand" ]; then
   (echo $BASHPID >&3; tee -a $stdinfile) | (funbuffer -p $EXECPROG $PROGRAM_ARGUMENTS; r=$?; kill $(head -n1 <&3); exit $r) | tee $stdoutfile
else
    #echo "precommand before is $precommand"
    (echo $BASHPID >&3; eval $precommand | tee -a $stdinfile) | ($EXECPROG $PROGRAM_ARGUMENTS; r=$?; exit $r) | tee $stdoutfile
fi

TEE_PID=$(ps | grep [t]ee | awk '{print $1}')
if [ ! -z "$TEE_PID" ]; then
    kill $TEE_PID
fi


#exit ${PIPESTATUS[1]}

###### Call
#####tee -a $stdinfile | stdbuf -oL -eL $EXECPROG $PROGRAM_ARGUMENTS | tee $stdoutfile

