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
echo "2. Save the URL link to /etc/nps-rpm-additions"

CURRENTDIR=`pwd`
TMPDIR="/tmp/.wgetdownload"
rm -rf $TMPDIR
mkdir -p $TMPDIR

cd $TMPDIR
/usr/local/bin/DownloadRPMs.sh

# Copies rpm to centosplus/Packages
cp *.rpm /data/html/centosmirror.uc.nps.edu/repos/centosplus/Packages

createrepo /data/html/centosmirror.uc.nps.edu/repos/centosplus/

# chown -R apache:apache /data/html/centosmirror.uc.nps.edu/repos
chown -R apache:apache /data/html/centosmirror.uc.nps.edu/repos

cd $CURRENTDIR
rm -rf $TMPDIR
