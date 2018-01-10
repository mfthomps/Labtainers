#!/bin/bash
#
# If root, loop forever in login. 
#
id | grep root >>/dev/null
result=$?
if [[ $result -eq 0 ]]; then
    #echo "is root"
    while [ 1 ]; do
        trap login SIGINT
        /sbin/login
    done
fi
