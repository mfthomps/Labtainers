#!/bin/bash
#
# Start the Ubuntu 16 smoke test with the results of the latest mkall
#
isrunning=$(./vbox-client.py "list runningvms")
echo "isrunning $isrunning"
ok=$(echo $isrunning | grep -c "SmokeTest")
if [[ $ok != 0 ]]; then
    echo "ERROR:  Is already running: $isrunning"
    exit 1
fi

vmdir="/media/sf_SEED/test_vms/ubuntu16smoke/"
if [[ "$1" != "-n" ]]; then 
    cp testvm-do.sh $vmdir/dothis.sh
    chmod a+x $vmdir/dothis.sh
    if [[ "$1" != "-t" ]]; then
        branch=$(git rev-parse --abbrev-ref HEAD)
        sed -i "s/REPLACE_THIS/$branch/" $vmdir/dothis.sh
    else
        sed -i "s/REPLACE_THIS/premaster/" $vmdir/dothis.sh
    fi
else
    echo "Leaving the dothis.sh file as it was."
fi
tlist="labtainer.tar labtainer-developer.tar labtainer-tests.tar"
for t in $tlist; do
    cp /media/sf_SEED/$t $vmdir
done

./vbox-client.py "startvm SmokeTest"
