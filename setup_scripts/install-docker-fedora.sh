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
# Install Docker on a Fedora system, along with other packages required by Labtainers
#
read -p "This script will reboot the system when done, press enter to continue"

sudo dnf upgrade
sudo dnf install python docker
sudo pip install netaddr
sudo systemctl start docker
sudo systemctl enable docker

sudo groupadd docker
sudo usermod -aG docker $USER

sudo reboot
