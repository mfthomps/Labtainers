#
# Invoke the command in $1 using the capinout.sh script, 
# but only if it is not a system command
#
preexec() { 
   #echo "just typed $1"; 
   if [[ "$1" == "exit" ]]; then
       return 0
   fi
   stringarray=($1)
   cmd_path=`which ${stringarray[0]}`
   if [[ ! -z $cmd_path ]] && [[ "$cmd_path" != /usr/* ]] && [[ "$cmd_path" != /bin/* ]]; then
       #echo "would do this command"
       capinout.sh $1
       return 1
   fi
   return 0
}

