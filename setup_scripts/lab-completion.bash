#/usr/bin/env bash
#
#  Tab completion for Labtainers
#  source this script 
#  e.g., "source lab-completion.bash"
#  or put it into /etc/bashcompletion.d
#
# Get list of labtainer labs
#
lablist=$($LABTAINER_DIR/scripts/labtainer-student/bin/start.py -l)
# replace newlines with spaces
lablist="${lablist//$'\n'/ }"
# tell bash to use this list for tab completion of the "labtainer" command.
complete -W "$lablist" labtainer


ldir=~/labtainer_xfer
mkdir -p $ldir
lablist=$(ls $ldir)
# replace newlines with spaces
lablist="${lablist//$'\n'/ }"
complete -W "$lablist" gradelab

ldir=$LABTAINER_DIR/labpacks
packlist=$(ls $ldir)
list=""
for p in $packlist; do
    list="$list ${p%%.*}"
done
complete -W "$list" labpack
