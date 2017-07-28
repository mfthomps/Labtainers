: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
treatlocal(){
   local cmd_path=$1
   local TAS=/home/ubuntu/.local/bin/treataslocal
   if [ -f $TAS ]
   then
       # Get the list of commands from treataslocal
       while read cmdlocal; do
           if [[ "$cmd_path" == "$cmdlocal" ]]; then
               return 1
           else
               continue
           fi
       done <$TAS
    fi
    return 0
}
ignorelocal(){
   local cmd_path=$1
   local TAS=/home/ubuntu/.local/bin/ignorelocal
   if [ -f $TAS ]
   then
       # Get the list of commands from ignorelocal
       while read cmdlocal; do
           if [[ "$cmd_path" == "$cmdlocal" ]]; then
               return 1
           else
               continue
           fi
       done <$TAS
    fi
    return 0
}
#
# Invoke the command in $1 using the capinout.sh script, 
# but only if it is not a system command.  Checks the
# ~/.local/bin/treataslocal for exceptions.
# If the command includes a pipe, look at both sides of the pipe.
# Ignore sudo, and treats target command as the command.
#
preexec() {
   #echo "just typed $1";
   if [[ "$1" == "exit" ]]; then
       return 0
   fi
   IFS='|' read -ra commandarray <<< "$1"
   #echo "command array: $commandarray"
   IFS=' '
   for command in "${commandarray[@]}";do
       stringarray=($command)
       if [ ${stringarray[0]} == "sudo" ]; then
          cmd_path=`which ${stringarray[1]}`
       else
          cmd_path=`which ${stringarray[0]}`
       fi
       treatlocal $cmd_path
       result=$?
       if [ $result == 1 ]; then
           capinout.sh "$1"
           return 1
       fi
       ignorelocal $cmd_path
       result=$?
       if [ $result == 1 ]; then
           return 0
       fi
       if [[ ! -z $cmd_path ]] && [[ "$cmd_path" != /usr/* ]] && \
          [[ "$cmd_path" != /bin/* ]] && [[ "$cmd_path" != /sbin/* ]]; then
           #echo "would do this command $1"
           capinout.sh "$1"
           return 1
       fi
   done
   return 0
}

