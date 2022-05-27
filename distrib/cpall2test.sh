#!/bin/bash
#
#  copy the labtainer distribution tars to all the test vm directories
#  Intended for ad-hoc testing.  Normally, copy done as part of per-vm test suite
#
tlist="labtainer.tar labtainer-master.tar labtainer-tests.tar"
dlist=$(ls /media/sf_SEED/test_vms)
for d in $dlist; do
    mkdir -p /media/sf_SEED/test_vms/$d
    for t in $tlist; do
        cp /media/sf_SEED/$t /media/sf_SEED/test_vms/$d/
    done
done
