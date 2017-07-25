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
#Install Docker on a Debian system, along with other packages required by Labtainers
#
read -p "This script will reboot the system when done, press enter to continue"

#needed packages for Docker install
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common 

#adds Docker’s official GPG Key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

#used to verify matching Key ID (optional)
#sudo apt-key fingerprint 0EBFCD88

#sets up stable repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

#installs Docker:Community Edition
sudo apt-get update
sudo apt-get -y install docker-ce 

#gives user access to docker commands
sudo groupadd docker
sudo usermod -aG docker $USER

#enables and starts docker
sudo systemctl start docker
sudo systemctl enable docker

#additional packages needed for labtainers
sudo apt-get -y install python-pip 
sudo pip install --upgrade pip 
sudo pip install netaddr 

sudo reboot

#Notes: The “-y” after each install means that the user doesn’t need to press “y” in between each package download. The install script is based on this page: https://docs.docker.com/engine/installation/linux/docker-ce/debian/
