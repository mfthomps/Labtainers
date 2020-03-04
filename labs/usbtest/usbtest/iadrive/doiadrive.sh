#!/bin/bash
sdir=`dirname $0`
exec 2>&1 > /tmp/iadrive.log
export LD_LIBRARY_PATH=$sdir
$sdir/iadrive -c $sdir/iadrive.cfg $@

