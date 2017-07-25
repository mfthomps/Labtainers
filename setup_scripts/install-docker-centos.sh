#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
#
# Install Docker on a CentOS system, along with other packages required by Labtainers
#
read -p "This script will reboot the system when done, press enter to continue"

#needed packages for install
sudo yum update
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

#sets up stable repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

#installs Docker: Community Edition
sudo yum makecache fast
sudo yum install -y docker-ce

#additional packages needed
sudo yum --enablerepo=extras -y install epel-release
sudo yum install -y python-pip
sudo pip install --upgrade pip
sudo pip install netaddr

#starts and enables docker
sudo systemctl start docker
sudo systemctl enable docker

#gives user docker commands
sudo groupadd docker
sudo usermod -aG docker $USER

sudo reboot

#Notes: The “-y” after each install means that the user doesn’t need to press “y” in between each package download. The install script is based on this page: https://docs.docker.com/engine/installation/linux/docker-ce/centos/
