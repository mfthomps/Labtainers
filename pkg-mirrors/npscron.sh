#!/bin/bash

echo "NPS cron jobs"

# Update CentOS repo
sudo /usr/local/bin/UpdateCentosRepo.sh

# Update Ubuntu repo - only main and restricted
sudo /usr/local/bin/apt-mirror

# Update Ubuntu dists hierarchy - include universe and multiverse
sudo /usr/local/bin/CheckHierarchy.sh

# Update Packages
sudo /usr/local/bin/UpdatePackage.sh

# Update CentOS RPMs
sudo /usr/local/bin/UploadUpdateCentosPlus.sh

exit 0
