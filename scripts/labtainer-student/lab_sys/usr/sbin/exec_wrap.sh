#!/bin/bash
cmd=$1
trap "echo got signal" SEGV
trap "echo got signal" ILL
trap "echo got signal" SIGFPE
if [[ ! -z "$2" ]];then
   shift
   #echo eval $cmd $@
   eval $cmd $@
else
   #echo eval $cmd
   eval $cmd
fi
