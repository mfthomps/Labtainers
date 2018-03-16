#!/usr/bin/env bash
#
# Filename: UpdateCentosRepo.sh
#
# Assumptions:
# 1. Web server httpd is installed and configured with the following lines in /etc/httpd/conf/httpd.conf file:
# <VirtualHost *:80>
#     DocumentRoot "/var/www/html/centosmirror.uc.nps.edu"
#     Servername centosmirror.uc.nps.edu
# </VirtualHost>
# Note: do not include the '#'
#
# 2. /data is on a separate partition with larger disk size
#
# 3. /etc/yum.conf has been modified to add the following line:
# exclude=java*openjdk* kde* kernel*
# Note: do not include the '#'
# This tells to exclude the packages java*openjdk* kde* kernel*
#
# 4. Add the 'CentOS-Base.repo' into /etc/yum.repos.d directory


if [[ $EUID -ne 0 ]]
then
    echo "This script must be run as root"
    exit 1
fi

reposync --plugins --repoid=base \
  --newest-only --delete --downloadcomps --download-metadata \
  --download_path=/data/html/centosmirror.uc.nps.edu/repos/

reposync --plugins --repoid=centosplus \
  --newest-only --delete --downloadcomps --download-metadata \
  --download_path=/data/html/centosmirror.uc.nps.edu/repos/

reposync --plugins --repoid=extras \
  --newest-only --delete --downloadcomps --download-metadata \
  --download_path=/data/html/centosmirror.uc.nps.edu/repos/

reposync --plugins --repoid=updates \
  --newest-only --delete --downloadcomps --download-metadata \
  --download_path=/data/html/centosmirror.uc.nps.edu/repos/

createrepo /data/html/centosmirror.uc.nps.edu/repos/base/ -g comps.xml
createrepo /data/html/centosmirror.uc.nps.edu/repos/centosplus/
createrepo /data/html/centosmirror.uc.nps.edu/repos/extras/
createrepo /data/html/centosmirror.uc.nps.edu/repos/updates/

# chown -R apache:apache /data/html/centosmirror.uc.nps.edu/repos
chown -R apache:apache /data/html/centosmirror.uc.nps.edu/repos

# Chown /var/www/html/centosmirror.uc.nps.edu just in case
chown apache:apache /var/www/html/centosmirror.uc.nps.edu

# Chown repos just in case
chown -h apache:apache /var/www/html/centosmirror.uc.nps.edu/repos


