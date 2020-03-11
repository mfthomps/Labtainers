#!/bin/bash
homedir=$1
destdir=$2
if [[ $destdir == *netmon* ]];then
    cd $homedir/$destdir
    mkdir session1
    cd session1
    unzip ../GrassMarlin/session1.gm3
    cd $homedir/$destdir
    mkdir session2
    cd session2
    unzip ../GrassMarlin/session2.gm3
fi
