#!/bin/bash
#
#  wait until parameterization happens
#
echo "start wait" >/tmp/wait.log
PERMLOCKDIR=/var/labtainer/did_param
while [ ! -d "$PERMLOCKDIR" ]
do
   sleep 2
done
systemd-notify --ready
date >>/tmp/wait.log
