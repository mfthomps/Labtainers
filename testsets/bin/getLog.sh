#!/bin/bash
#
# Get the name of a smoketest log that is newer than the time
# at which we start looking.  Assumes this is run while a VM
# is still booting.
#
which=$1
logdir=/media/sf_SEED/smokelogs
look4=$logdir/$which*
now=$(date)
now_ts=$(date -d "${now}" "+%s")
count=0
while [[ -z $gotit ]]; do
    sleep 2
    flist=$(ls $look4)
    for f in $flist; do
        fdate=$(date -r $f)
        fdate_ts=$(date -d "${fdate}" "+%s")
        if [[ $fdate_ts -ge $now_ts ]]; then
            gotit=$f
        fi
    done
    count=$((count+1))
    if [[ $count -gt 200 ]]; then
        echo "Failure: Time out finding log file"
        exit 1
    fi
done
if [[ -z $gotit ]]; then
    echo "Failure: did not find log file"
    exit 1
else
    echo $gotit
fi
