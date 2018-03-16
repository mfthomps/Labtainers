#!/bin/bash

echo "NPS cron jobs"
NPS_PKG_ADDITIONS="/home/jkhosali/nps-apt-additions"

# Update CentOS repo
sudo /home/jkhosali/UpdateCentosRepo.sh

# Update Ubuntu repo - only main and restricted
sudo /usr/local/bin/apt-mirror

# Update Ubuntu dists hierarchy - include universe and multiverse
sudo /home/jkhosali/CheckHierarchy.sh

while read pkgaddition;
do
    echo "Adding package $pkgaddition"
    sudo /home/jkhosali/AddPackage.py $pkgaddition
done < $NPS_PKG_ADDITIONS

exit 0
