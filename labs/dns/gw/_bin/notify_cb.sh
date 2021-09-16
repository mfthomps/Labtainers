#!/bin/bash
#
#  Callback from an inotify event
#
the_path=$1
the_mode=$2
the_user=$3
the_cmd=$4
if [[ "$the_path" == /sbin/iptables ]];then
    #
    #  inotify says iptables ran.  Determine if it may have had an effect -- e.g.,
    #  do not break up timestamp ranges if student simply runs a sudo iptables -L 
    #
    #
    # Only care if run as root.  Make a record if consequential iptables command, or via rc.local
    #
    if [[ $the_user == root ]]; then
        if [[ "$the_cmd" == iptables* ]]; then
            if [[ "$the_cmd" == *-A* ]]; then
                echo "is root and -A $the_cmd"
            fi
        else
            # if run from script, e.g., rc.local, assume effects
            echo $the_cmd
        fi
    fi 
fi
