#!/bin/bash
#
# inotify callback
#
the_path=$1
the_mode=$2
the_user=$3
the_cmd=$4
if [[ $the_mode == CREATE ]]; then
    # due to file creation show diretory acl
    getfacl -d $the_path
else
    # file access, show file acl
    getfacl $the_path
fi
