#!/bin/bash

echo "NPS cron jobs"
NPS_PKG_ADDITIONS="/etc/nps-apt-additions"

# Update CentOS repo
sudo /usr/local/bin/UpdateCentosRepo.sh

# Update Ubuntu repo - only main and restricted
sudo /usr/local/bin/apt-mirror

# Update Ubuntu dists hierarchy - include universe and multiverse
sudo /usr/local/bin/CheckHierarchy.sh

while read pkgaddition;
do
    echo "Adding package $pkgaddition"
    sudo /usr/local/bin/AddPackage.py $pkgaddition
done < $NPS_PKG_ADDITIONS

exit 0
