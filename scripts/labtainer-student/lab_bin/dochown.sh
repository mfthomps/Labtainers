#!/bin/bash
#
#  chown -R takes forever in Docker, something about a cow.
#
mychown(){
   dir=$1
   user=$2
   flist=$(find $dir ! -user $2)
   for f in $flist; do
       chown $user:$user $f
   done
}
user=$1
mychown /home/$user $user
mychown /usr root
