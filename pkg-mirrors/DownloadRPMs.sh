#!/bin/bash

NPS_RPM_ADDITIONS="/etc/nps-rpm-additions"

while read rpmaddition;
do
    echo "Downloading RPM $rpmaddition"
    sudo wget $rpmaddition
done < $NPS_RPM_ADDITIONS
