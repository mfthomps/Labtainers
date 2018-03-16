#!/bin/bash

NPS_PKG_ADDITIONS="/etc/nps-apt-additions"

while read pkgaddition;
do
    echo "Adding package $pkgaddition"
    sudo /usr/local/bin/AddPackage.py $pkgaddition
done < $NPS_PKG_ADDITIONS
