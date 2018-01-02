#!/bin/bash
done=0
while ! ping -c 1 -w 2 "$1" &>/dev/null; do
   echo nope
   sleep 1
done
echo done

