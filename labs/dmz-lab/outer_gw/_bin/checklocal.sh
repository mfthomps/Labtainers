#!/bin/bash
#
#  TBD, move the guts of cmd retrieval logic to an /sbin script
#  and invoke it as a function?
#
the_path=$1
the_mode=$2
the_user=$3
if [[ "$the_path" == /sbin/iptables ]];then
    #
    # begin the function
    # use most recent bash history for to find the command
    # would return cmd and root
    #
    root=NO
    if [ ! -f /root/.bash_history ] || [ /home/$the_user/.bash_history -nt /root/.bash_history ]; then
        cmd=$(tail -n1 /home/$the_user/.bash_history)
        if [[ "$cmd" == sudo* ]]; then
            root=YES
        fi
    else
        cmd=$(tail -n1 /root/.bash_history)
        root=YES
    fi
    #
    # end of function
    #
    if [[ $root == YES ]]; then
        if [[ "$cmd" == *-A* ]]; then
            echo "$cmd"
        fi
    fi 
fi
