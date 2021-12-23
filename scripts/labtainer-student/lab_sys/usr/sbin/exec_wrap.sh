#!/bin/bash
cmd=$1
trap "echo got signal" SEGV
trap "echo got signal" ILL
trap "echo got signal" SIGFPE
trap "echo got signal" SIGKILL
trap "echo got signal" SIGTERM
trap "echo \n" SIGINT
unset did_pipe
if [[ ! -z "$2" ]];then
   shift
   #echo eval $cmd $@
   eval $cmd $@
else
   #echo eval $cmd
   eval $cmd
fi
