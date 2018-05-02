#!/bin/bash
cmd=$1
if [[ ! -z "$2" ]];then
   shift
   #echo eval $cmd $@
   eval $cmd $@
else
   #echo eval $cmd
   eval $cmd
fi
