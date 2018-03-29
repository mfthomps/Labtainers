#!/usr/bin/env bash
#
# Filename: UploadUpdateCentosPlus.sh
#
# Performs the following:
# 1. Copies any *.rpm to /data/html/centosmirror.uc.nps.edu/repos/centosplus/Packages
# 2. Run createrepo
#

if [[ $EUID -ne 0 ]]
then
    echo "This script must be run as root"
    exit 1
fi

# Give usage information
echo "This script is meant to be run after RPMs that are required have been downloaded"
echo "For example: "
echo "1. Go to rpmfind.net and search for leafpad (x86_64)"
echo "2. Save the URL link and use wget to download the RPM"
echo "3. example: wget http://rpmfind.net/linux/fedora/linux/releases/26/Everything/x86_64/os/Packages/l/leafpad-0.8.18.1-16.fc26.x86_64.rpm"

echo
echo "Do you want to continue? (If RPM has not been downloaded, Ctrl-C to break here and go download the RPMs)"
echo "Otherwise, to continue, press <Enter>"
read CONTINUE

# Copies rpm to centosplus/Packages
cp *.rpm /data/html/centosmirror.uc.nps.edu/repos/centosplus/Packages

createrepo /data/html/centosmirror.uc.nps.edu/repos/centosplus/

# chown -R apache:apache /data/html/centosmirror.uc.nps.edu/repos
chown -R apache:apache /data/html/centosmirror.uc.nps.edu/repos

