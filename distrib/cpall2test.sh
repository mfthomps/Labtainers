#!/bin/bash
#
#  copy the labtainer distribution tars to all the test vm directories
#  Intended for ad-hoc testing.  Normally, copy done as part of per-vm test suite
#
tlist="labtainer.tar labtainer-developer.tar labtainer-tests.tar"
dlist=$(ls /media/sf_SEED/test_vms)
for d in $dlist; do
    for t in $tlist; do
        cp /media/sf_SEED/$t /media/sf_SEED/test_vms/$d/
    done
done
