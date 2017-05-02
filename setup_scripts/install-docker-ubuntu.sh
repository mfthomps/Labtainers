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
# Install Docker on an Ubuntu system, along with other packages required by Labtainers
#
read -p "This script will reboot the system when done, press enter to continue"

sudo rm -f /tmp/docker.list
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" > /tmp/docker.list
sudo cp /tmp/docker.list /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates
# The step below is to add the GPG key for the official Docker repository to the system
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-get purge lxc-docker
apt-cache policy docker-engine

sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
sudo apt-get install docker-engine
sudo service docker start

sudo groupadd docker
sudo usermod -aG docker $USER

#
# Other packages required by Labtainers
#
sudo apt-get install python-pip
sudo pip install netaddr

sudo reboot
