#!/bin/bash

sudo rm -f /tmp/docker.list
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" > /tmp/docker.list
sudo cp /tmp/docker.list /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-get purge lxc-docker
apt-cache policy docker-engine

sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
sudo apt-get install docker-engine
sudo service docker start

sudo groupadd docker
sudo usermod -aG docker $USER
sudo reboot
