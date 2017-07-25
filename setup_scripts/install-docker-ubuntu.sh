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

#needed packages for install
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common 

#adds docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 

#sets up stable repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

#installs Docker: Community Edition
sudo apt-get update
sudo apt-get -y install docker-ce 

#starts and enables docker
sudo systemctl start docker
sudo systemctl enable docker

#gives user docker commands
sudo groupadd docker
sudo usermod -aG docker $USER 

#other packages required by Labtainers
sudo apt-get -y install python-pip 
sudo -H pip install --upgrade pip
sudo -H pip install netaddr

sudo reboot

#Notes: The “-y” after each install means that the user doesn’t need to press “y” in between each package download. The install script is based on this page: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
