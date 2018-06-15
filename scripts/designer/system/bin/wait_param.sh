#!/bin/bash
#
# wait for container to be parameterized
#
PERMLOCKDIR=/var/labtainer/did_param
while [ ! -d "$PERMLOCKDIR" ]
do
   sleep 2
done

