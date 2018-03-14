#!/usr/bin/env bash
#
# Filename: CreateUbuntuRepo.sh
#
# Assumptions:
# 1. Web server httpd is installed and configured with the following lines in /etc/httpd/conf/httpd.conf file:
# <VirtualHost *:80>
#     DocumentRoot "/var/www/html/ubuntumirror.uc.nps.edu"
#     Servername ubuntumirror.uc.nps.edu
# </VirtualHost>
# Note: do not include the '#'
#
# 2. /data is on a separate partition with larger disk size
#
# 3. /etc/apt/mirror.list has been modified (see attached mirror.list)
#
# 4. apt-mirror has been installed somehow (either by binary or compiled using source)

if [[ $EUID -ne 0 ]]
then
    echo "This script must be run as root"
    exit 1
fi

# Remove /var/spool/apt-mirror if exists (create a soft-link instead)
# Create /data/apt-mirror and soft-link /var/spool/apt-mirror
rm -rf /var/spool/apt-mirror
mkdir /data/apt-mirror
ln -s /data/apt-mirror /var/spool/apt-mirror

# Run apt-mirror
apt-mirror

# chown -R apache:apache /data/apt-mirror/mirror/us.archive.ubuntu.com
chown -R apache:apache /data/apt-mirror/mirror/us.archive.ubuntu.com

# Create and chown /var/www/html/ubuntumirror.uc.nps.edu
mkdir -p /var/www/html/ubuntumirror.uc.nps.edu
chown apache:apache /var/www/html/ubuntumirror.uc.nps.edu

# Link and chown repos
ln -s /data/apt-mirror/mirror/us.archive.ubuntu.com/ubuntu /var/www/html/ubuntumirror.uc.nps.edu/ubuntu
chown -h apache:apache /var/www/html/ubuntumirror.uc.nps.edu/ubuntu

