#
# Invoke the command in $1 using the capinout.sh script, 
# but only if it is not a system command.
# If the command includes a pipe, look at both sides of the pipe.
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
       cmd_path=`which ${stringarray[0]}`
       if [[ ! -z $cmd_path ]] && [[ "$cmd_path" != /usr/* ]] && \
          [[ "$cmd_path" != /bin/* ]] && [[ "$cmd_path" != /sbin/* ]]; then
           #echo "would do this command $1"
           capinout.sh "$1"
           return 1
       fi
   done
   return 0
}

